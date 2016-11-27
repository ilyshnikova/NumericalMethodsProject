#ifndef LINEQ
#define LINEQ

#include <vector>
#include <algorithm>
#include <cmath>
#include <set>

class LinearSystemSolution {
private:
	bool is_there_solution;
	std::vector<double> solution;

public:

	class ConstIterator {
	private:
		int index;
		const std::vector<double>* solution;
	public:
		ConstIterator(const size_t index, const std::vector<double>* solution)
			: index(index)
			, solution(solution)
		{}

		double operator* () const {
			return solution->operator[](index);
		}

		ConstIterator& operator++() {
			++index;
			return *this;
		}

		ConstIterator operator++(int) {
			ConstIterator tmp(*this);
			++index;
			return tmp;
		}


		bool operator== (const ConstIterator& other) const {
			return index == other.index;
		}



	};

	ConstIterator begin() const {
		return ConstIterator(0, &solution);
	}

	ConstIterator end() const {
		return ConstIterator(solution.size(), &solution);
	}

	typedef ConstIterator const_iterator;

	LinearSystemSolution()
		: is_there_solution(false)
		, solution()
	{}

	LinearSystemSolution(const std::vector<double>& solution)
		: is_there_solution(true)
		, solution(solution)
	{}

	bool IsThereSolution() const {
		return is_there_solution;
	}

	std::vector<double> GetSolution() const {
		return solution;
	}
};

class LinearSystem {
private:

	std::vector<std::vector<double> > left_part_coefficients;
	std::vector<double> right_part_coefficients;


public:

	LinearSystem()
		: left_part_coefficients()
		, right_part_coefficients()
	{}

	LinearSystem& clear() {
		left_part_coefficients.clear();
		right_part_coefficients.clear();
		return *this;
	}

	LinearSystem& AddEquation(
		const std::vector<double>& new_left_part,
		const double right_part
	) {
		left_part_coefficients.push_back(new_left_part);
		right_part_coefficients.push_back(right_part);
		return *this;
	}


	LinearSystem& SwapEquations(const size_t first_index, const size_t second_index) {
		std::swap(left_part_coefficients[first_index], left_part_coefficients[second_index]);
		std::swap(right_part_coefficients[first_index], right_part_coefficients[second_index]);
		return *this;
	}

	LinearSystem& Transformation(const size_t first_index, const size_t second_index, const double coefficient) {
		for (size_t column = 0; column < left_part_coefficients[first_index].size(); ++column) {
			left_part_coefficients[first_index][column] += coefficient * left_part_coefficients[second_index][column];
		}
		right_part_coefficients[first_index] += coefficient * right_part_coefficients[second_index];
		return *this;
	}

	LinearSystemSolution Solve() {
		std::vector<size_t> dependent_vars;

		for (size_t col = 0; col < left_part_coefficients[0].size(); ++col) {
			size_t nonzero_index = -1;
			for (size_t row = dependent_vars.size(); row < left_part_coefficients.size(); ++row) {
				if (left_part_coefficients[row][col] != 0) {
					nonzero_index = row;
					break;
				}
			}
			if (nonzero_index == -1) {
				continue;
			}
			SwapEquations(dependent_vars.size(), nonzero_index);
			const double coefficient = 1 / left_part_coefficients[dependent_vars.size()][col];

			for (size_t row = dependent_vars.size() + 1; row < left_part_coefficients.size(); ++row) {
				Transformation(
					row,
					dependent_vars.size(),
					-left_part_coefficients[row][col] * coefficient
				);
			}
			dependent_vars.push_back(col);
		}

		for (size_t row = dependent_vars.size(); row < right_part_coefficients.size(); ++row) {
			if (right_part_coefficients[row] != 0) {
				return LinearSystemSolution();
			}
		}
		std::vector<double> solution(left_part_coefficients[0].size(), 0);
		size_t last_defined_var = left_part_coefficients[0].size();
		for (int row = static_cast<int>(dependent_vars.size()) - 1; row >= 0; --row) {
			double res = right_part_coefficients[row];
			for (size_t col = dependent_vars[row] + 1; col < left_part_coefficients.size(); ++col) {
				res -= left_part_coefficients[row][col] * solution[col];
			}
			res /= left_part_coefficients[row][dependent_vars[row]];
			solution[dependent_vars[row]] = res;
		}
		return LinearSystemSolution(solution);
	}
};


#endif
