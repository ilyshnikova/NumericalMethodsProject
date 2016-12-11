#include <cmath>
#include "cauchy_problem.h"
#include "ad_server.h"

double SimpleDiffAdFunction::GetValue(const double z, const double x, const double S) const {
	return beta * (S - x);
}

double AdCauchyFunction::GetValueX(const double x, const double y, const double t) const {
	return z_diff.GetValue(t) * U.GetValue(y);
}

double AdCauchyFunction::GetValueY(const double x, const double y, const double t) const {
	return f_beta->GetValue(z.GetValue(t), x, S.GetValue(t));
}

void AdCauchyFunction::SetBeta(const double beta) {
	f_beta->SetBeta(beta);
}

void AdServer::SetBeta(const double beta) {
	ad_cauchy_function.SetBeta(beta);
}

void AdServer::SetX0(const double new_x0) {
	x0 = new_x0;
}

void AdServer::SetY0(const double new_y0) {
	y0 = new_y0;
}

void AdServer::SolveCauchyProblem() {
	CauchyProblem cauchy_problem(
		x0,
		y0,
		0.,
		2. * S.GetValue(T),
		0.,
		1.,
		0.,
		T,
		step,
		&ad_cauchy_function
	);
	CauchySolution cauchy_solution = cauchy_problem.Solve();
	x = cauchy_solution.GetX();
       	y = cauchy_solution.GetY();
}

TabularFunction AdServer::GetS() const {
	return S;
}

TabularFunction AdServer::GetX() const {
	return x;
}

TabularFunction AdServer::GetY() const {
	return y;
}

double AdServer::C1() const {
	TabulateIntegration integration;

	TabularFunction indefinite_integral = integration.Integrate(
		integration.Integrate(rho.MultiplyByArgument()).MultiplyBy(-1).MakeValueZero(1).Combine(y).MultiplyByAnotherFunction(x.Diff())
	);

	return (
		1.
		- (
			indefinite_integral.GetValue(T) - indefinite_integral.GetValue(0)
		)
		/ (
			x.GetValue(T) - x0
		)
	);
}

double AdServer::C2() const {
	return fabs(x.GetValue(T) - S.GetValue(T)) / S.GetValue(T);
}

double AdServer::Phi() const {
	return C1() + 10 * C2();
}

void AdServerAutoSetup::SetX0(const double x0) {
	ad_server.SetX0(x0);
}

void AdServerAutoSetup::SetY0(const double y0) {
	ad_server.SetY0(y0);
}

void AdServerAutoSetup::SetupOptimalBeta() {
	double cur_beta_min = beta_min;
	double cur_beta_max = beta_max;
	while (cur_beta_max - cur_beta_min >= beta_precision) {
		double first_beta = cur_beta_min * 2./3 + cur_beta_max * 1./3;
		double second_beta = cur_beta_min * 1./3 + cur_beta_max * 2./3;

		ad_server.SetBeta(first_beta);
		ad_server.SolveCauchyProblem();
		double first_phi = ad_server.Phi();

		ad_server.SetBeta(second_beta);
		ad_server.SolveCauchyProblem();
		double second_phi = ad_server.Phi();

		if (first_phi < second_phi) {
			cur_beta_max = second_phi;
		} else {
			cur_beta_min = first_phi;
		}
	}

	double optimal_beta = cur_beta_min;
	ad_server.SetBeta(optimal_beta);
	ad_server.SolveCauchyProblem();
}

AdServer AdServerAutoSetup::GetAdServer() const {
	return ad_server;
}

extern "C" {
	SimpleDiffAdFunction* SimpleDiffAdFunction_New() {
		return new SimpleDiffAdFunction();
	}

	void SimpleDiffAdFunction_Delete(const SimpleDiffAdFunction& self) {
		delete &self;
	}

	AdServer* AdServer_New(
		const TabularFunction& rho,
		const TabularFunction& S,
		ParametrisedAdBaseFunction * f_beta,
		const TabularFunction& z,
		const double x0,
		const double y0,
		const double T,
		const double step
	) {
		return new AdServer(
			rho,
			S,
			f_beta,
			z,
			x0,
			y0,
			T,
			step
		);
	}

	TabularFunction* AdServer_GetS(const AdServer& self) {
		return new TabularFunction(self.GetS());
	}

	TabularFunction* AdServer_GetX(const AdServer& self) {
		return new TabularFunction(self.GetX());
	}

	TabularFunction* AdServer_GetY(const AdServer& self) {
		return new TabularFunction(self.GetY());
	}

	double AdServer_C1(const AdServer& self) {
		return self.C1();
	}

	double AdServer_C2(const AdServer& self) {
		return self.C2();
	}

	double AdServer_Phi(const AdServer& self) {
		return self.Phi();
	}

	void AdServer_SetBeta(AdServer& self, const double beta) {
		self.SetBeta(beta);
	}

	void AdServer_SolveCauchyProblem(AdServer& self) {
		self.SolveCauchyProblem();
	}

	AdServer* AdServer_Copy(const AdServer& self) {
		return new AdServer(self);
	}

	void AdServer_Delete(const AdServer& self) {
		delete &self;
	}

	AdServerAutoSetup* AdServerAutoSetup_New(const AdServer& ad_server, const double beta_min, const double beta_max, const double beta_precision) {
		return new AdServerAutoSetup(ad_server, beta_min, beta_max, beta_precision);
	}

	void AdServerAutoSetup_SetupOptimalBeta(AdServerAutoSetup& self) {
		self.SetupOptimalBeta();
	}

	AdServer* AdServerAutoSetup_GetAdServer(const AdServerAutoSetup& self) {
		return new AdServer(self.GetAdServer());
	}

	void AdServerAutoSetup_Delete(const AdServerAutoSetup& self) {
		delete &self;
	}
}
