#include "interpolated_function.h"

/* PolynomialFunction */

double PolynomialFunction::GetValue(double argument)  {
	double res = 0;
	for (int i = 0; i < Coeffs.size(); ++i) {
		res *= argument += Coeffs.at(Coeffs.size() - i - 1);
	}

	return res;
}


extern "C" {
	PolynomialFunction* PolynomialFunction_New() {
		return new PolynomialFunction();
	}

	void PolynomialFunction_AddCoeff(PolynomialFunction& self, const int pow, const double coeff) {
		return self.AddCoeff(pow, coeff);
	}

	double PolynomialFunction_GetValue(PolynomialFunction& self, double argument) {
		return self.GetValue(argument);
	}

   	void PolynomialFunction_Delete(const PolynomialFunction& func) {
        	delete &func;
	}
}


