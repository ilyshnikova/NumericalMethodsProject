#include <iostream>
#include <map>
#include <cmath>
#include "functions.h"

template
<typename T>
const T * find_closest(const std::map<double, T> * some_map, const double some_key) {
	double lower_key = some_map->lower_bound(some_key)->first;
	double upper_key = some_map->upper_bound(some_key)->first;

	if (fabs(lower_key - some_key) < fabs(upper_key - some_key)) {
		return &(some_map->at(lower_key));
	} else {
		return &(some_map->at(upper_key));
	}
}

void TabularCauchyFunction::AddValueX(const double x, const double y, const double t, const double value) {
	if (x_values.count(x) == 0) {
	       x_values[x] = std::map<double, std::map<double, double> >();
      	}
	if (x_values[x].count(y) == 0) {
		x_values[x][y] = std::map<double, double>();
	}
	x_values[x][y][t] = value;
}

void TabularCauchyFunction::AddValueY(const double x, const double y, const double t, const double value) {
	if (y_values.count(x) == 0) {
	       y_values[x] = std::map<double, std::map<double, double> >();
      	}
	if (y_values[x].count(y) == 0) {
		x_values[x][y] = std::map<double, double>();
	}
	y_values[x][y][t] = value;
}

double TabularCauchyFunction::GetValueX(const double x, const double y, const double t) const {
	return *(find_closest(find_closest(find_closest(&x_values, x), y), t));
}

double TabularCauchyFunction::GetValueY(const double x, const double y, const double t) const {
	return *(find_closest(find_closest(find_closest(&y_values, x), y), t));
}

double CircleCauchyFunction::GetValueX(const double x, const double y, const double t) const {
	return y;
}

double CircleCauchyFunction::GetValueY(const double x, const double y, const double t) const {
	return -x;
}

double SpiralCauchyFunction::GetValueX(const double x, const double y, const double t) const {
	return x + y;
}

double SpiralCauchyFunction::GetValueY(const double x, const double y, const double t) const {
	return y -  20 * x;
}



extern "C" {
	TabularCauchyFunction* TabularCauchyFunction_New() {
		return new TabularCauchyFunction();
	}

	void TabularCauchyFunction_AddValueX(TabularCauchyFunction& self, const double x, const double y, const double t, const double value) {
		self.AddValueX(x, y, t, value);
	}

	void TabularCauchyFunction_AddValueY(TabularCauchyFunction& self, const double x, const double y, const double t, const double value) {
		self.AddValueY(x, y, t, value);
	}

	void TabularCauchyFunction_Delete(const TabularCauchyFunction& self) {
		delete &self;
	}

	CircleCauchyFunction* CircleCauchyFunction_New() {
		return new CircleCauchyFunction();
	}

	void CircleCauchyFunction_Delete(const CircleCauchyFunction& self) {
		delete &self;
	}

	SpiralCauchyFunction* SpiralCauchyFunction_New() {
		return new SpiralCauchyFunction();
	}

	void SpiralCauchyFunction_Delete(const SpiralCauchyFunction& self) {
		delete &self;
	}
}

