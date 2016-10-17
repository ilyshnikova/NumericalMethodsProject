#include "cauchy_problem.h"

CauchySolution::CauchySolution(const TabularFunction& x, const TabularFunction& y)
	: x(x)
	, y(y)
{}

extern "C" {
	CauchyProblem* CauchyProblem_New(
		const double x0,
		const double y0,
		const double betta,
		const double T,
		const PolynomialFunction& U,
		const PolynomialFunction& S,
		const PolynomialFunction& z,
		const F1& f

	) {
		return new CauchyProblem(x0, y0, betta, T, U, S, z, f);
	}

	CauchySolution* CauchySolution_New() {
		return new CauchySolution();
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


