#ifndef INTERPOLATEDFUNCTION
#define INTERPOLATEDFUNCTION
#include <vector>


class PolynomialFunction {
private:
	std::vector<double> Coeffs;

public:
	double GetValue(double argument);
	PolynomialFunction Diff() {
		for (int i = 1; i < Coeffs.size(); ++i) {
			Coeffs[i - 1] = Coeffs[i] * i;
		}
		if (Coeffs.size() >= 1) {
			Coeffs[Coeffs.size() - 1] = 0;
		}
		return *this;
	}

	void AddCoeff(const int pow, const double coeff) {
		while (Coeffs.size() <= pow) {
			Coeffs.push_back(0);
		}
		Coeffs[pow] = coeff;
	}
};

#endif
