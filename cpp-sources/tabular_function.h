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
};




#endif
