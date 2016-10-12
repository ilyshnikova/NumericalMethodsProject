#ifndef LINEQ
#define LINEQ
#include <vector>

class LinearEquation {
private:
	std::vector<double> Coeffs;
	double FreeCoeff;

public:
	LinearEquation(const std::vector<double>& vector, const double val);

	std::vector<double> LinearEquation::GetCoeffs() const;

	double LinearEquation::GetFreeCoeffs() const;
};


class LinearEquationSystem {
private:
	std::vector<std::vector<double>> Coeffs;
	std::vector<double> FreeCoeffs;
public:
	void AddEquation(const LinearEquation& equation);
};


class Solution {
private:
	std::vector<double> solution_coeffs;

};
#endif

