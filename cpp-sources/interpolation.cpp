#include <vector>

#include "lin_equations_system.h"
#include "tabular_function.h"
#include "interpolation.h"

TabularFunction Interpolator::Interpolate(const TabularFunction& function) const {
	TabularFunction::iterator tabular_function_iterator = function.Begin();
	TabularFunction interpolated;
	double prev_x = 0;
	double prev_y = 0;
	bool first_time = true;
	while (tabular_function_iterator.IsDefine()) {
		double cur_x = tabular_function_iterator.GetX();
		double cur_y = tabular_function_iterator.GetY();
		if (!first_time) {
			LinearSystem linear_system;

			std::vector<double> left_part_1;
			left_part_1.push_back(cur_x * cur_x * cur_x);
		       	left_part_1.push_back(cur_x * cur_x);
		       	left_part_1.push_back(cur_x);
			left_part_1.push_back(1);
			linear_system.AddEquation(left_part_1, cur_y);

			std::vector<double> left_part_2;
			left_part_2.push_back(prev_x * prev_x * prev_x);
		       	left_part_2.push_back(prev_x * prev_x);
		       	left_part_2.push_back(prev_x);
			left_part_2.push_back(1);
			linear_system.AddEquation(left_part_2, prev_y);

			std::vector<double> left_part_3;
			left_part_3.push_back(3 * cur_x * cur_x);
		       	left_part_3.push_back(2 * cur_x);
		       	left_part_3.push_back(1);
			left_part_3.push_back(0);
			linear_system.AddEquation(left_part_3, 0);

			std::vector<double> left_part_4;
			left_part_4.push_back(3 * prev_x * prev_x);
		       	left_part_4.push_back(2 * prev_x);
		       	left_part_4.push_back(1);
			left_part_4.push_back(0);
			linear_system.AddEquation(left_part_4, 0);

			LinearSystemSolution linear_system_solution = linear_system.Solve();
			LinearSystemSolution::const_iterator linear_system_solution_iterator = linear_system_solution.begin();

			double a = *linear_system_solution_iterator++;
			double b = *linear_system_solution_iterator++;
			double c = *linear_system_solution_iterator++;
			double d = *linear_system_solution_iterator++;

			double x_coord = prev_x;
			while (x_coord < cur_x) {
				interpolated.AddValue(x_coord, a * x_coord * x_coord * x_coord + b * x_coord * x_coord + c * x_coord + d);
				x_coord += precise_step;
			}

		}
		prev_x = cur_x;
		prev_y = cur_y;
		first_time = false;
		tabular_function_iterator.Next();
	}

	return interpolated;
}

extern "C" {
	Interpolator* Interpolator_New(const double precise_step) {
		return new Interpolator(precise_step);
	}

	TabularFunction* Interpolator_Interpolate(const Interpolator& self, const TabularFunction& tabular_function) {
		return new TabularFunction(self.Interpolate(tabular_function));
	}

	void Interpolator_Delete(const Interpolator& self) {
		delete &self;
	}
};


