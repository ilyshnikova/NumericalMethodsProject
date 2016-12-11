# -*- coding: utf8 -*-

from flask import Flask, send_from_directory, render_template, request
from modules.tabulator import Tabulator
from modules.cauchy_problem import CauchyProblem, CauchySolution, CircleCauchyFunction, SpiralCauchyFunction
from modules.interpolated_function import PolynomialFunction
from modules.functions import F1
from modules.tabulator import TabularFunction, CauchyFunctionTabulator
from modules.integration import TabulateIntegration
from modules.interpolator import Interpolator
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
                'href' : '/test-modules/interpolator',
            },
            {
                'title' : 'Вернуться',
                'href'  : '/',
            },
        ],
    )

@app.route('/test-modules/interpolator')
def interpolate():
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
            'title' : 'Шаг табулированной функции',
            'id' : 'step',
        },
        {
            'title' : 'Шаг интерполированной функции',
            'id' : 'precise_step',
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
        interpolator = Interpolator(c_double(float(request.args.get('precise_step'))))
        integrated_function = TabularFunction(interpolator.Interpolate(tabular_function.obj), constructor='Copy')
        points = tabulator.get_points(integrated_function)
        return render_template(
            "test-modules/interpolation/output.html",
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
            'title': 'Equation',
            'id': 'equation',
            'type' : 'choice',
            'options' : [
                {
                    'title' : 'D(x) = y, D(y) = -x',
                    'id' : 'CircleCauchyFunction',
                },
                {
                    'title' : 'D(x) = x + y, D(y) = y - 20 * x',
                    'id' : 'SpiralCauchyFunction',
                },
            ],
            'default': 'CircleCauchyFunction',
        },
        {
            'title' : 'x0',
            'id' : 'x0',
        },
        {
            'title' : 'y0',
            'id' : 'y0',
        },
        {
            'title' : 'x_min',
            'id' : 'x_min',
        },
        {
            'title' : 'x_max',
            'id' : 'x_max',
        },
        {
            'title' : 'y_min',
            'id' : 'y_min',
        },
        {
            'title' : 'y_max',
            'id' : 'y_max',
        },
        {
            'title' : 't_min',
            'id' : 't_min',
        },
        {
            'title' : 't_max',
            'id' : 't_max',
        },
        {
            'title' : 't_step',
            'id' : 't_step',
        },
    ]
    return_url="/test-modules"


    if request.args.get('result'):
        cauchy_function_tabulator = CauchyFunctionTabulator(
            float(request.args.get('t_min')),
            float(request.args.get('t_max')),
            float(request.args.get('t_step')),
            float(request.args.get('x_min')),
            float(request.args.get('x_max')),
            float(request.args.get('y_min')),
            float(request.args.get('y_max')),
        )
        tabular_cauchy_function = eval(request.args.get('equation'))()
        #cauchy_function_tabulator.tabulate(request.args.get('f_x'), request.args.get('f_y'))

        cauchy_problem = CauchyProblem(
            c_double(float(request.args.get('x0'))),
            c_double(float(request.args.get('y0'))),
            c_double(float(request.args.get('x_min'))),
            c_double(float(request.args.get('x_max'))),
            c_double(float(request.args.get('y_min'))),
            c_double(float(request.args.get('y_max'))),
            c_double(float(request.args.get('t_min'))),
            c_double(float(request.args.get('t_max'))),
            c_double(float(request.args.get('t_step'))),
            tabular_cauchy_function.obj,
        )

        solution = CauchySolution(cauchy_problem.Solve(), constructor='Copy')
        solution_x_func = TabularFunction(solution.GetX(), constructor='Copy')
        solution_y_func = TabularFunction(solution.GetY(), constructor='Copy')

        tabulator = Tabulator()
        x_points=tabulator.get_points(solution_x_func)
        y_points=tabulator.get_points(solution_y_func)

        y_x_dict = {}

        for point in x_points:
            t = point[0]
            x = point[1]
            y_x_dict.setdefault(t, {}).setdefault('x', x)

        for point in y_points:
            t = point[0]
            y = point[1]
            y_x_dict.setdefault(t, {}).setdefault('y', y)

        y_x_data = []
        for t in sorted(y_x_dict.keys()):
            if 'x' in y_x_dict[t] and 'y' in y_x_dict[t]:
                y_x_data.append((y_x_dict[t]['x'], y_x_dict[t]['y']))

        return render_template(
            "test-modules/cauchy_problem/output.html",
            elements=add_default_values(elements, request),
            x_min=float(request.args.get('x_min')),
            x_max=float(request.args.get('x_max')),
            y_min=float(request.args.get('y_min')),
            y_max=float(request.args.get('y_max')),
            y_x_data=y_x_data,
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
    app.jinja_env.tests['equalto'] = lambda value, other : value == other
    app.run(
        host='::',
        port=5001,
        use_reloader=False,
        debug=True,
    )

