# -*- coding: utf8 -*-

from flask import Flask, send_from_directory, render_template, request
from modules.tabulator import Tabulator
from modules.cauchy_problem import CauchyProblem, CauchySolution
from modules.interpolated_function import PolynomialFunction
from modules.functions import F1
from modules.tabulator import TabularFunction
from modules.integration import TabulateIntegration
from ctypes import c_double, c_bool
import json

app = Flask(__name__)

def add_default_values(elements, request):
    for element in elements:
        value = request.args.get(element['id'])
        if value:
            element['default'] = value

    return elements

@app.route('/files/<path:path>')
def send_file(path):
    return send_from_directory('files', path)

@app.route('/')
def ok():

    return render_template(
        'menu.html',
        elements=[
            {
                'disabled' : True,
                'title' : 'Автоматический запуск',
            },
            {
#                'disabled' : True,
                'title' : 'Ручной запуск',
                'href' : '/manual-mode'
            },
            {
                'title' : 'Запуск отдельных модулей',
                'href' : '/test-modules',
            },
        ],
    )

@app.route('/test-modules')
def main_menu():
    return render_template(
        'menu.html',
        elements=[
            {
                'title' : 'Табулирование функции',
                'href' : '/test-modules/tabulator'
            },
            {
                'title' : 'Интегрирование',
                'href' : '/test-modules/integration',
            },
            {
                'title' : ' Решение задачи Коши',
                'href' : '/test-modules/cauchy-problem',
            },
            {
                'title' : 'Интерполяция',
                'disabled' : True,
            },
            {
                'title' : 'Вернуться',
                'href'  : '/',
            },
        ],
    )

@app.route('/test-modules/integration')
def intergate():
    elements = [
        {
            'title': 'Выражение',
            'id': 'expression',
        },
        {
            'title': 'Начальная точка',
            'id' : 'from_arg',
        },
        {
            'title': 'Конечная точка',
            'id': 'to_arg',
        },
        {
            'title' : 'Шаг',
            'id' : 'step',
        },
    ]
    return_url="/test-modules"
    if request.args.get('result'):
        tabulator = Tabulator()
        tabular_function = tabulator.tabulting(
            request.args.get('expression'),
            float(request.args.get('from_arg')),
            float(request.args.get('to_arg')),
            float(request.args.get('step')),
        )
        tabulate_integration = TabulateIntegration()
        integrated_function = TabularFunction(tabulate_integration.Integrate(tabular_function.obj), constructor='Copy')
        points = tabulator.get_points(integrated_function)
        return render_template(
            "test-modules/integration/output.html",
            elements=add_default_values(elements, request),
            data=points,
            return_url=return_url,
        )
    else:
        return render_template(
            "input.html",
            elements=elements,
            return_url=return_url,
        )

