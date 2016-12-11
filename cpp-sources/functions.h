#ifndef FUNCTION
#define FUNCTION

#include <map>
#include "interpolated_function.h"

class BaseCauchyFunction {
public:
	virtual double GetValueX(const double x, const double y, const double t) const = 0;
	virtual double GetValueY(const double x, const double y, const double t) const = 0;
};

class TabularCauchyFunction : public BaseCauchyFunction {
private:
	std::map<double, std::map<double, std::map<double, double> > > x_values;
	std::map<double, std::map<double, std::map<double, double> > > y_values;
public:
	void AddValueX(const double x, const double y, const double t, const double value);
	void AddValueY(const double x, const double y, const double t, const double value);

	double GetValueX(const double x, const double y, const double t) const;
	double GetValueY(const double x, const double y, const double t) const;
};

class CircleCauchyFunction : public BaseCauchyFunction {
	double GetValueX(const double x, const double y, const double t) const;
	double GetValueY(const double x, const double y, const double t) const;
};

class SpiralCauchyFunction : public BaseCauchyFunction {
	double GetValueX(const double x, const double y, const double t) const;
	double GetValueY(const double x, const double y, const double t) const;
};

#endif
