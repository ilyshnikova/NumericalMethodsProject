#ifndef TABULARFUNCTION
#define TABULARFUNCTION

#include <iostream>
#include <map>

class TabularFunction {
private:
    std::map<double, double> ValuesMapping;

    class TabularFunctionConstIterator {
        private:
            std::map<double, double>::const_iterator current;
            std::map<double, double>::const_iterator end;
        public:
            TabularFunctionConstIterator(std::map<double, double>::const_iterator current, std::map<double, double>::const_iterator end)
	            : current(current)
        	    , end(end)
            {}

            bool Next() {
               current++;
            }

            bool IsDefine() const {
                return !(current == end);
            }

            double GetX() const {
                return current->first;
            }

            double GetY() const {
                return current->second;
            }
    };

public:
    TabularFunction();

    TabularFunction(const TabularFunction& function)
        : ValuesMapping(function.GetValues())
    {}

    std::map<double, double> GetValues() const {
        return ValuesMapping;
    }

    double GetValue(const double argument) const;

    void AddValue(const double argument, const double value);

    typedef TabularFunctionConstIterator iterator;

    TabularFunctionConstIterator Begin() const {
        return TabularFunctionConstIterator(ValuesMapping.begin(), ValuesMapping.end());
    }

    size_t Size() const {
    	return ValuesMapping.size();
    }

	TabularFunction Diff() const {
		TabularFunction new_tabular_function;

		double prev_x;
		double prev_y;
		bool first_time = true;
		TabularFunction::iterator it = Begin();
		while (it.IsDefine()) {
			double x = it.GetX();
			double y = it.GetY();
			if (!first_time) {
				new_tabular_function.AddValue(prev_x, (y - prev_y) / (x - prev_x));
			}
			it.Next();
			first_time = false;
			prev_x = x;
			prev_y = y;
		}
		return new_tabular_function;
	}

	TabularFunction MultiplyBy(const double value)  const {
		TabularFunction new_tabular_function;

		TabularFunction::iterator it = Begin();
		while (it.IsDefine()) {
			double x = it.GetX();
			double y = it.GetY();
			new_tabular_function.AddValue(x, y * value);
			it.Next();
		}
		return new_tabular_function;
	}

	TabularFunction MakeValueZero(const double zero_arg) const {
		double subtract = GetValue(zero_arg);
		TabularFunction new_tabular_function;

		TabularFunction::iterator it = Begin();
		while (it.IsDefine()) {
			double x = it.GetX();
			double y = it.GetY();
			new_tabular_function.AddValue(x, y - subtract);
			it.Next();
		}
		return new_tabular_function;
	}

	TabularFunction MultiplyByArgument () const {
		TabularFunction new_tabular_function;

		TabularFunction::iterator it = Begin();
		while (it.IsDefine()) {
			double x = it.GetX();
			double y = it.GetY();
			new_tabular_function.AddValue(x, y * x);
			it.Next();
		}
		return new_tabular_function;
	}

	TabularFunction Combine(const TabularFunction& inner) const {
		TabularFunction new_tabular_function;
		TabularFunction::iterator it = inner.Begin();
		while (it.IsDefine()) {
			double x = it.GetX();
			double y = it.GetY();
			new_tabular_function.AddValue(x, GetValue(y));
			it.Next();
		}
		return new_tabular_function;
	}

	TabularFunction MultiplyByAnotherFunction(const TabularFunction& another_function) const {
		TabularFunction new_tabular_function;

		TabularFunction::iterator it = Begin();
		while (it.IsDefine()) {
			double x = it.GetX();
			double y = it.GetY();
			new_tabular_function.AddValue(x, y * another_function.GetValue(x));
			it.Next();
		}
		return new_tabular_function;
	}
};




#endif
