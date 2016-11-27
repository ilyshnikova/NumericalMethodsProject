#ifndef INTERPOLATION
#define INTERPOLATION

#include "tabular_function.h"

class Interpolator {
private:
	double precise_step;
public:
	Interpolator(const double precise_step)
	: precise_step(precise_step)
	{}

	TabularFunction Interpolate(const TabularFunction& function) const;
};


#endif
