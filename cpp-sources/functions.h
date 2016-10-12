#ifndef FUNCTION
#define FUNCTION
#include "interpolated_function.h"

class BaseThreeArumentFunction {
public:
	virtual double GetValue(const double first_arg, const double second_arg, const double third_arg);
};

class F1 {
private:
	double betta;
	PolynomialFunction S;
	PolynomialFunction z;
public:
	F1(double betta, const PolynomialFunction& S, const PolynomialFunction& z)
		: betta(betta)
		, S(S)
		, z(z)
	{}

	F1()
		: betta(0)
		, S()
		, z()
	{}

	void SetBetta(double betta) {
		betta = betta;
	}

	void SetS(const PolynomialFunction& s) {
		S = s;
	}

	void SetZ(const PolynomialFunction& _z) {
		z = _z;
	}

	virtual double GetValue(const double first_arg, const double second_arg, const double third_arg=0) {
		return betta * (first_arg - z.GetValue(second_arg));
	}

};

#endif
