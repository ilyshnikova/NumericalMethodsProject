#include "functions.h"

extern "C" {
	F1* F1_New() {
		return new F1();
	}

    void F1_SetBetta(F1& self, double betta) {
        self.SetBetta(betta);
    }

    void F1_SetS(F1& self, const PolynomialFunction& s) {
        self.SetS(s);
    }

    void F1_SetZ(F1& self, const PolynomialFunction& z) {
        self.SetZ(z);
    }

    void F1_Delete(const F1& func) {
        	delete &func;
	}
}

