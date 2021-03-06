#include "tabular_function.h"

/* TabularFunction */

TabularFunction::TabularFunction()
	: ValuesMapping()
{}

double TabularFunction::GetValue(const double argument) const {
	if (ValuesMapping.size() == 0) {
		return 0;
	} else {
		std::map<double, double>::const_iterator lower_bound = ValuesMapping.lower_bound(argument);
		if (lower_bound == ValuesMapping.end()) {
			--lower_bound;
		}
		return lower_bound->second;
	}
}

void TabularFunction::AddValue(const double argument, const double value) {
	ValuesMapping[argument] = value;
}


extern "C" {
	TabularFunction* TabularFunction_New() {
		return new TabularFunction();
	}

	double TabularFunction_GetValue(const TabularFunction& self, const double argument) {
		return self.GetValue(argument);
	}

	void TabularFunction_AddValue(TabularFunction& self, const double argument, const double value) {
		self.AddValue(argument, value);
	}

	void TabularFunction_Delete(const TabularFunction& tabular_function) {
        	delete &tabular_function;
	}

	TabularFunction * TabularFunction_Copy(const TabularFunction& tabular_function) {
		return new TabularFunction(tabular_function);
	}

	TabularFunction::iterator* TabularFunctionIterator_New(const TabularFunction& tabular_function) {
        	return new TabularFunction::iterator(tabular_function.Begin());
   	}

    	void TabularFunctionIterator_Next(TabularFunction::iterator& it) {
        	it.Next();
    	}

    	bool TabularFunctionIterator_IsDefine(const TabularFunction::iterator& it) {
        	return it.IsDefine();
    	}

    	double TabularFunctionIterator_GetX(const TabularFunction::iterator& it) {
        	return it.GetX();
    	}

    	double TabularFunctionIterator_GetY(const TabularFunction::iterator& it) {
        	return it.GetY();
   	}

    	void TabularFunctionIterator_Delete(const TabularFunction::iterator& it) {
        	delete &it;
    	}
}
