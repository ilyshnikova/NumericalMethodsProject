#ifndef INTERPOLATION
#define INTERPOLATION

#include "tabular_function.h"

struct CubeSpline {
private:
	double a;
	double b;
	double c;
	double d;
	double cur_x;

public:
	CubeSpline(const double a, const double b, const double c, const double d, const double x)
		: a(a)
		, b(b)
		, c(c)
		, d(d)
		, cur_x(x)
	{}

	double GetValue(const double x) const {
		return a + b * (x - cur_x) + c / 2 * (x - cur_x) * (x - cur_x) + d / 6 * (x - cur_x) * (x - cur_x) * (x - cur_x);
	}
};

class Interpolator {
private:
	std::vector<CubeSpline> splines;
	std::vector<double> bounds;

	void Interpolate(const TabularFunction& function);

public:
	Interpolator(const TabularFunction& function)
	{
		Interpolate(function);
	}

	double GetValue(const double x) const;

	TabularFunction GetTabularFunction(const double precise_step) const {
		TabularFunction interpolated;
		double prev_x = bounds[0];
		for (size_t i = 1; i < bounds.size(); ++i) {
			double cur_x = bounds[i];
			double x = prev_x;
			while (x < cur_x) {
				interpolated.AddValue(x, splines[i - 1].GetValue(x));
				x += precise_step;
			}
			prev_x = cur_x;
		}
		return interpolated;
	}
};


#endif
