#include "tabular_function.h"
#include "tabulate_integration.h"

TabularFunction TabulateIntegration::Integrate(const TabularFunction& function) const {
	TabularFunction integrated;
	TabularFunction::iterator it = function.Begin();

	double integral_value = 0;
	bool first_point = true;
	double prev_y = 0;
	double prev_x = 0;
	while (it.IsDefine()) {
		double x = it.GetX();
		double y = it.GetY();

		if (!first_point) {
			integral_value += (y + prev_y) / 2 * (x - prev_x);
		}

		integrated.AddValue(x, integral_value);
		it.Next();
		first_point = false;
		prev_y = y;
		prev_x = x;
	}

	return integrated;
}

extern "C" {
	TabulateIntegration* TabulateIntegration_New() {
		return new TabulateIntegration();
	}


	TabularFunction* TabulateIntegration_Integrate(const TabulateIntegration& self, const TabularFunction& function) {
	       return new TabularFunction(self.Integrate(function));
      	}

	void TabulateIntegration_Delete(const TabulateIntegration& self) {
		delete &self;
	}
}

