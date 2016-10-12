#include "lin_equation_system.h"

LinearEquation::LinearEquation(const std::vector<double>& vector, const double val)
	: Coeffs(vector)
	, Val(val)
{}

std::vector<double> LinearEquation::GetCoeffs() const {
	return Coeffs;
}

double LinearEquation::GetFreeCoeffs() const {
	return FreeCoeff;
}

void LinearEquationSystem::AddEquation(const LinearEquation& equation) {
	Coeffs.push_back(equation.GetCoeffs());
	FreeCoeffs.push_back(equation.GetFreeCoeff())
}

