#include "tabular_function.h"
#include "functions.h"
#include "interpolation.h"
#include "tabulate_integration.h"

class ParametrisedAdBaseFunction {
protected:
	double beta;
public:
	virtual void SetBeta(const double new_beta) {
		beta = new_beta;
	}

	virtual double GetBeta() const {
		return beta;
	}

	virtual double GetValue(const double z, const double x, const double S) const = 0;
};

class SimpleDiffAdFunction : public ParametrisedAdBaseFunction {
public:
	double GetValue(const double z, const double x, const double S) const;
};

class AdCauchyFunction : public BaseCauchyFunction {
private:
	Interpolator z_diff;
	Interpolator U;
	Interpolator z;
	Interpolator S;
	ParametrisedAdBaseFunction* f_beta;
public:
	AdCauchyFunction(
		const Interpolator& z_diff,
		const Interpolator& U,
		const Interpolator& z,
		const Interpolator& S,
		ParametrisedAdBaseFunction* f_beta
	)
	: z_diff(z_diff)
	, U(U)
	, z(z)
	, S(S)
	, f_beta(f_beta)
	{}

	double GetBeta() const;
	double GetValueX(const double x, const double y, const double t) const;
	double GetValueY(const double x, const double y, const double t) const;

	void SetBeta(const double beta);
};

class AdServer {
private:
	TabularFunction rho;
	TabularFunction S;
	TabularFunction z;
	double x0;
	double y0;
	double T;
	double step;
	TabularFunction x;
	TabularFunction y;
	TabulateIntegration integration;
	AdCauchyFunction ad_cauchy_function;

public:
	AdServer(
		const TabularFunction& rho,
		const TabularFunction& S,
		ParametrisedAdBaseFunction * f_beta,
		const TabularFunction& z,
		const double x0,
		const double y0,
		const double T,
		const double step
	)
	: rho(rho)
	, S(S)
	, z(z)
	, x0(x0)
	, y0(y0)
	, T(T)
	, step(step)
	, integration()
	, ad_cauchy_function(
		Interpolator(z.Diff()),
		Interpolator(integration.Integrate(rho).MultiplyBy(-1).MakeValueZero(1.)),
		Interpolator(z),
		Interpolator(S),
		f_beta
	)
	{
	}


	void SetBeta(const double beta);
	void SetX0(const double x0);
	void SetY0(const double y0);
	void SolveCauchyProblem();

	TabularFunction GetS() const;
	TabularFunction GetX() const;
	TabularFunction GetY() const;

	double GetBeta() const;
	double C1() const;
	double C2() const;
	double Phi() const;
};

class AdServerAutoSetup {
private:
	AdServer ad_server;
	double beta_min;
	double beta_max;
	double beta_precision;
	double x0;
	double y0;
public:
	AdServerAutoSetup(
		const AdServer& ad_server,
		const double beta_min,
		const double beta_max,
		const double beta_precision
	)
	: ad_server(ad_server)
	, beta_min(beta_min)
	, beta_max(beta_max)
	, beta_precision(beta_precision)
	{}

	void SetX0(const double x0);
	void SetY0(const double y0);
	void SetupOptimalBeta();
	AdServer GetAdServer() const;
};