@app.route('/test-modules/cauchy-problem')
def cauchy_problem_input():
    elements = [
        {
            'title' : 'x0',
            'id' : 'x0',
        },
        {
            'title' : 'y0',
            'id' : 'y0',
        },
        {
            'title' : 'T',
            'id' : 'T',
        },
        {
            'title' : 'betta',
            'id' : 'betta',
        },
        {
            'title' : 'U(y) polynom coeffs',
            'id' : 'U',
        },
        {
            'title' : 'S(t) polynom coeffs',
            'id' : 'S',
        },
        {
            'title' : 'z(y) polynom coeffs',
            'id' : 'z',
        },
    ]
    return_url="/test-modules"


    if request.args.get('result'):
        U = PolynomialFunction()
        coeff_index = 0
        for i in request.args.get('U').split(','):
            U.AddCoeff(coeff_index, c_double(float(i)))
            coeff_index += 1

        S = PolynomialFunction()
        coeff_index = 0
        for i in request.args.get('S').split(','):
            S.AddCoeff(coeff_index, c_double(float(i)))
            coeff_index += 1

        z = PolynomialFunction()
        coeff_index = 0
        for i in request.args.get('z').split(','):
            z.AddCoeff(coeff_index, c_double(float(i)))
            coeff_index += 1

        F = F1()
        F.SetBetta(c_double(float(request.args.get('betta'))))
        F.SetS(S.obj)
        F.SetZ(z.obj)

        cauchy_problem = CauchyProblem(
            c_double(float(request.args.get('x0'))),
            c_double(float(request.args.get('y0'))),
            c_double(float(request.args.get('betta'))),
            c_double(float(request.args.get('T'))),
            U.obj,
            S.obj,
            z.obj,
            F.obj,
        )
        solution = CauchySolution(cauchy_problem.Solve(), constructor='Copy')
        solution_x_func = TabularFunction(solution.GetX(), constructor='Copy')
        solution_y_func = TabularFunction(solution.GetY(), constructor='Copy')
        tabulator = Tabulator()
        return render_template(
            "test-modules/cauchy_problem/output.html",
            elements=add_default_values(elements, request),
            x_data=tabulator.get_points(solution_x_func),
            y_data=tabulator.get_points(solution_y_func),
            return_url=return_url,
        )
    else:
        return render_template(
            "input.html",
            elements=elements,
            return_url=return_url,
        )


@app.route('/test-modules/tabulator')
def tabulator_input():
    elements = [
        {
            'title' : 'Выражение',
            'id' : 'expression',
        },
        {
            'title' : 'Начальная точка',
            'id' : 'from_arg',
        },
        {
            'title' : 'Конечная точка',
            'id' : 'to_arg',
        },
        {
            'title' : 'Шаг',
            'id' : 'step',
        },
    ]
    return_url="/test-modules"
    if request.args.get('result'):
        tabulator = Tabulator()
        tabular_function = tabulator.tabulting(
            request.args.get('expression'),
            float(request.args.get('from_arg')),
            float(request.args.get('to_arg')),
            float(request.args.get('step')),
        )
        points = tabulator.get_points(tabular_function)
        return render_template(
            "test-modules/tabulator/output.html",
            elements=add_default_values(elements, request),
            data=points,
            return_url=return_url,
        )
    else:
        return render_template(
            "input.html",
            elements=elements,
            return_url=return_url,
        )

@app.route('/manual-mode')
def functions_input():
    if request.args.get('result'):
        functions = ['p', 'z', 'S']
        points = {}
        for f in functions:
            tabulator = Tabulator()
            tabular_function = tabulator.tabulting(
                request.args.get(f),
                float(request.args.get(f + '_from_arg')),
                float(request.args.get(f + '_to_arg')),
                float(request.args.get(f + '_step')),
            )

            points[f] = tabulator.get_points(tabular_function)
        return json.dumps(points)
    else:
        return render_template(
            "input.html",
            elements=[
                {
                    'title' : 'p(w)',
                    'id' : 'p',
                },
                {
                    'title' : 'Начальная точка',
                    'id' : 'p_from_arg',
                },
                {
                    'title' : 'Конечная точка',
                    'id' : 'p_to_arg',
                },
                {
                    'title' : 'Шаг',
                    'id' : 'p_step',
                },

                {
                    'title' : 'z(t)',
                    'id' : 'z',
                },
                {
                    'title' : 'Начальная точка',
                    'id' : 'z_from_arg',
                },
                {
                    'title' : 'Конечная точка',
                    'id' : 'z_to_arg',
                },
                {
                    'title' : 'Шаг',
                    'id' : 'z_step',
                },

                {
                    'title' : 'S(t)',
                    'id' : 'S',
                },
                {
                    'title' : 'Начальная точка',
                    'id' : 'S_from_arg',
                },
                {
                    'title' : 'Конечная точка',
                    'id' : 'S_to_arg',
                },
                {
                    'title' : 'Шаг',
                    'id' : 'S_step',
                },

            ],
        )



if __name__ == "__main__":
    app.run(
        host='::',
        port=5001,
        use_reloader=False,
        debug=True,
    )

