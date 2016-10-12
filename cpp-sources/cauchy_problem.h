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
};



class CauchyProblem {
private:
	double x0;
	double y0;
	double betta;
	double T;
	PolynomialFunction U;
	PolynomialFunction S;
	PolynomialFunction z;
	F1 f;
public:

	CauchyProblem(
		const double x0,
		const double y0,
		const double betta,
		const double T,
		const PolynomialFunction& U,
		const PolynomialFunction& S,
		const PolynomialFunction& z,
		const F1& f2
	)
		: x0(x0)
		, y0(y0)
		, betta(betta)
		, T(T)
        , U(U)
        , S(S)
        , z(z)
		, f(f2)
	{}


	CauchySolution Solve() {
		double step = T / 1000.;
		TabularFunction x, y;

		x.AddValue(x0, 0);
		y.AddValue(y0, 0);
		double prev_x = x0;
		double prev_y = y0;

		for (int t = 0; t <= T; t+=step) {
			double cur_x = z.Diff().GetValue(t) * U.GetValue(prev_y);
			double cur_y = f.GetValue(prev_x, t, 0) * step + prev_y;

			x.AddValue(cur_x, t);
			y.AddValue(cur_y, t);

			prev_x = cur_x;
			prev_y = cur_y;
		}
		return CauchySolution(x, y);
   	}
};


#endif
