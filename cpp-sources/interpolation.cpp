#include <vector>

#include "lin_equations_system.h"
#include "tabular_function.h"
#include "interpolation.h"

void Interpolator::Interpolate(const TabularFunction& function) {
	TabularFunction::iterator tabular_function_iterator = function.Begin();

	size_t n = function.Size();
	if (n < 2) {
		return;
	} else {
		--n;
	}

	LinearSystem linear_system;

	std::vector<double> first_lin_eq(n + 1, 1);
	for (size_t i = 1; i < n + 1; ++i) {
		first_lin_eq[i] = 0;
	}
	linear_system.AddEquation(first_lin_eq, 0);

	std::vector<double> second_lin_eq(n + 1, 0);
	second_lin_eq[n] = 1;
	linear_system.AddEquation(second_lin_eq, 0);

	double prev_x = 0;
	double prev_y = 0;
	size_t step_index = 0;
	while (tabular_function_iterator.IsDefine()) {
		double cur_x = tabular_function_iterator.GetX();
		double cur_y = tabular_function_iterator.GetY();
		tabular_function_iterator.Next();

		if (step_index != 0 && tabular_function_iterator.IsDefine()) {
			double post_x = tabular_function_iterator.GetX();
			double post_y = tabular_function_iterator.GetY();

			double cur_h = cur_x - prev_x;
			double post_h = post_x - cur_x;

			std::vector<double> left_part(n + 1, 0);
			left_part[step_index - 1] = cur_h;
			left_part[step_index] = 2 * (cur_h + post_h);
			left_part[step_index + 1] = post_h;

			linear_system.AddEquation(left_part, 6 * ((post_y - cur_y) / post_h - (cur_y - prev_y) / cur_h));
		}
		prev_x = cur_x;
		prev_y = cur_y;
		++step_index;
	}

	LinearSystemSolution linear_system_solution = linear_system.Solve();
	LinearSystemSolution::const_iterator linear_system_solution_iterator = linear_system_solution.begin();
	tabular_function_iterator = function.Begin();

	step_index = 0;
	double prev_c = 0;

	while (
		linear_system_solution_iterator.IsDefine() &&
		tabular_function_iterator.IsDefine()
	) {
		double c = *linear_system_solution_iterator;
		double cur_x = tabular_function_iterator.GetX();
		double cur_y = tabular_function_iterator.GetY();
		bounds.push_back(cur_x);
		if (step_index != 0) {
			double cur_h = cur_x - prev_x;
			double a = cur_y;
			double d = (c - prev_c) / cur_h;
			double b = (cur_y - prev_y) / cur_h + cur_h * (2 * c + prev_c) / 6;
			splines.push_back(CubeSpline(a, b, c, d, cur_x));

		}
		prev_x = cur_x;
		prev_y = cur_y;
		prev_c = c;

		tabular_function_iterator.Next();
		++linear_system_solution_iterator;
		++step_index;
	}
}

double Interpolator::GetValue(const double x) const {
	double index = std::lower_bound(bounds.begin(), bounds.end(), x) - bounds.begin();
	if (index >= splines.size()) {
		--index;
	}
	return splines[index].GetValue(x);
}

extern "C" {
	Interpolator* Interpolator_New(const TabularFunction& tabular_function) {
		return new Interpolator(tabular_function);
	}

	TabularFunction* Interpolator_GetTabularFunction(const Interpolator& self, const double precise_step) {
		return new TabularFunction(self.GetTabularFunction(precise_step));
	}

	void Interpolator_Delete(const Interpolator& self) {
		delete &self;
	}
};


