#ifndef CAUCHYPROBLEM
#define CAUCHYPROBLEM
#include "interpolated_function.h"
#include "functions.h"
#include "tabular_function.h"

class CauchySolution {
private:
	TabularFunction x;
	TabularFunction y;

public:
	CauchySolution(const TabularFunction& x, const TabularFunction& y);
	CauchySolution()
		: x()
		, y()
	{}

	TabularFunction GetX() const;

	TabularFunction	GetY() const;
};

class CauchyProblem {
private:
	double x0;
	double y0;
	double x_min;
	double x_max;
	double y_min;
	double y_max;
	double t_min;
	double t_max;
	double t_step;
	BaseCauchyFunction * f;
public:

	CauchyProblem(
		const double x0,
		const double y0,
		const double x_min,
		const double x_max,
		const double y_min,
		const double y_max,
		const double t_min,
		const double t_max,
		const double t_step,
		BaseCauchyFunction * f
	)
	: x0(x0)
	, y0(y0)
	, x_min(x_min)
	, x_max(x_max)
	, y_min(y_min)
	, y_max(y_max)
	, t_min(t_min)
	, t_max(t_max)
	, t_step(t_step)
	, f(f)
	{}

	CauchySolution Solve() const;
};


#endif
