#include "cauchy_problem.h"

TabularFunction CauchySolution::GetX() const {
	return x;
}

TabularFunction CauchySolution::GetY() const {
	return y;
}

CauchySolution::CauchySolution(const TabularFunction& x, const TabularFunction& y)
	: x(x)
	, y(y)
{}

CauchySolution CauchyProblem::Solve() const{
	TabularFunction x, y;

	double prev_x = x0;
	double prev_y = y0;
	double prev_t = t_min;

	double t_cur = t_min;
	while (t_cur <= t_max) {
		if (prev_x > x_max + t_step || prev_x < x_min - t_step || prev_y > y_max + t_step || prev_y < y_min - t_step) {
			break;
		} else {
			double x_cur = prev_x + (t_cur - prev_t) * f->GetValueX(prev_x, prev_y, prev_t);
			double y_cur = prev_y + (t_cur - prev_t) * f->GetValueY(prev_x, prev_y, prev_t);

			x.AddValue(t_cur, x_cur);
			y.AddValue(t_cur, y_cur);

			prev_x = x_cur;
			prev_y = y_cur;
			prev_t = t_cur;

			t_cur += t_step;
		}
	}

	return CauchySolution(x, y);
}


extern "C" {
	CauchyProblem* CauchyProblem_New(
		const double x0,
		const double y0,
		const double x_min,
		const double x_max,
		const double y_min,
		const double y_max,
		const double t_min,
		const double t_max,
		const double t_step,
		BaseCauchyFunction* f
	) {
		return new CauchyProblem(x0, y0, x_min, x_max, y_min, y_max, t_min, t_max, t_step, f);
	}

	CauchySolution* CauchySolution_Copy(const CauchySolution& cauchy_solution) {
		return new CauchySolution(cauchy_solution);
	}

	TabularFunction* CauchySolution_GetX(const CauchySolution& cauchy_solution) {
		return new TabularFunction(cauchy_solution.GetX());
	}

	TabularFunction* CauchySolution_GetY(const CauchySolution& cauchy_solution) {
		return new TabularFunction(cauchy_solution.GetY());
	}

	CauchySolution* CauchyProblem_Solve(CauchyProblem * self) {
		return new CauchySolution(self->Solve());
	}

	void CauchyProblem_Delete(const CauchyProblem& cauchy_problem) {
        	delete &cauchy_problem;
	}

	void CauchySolution_Delete(const CauchySolution& cauchy_solution) {
        	delete &cauchy_solution;
	}
}


