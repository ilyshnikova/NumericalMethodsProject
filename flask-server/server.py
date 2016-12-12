# -*- coding: utf8 -*-

from flask import Flask, send_from_directory, render_template, request
from modules.tabulator import Tabulator
from modules.cauchy_problem import CauchyProblem, CauchySolution, CircleCauchyFunction, SpiralCauchyFunction
from modules.interpolated_function import PolynomialFunction
from modules.functions import SimpleDiffAdFunction
from modules.tabulator import TabularFunction, CauchyFunctionTabulator
from modules.integration import TabulateIntegration
from modules.interpolator import Interpolator
from modules.ad_server import AdServer, AdServerAutoSetup
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
                'title' : 'Запуск отдельных модулей',
                'href' : '/test-modules',
            },
            {
                'title' : 'Ручной запуск',
                'href' : '/manual-mode'
            },
            {
                'title' : 'Автоматический запуск',
                'href' : '/auto-mode',
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
    demos = [
        {
            'title' : 'Полином 4-ой степени',
            'link' : '/test-modules/interpolator?expression=x**4+-+3*x**2&from_arg=-3&to_arg=3&step=1&precise_step=0.1&result=1',
        },
        {
            'title' : 'Осциллирующая функция',
            'link' : '/test-modules/interpolator?expression=sin%281%2Fx%29&from_arg=0.01&to_arg=10&step=0.1&precise_step=0.01&result=1',
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

        interpolator = Interpolator(tabular_function.obj)
        integrated_function = TabularFunction(interpolator.GetTabularFunction(c_double(float(request.args.get('precise_step')))), constructor='Copy')

        points = tabulator.get_points(integrated_function)
        return render_template(
            "test-modules/interpolation/output.html",
            elements=add_default_values(elements, request),
            data=points,
            return_url=return_url,
            demos=demos,
        )

    else:
        return render_template(
            "input.html",
            elements=elements,
            return_url=return_url,
            demos=demos,
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
    demos = [
        {
            'title' : 'Линейная функция',
            'link' : '/test-modules/integration?expression=x&from_arg=-10&to_arg=10&step=0.1&result=1',
        },
        {
            'title' : 'Квадратичная функция',
            'link' : '/test-modules/integration?expression=x**2&from_arg=-10&to_arg=10&step=0.1&result=1',
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
            demos=demos,
        )
    else:
        return render_template(
            "input.html",
            elements=elements,
            return_url=return_url,
            demos=demos,
        )

def merge_functions(x_points, y_points):
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

    return y_x_data


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
    demos = [
        {
            'title' : 'Круговое решение',
            'link' : '/test-modules/cauchy-problem?equation=CircleCauchyFunction&x0=0&y0=1&x_min=-2&x_max=2&y_min=-2&y_max=2&t_min=0&t_max=10&t_step=0.001&result=1',
        },
        {
            'title' : 'Спиралевидное решение',
            'link' : '/test-modules/cauchy-problem?equation=SpiralCauchyFunction&x0=0.01&y0=0&x_min=-2&x_max=2&y_min=-2&y_max=2&t_min=0&t_max=10&t_step=0.001&result=1',
        },
    ]
    return_url="/test-modules"


    if request.args.get('result'):
        cauchy_function = eval(request.args.get('equation'))()

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
            cauchy_function.obj,
        )

        solution = CauchySolution(cauchy_problem.Solve(), constructor='Copy')
        solution_x_func = TabularFunction(solution.GetX(), constructor='Copy')
        solution_y_func = TabularFunction(solution.GetY(), constructor='Copy')

        tabulator = Tabulator()
        x_points=tabulator.get_points(solution_x_func)
        y_points=tabulator.get_points(solution_y_func)



        return render_template(
            "test-modules/cauchy_problem/output.html",
            elements=add_default_values(elements, request),
            x_min=float(request.args.get('x_min')),
            x_max=float(request.args.get('x_max')),
            y_min=float(request.args.get('y_min')),
            y_max=float(request.args.get('y_max')),
            y_x_data=merge_functions(x_points, y_points),
            return_url=return_url,
            demos=demos,
        )
    else:
        return render_template(
            "input.html",
            elements=elements,
            return_url=return_url,
            demos=demos,
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
    demos = [
        {
            'title' : 'Квадратичная функция',
            'link' : '/test-modules/tabulator?expression=x**2&from_arg=-10&to_arg=10&step=0.1&result=1',
        },
        {
            'title' : 'Кубическая функция',
            'link' : '/test-modules/tabulator?expression=x**3&from_arg=-10&to_arg=10&step=0.1&result=1',
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
            demos=demos,
        )
    else:
        return render_template(
            "input.html",
            elements=elements,
            return_url=return_url,
            demos=demos,
        )

@app.route('/manual-mode')
def manual_mode():
    elements = [
        {
            'title' : 'f',
            'id' : 'f',
            'type' : 'choice',
            'options' : [
                {
                    'title' : 'beta * (S - x)',
                    'id' : 'SimpleDiffAdFunction',
                },
            ],
            'default' : 'SimpleDiffAdFunction',
        },
        {
            'title' : 'rho',
            'id' : 'rho_expression',
        },
        {
            'title' : 'S',
            'id' : 'S_expression',
        },
        {
            'title' : 'z',
            'id' : 'z_expression',
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
            'title' : 'T',
            'id' : 'T',
        },
        {
            'title' : 'step',
            'id' : 'step',
        },
        {
            'title' : 'beta',
            'id' : 'beta',
        },
    ]
    demos = [
        {
            'title' : 'Главный пример',
            'link' : '/manual-mode?f=SimpleDiffAdFunction&rho_expression=6*x*%281+-+x%29&S_expression=3*x+%2B+sin%283*x%29&z_expression=4*x+%2B+cos%28x%29&x0=0&y0=0&T=1&step=0.01&beta=0.03&result=1',
        },
    ]
    return_url="/"
    if request.args.get('result'):
        f_beta = eval(request.args.get('f'))()
        step = float(request.args.get('step'))
        T = float(request.args.get('T'))
        tabulator = Tabulator()
        rho_tabular_function = tabulator.tabulting(request.args.get('rho_expression'), 0, 1, step)
        S_tabular_function = tabulator.tabulting(request.args.get('S_expression'), 0, T, step)
        z_tabular_function = tabulator.tabulting(request.args.get('z_expression'), 0, T, step)

        ad_server = AdServer(
            rho_tabular_function.obj,
            S_tabular_function.obj,
            f_beta.obj,
            z_tabular_function.obj,
            c_double(float(request.args.get('x0'))),
            c_double(float(request.args.get('y0'))),
            c_double(T),
            c_double(step)
        )

        ad_server.SetBeta(c_double(float(request.args.get('beta'))))
        ad_server.SolveCauchyProblem()

        x_tabular_function = TabularFunction(ad_server.GetX(), constructor='Copy')
        y_tabular_function = TabularFunction(ad_server.GetY(), constructor='Copy')

        c_1 = float(ad_server.C1())
        c_2 = float(ad_server.C2())
        phi = float(ad_server.Phi())

        return render_template(
            "manual_mode/output.html",
            elements=add_default_values(elements, request),
            S_x_data=merge_functions(tabulator.get_points(S_tabular_function), tabulator.get_points(x_tabular_function)),
            y_data=tabulator.get_points(y_tabular_function),
            x_data=tabulator.get_points(x_tabular_function),
            S_data=tabulator.get_points(S_tabular_function),
            output_elements=[
                {
                    'title' : 'C1',
                    'value' : c_1,
                },
                {
                    'title' : 'C2',
                    'value' : c_2,
                },
                {
                    'title' : 'Phi',
                    'value' : phi,
                },
            ],
            return_url=return_url,
            demos=demos,
        )
    else:
        return render_template(
            "input.html",
            elements=elements,
            return_url=return_url,
            demos=demos,
        )

@app.route('/auto-mode')
def auto_mode():
    elements = [
        {
            'title' : 'f',
            'id' : 'f',
            'type' : 'choice',
            'options' : [
                {
                    'title' : 'beta * (S - x)',
                    'id' : 'SimpleDiffAdFunction',
                },
            ],
            'default' : 'SimpleDiffAdFunction',
        },
        {
            'title' : 'rho',
            'id' : 'rho_expression',
        },
        {
            'title' : 'S',
            'id' : 'S_expression',
        },
        {
            'title' : 'z',
            'id' : 'z_expression',
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
            'title' : 'step',
            'id' : 'step',
        },
        {
            'title' : 'beta_min',
            'id' : 'beta_min',
        },
        {
            'title' : 'beta_max',
            'id' : 'beta_max',
        },
        {
            'title' : 'beta_precision',
            'id' : 'beta_precision',
        },
    ]
    demos = [
        {
            'title' : 'Главный пример',
            'link' : '/auto-mode?f=SimpleDiffAdFunction&rho_expression=6*x*%281+-+x%29&S_expression=3*x+%2B+sin%283*x%29&z_expression=4*x+%2B+cos%28x%29&y0=0&T=1&step=0.01&beta_min=0.01&beta_max=1&beta_precision=0.001&result=1',
        },
    ]
    return_url="/"
    if request.args.get('result'):
        f_beta = eval(request.args.get('f'))()
        step = float(request.args.get('step'))
        T = float(request.args.get('T'))
        tabulator = Tabulator()
        rho_tabular_function = tabulator.tabulting(request.args.get('rho_expression'), 0, 1, step)
        S_tabular_function = tabulator.tabulting(request.args.get('S_expression'), 0, T, step)
        z_tabular_function = tabulator.tabulting(request.args.get('z_expression'), 0, T, step)

        x0 = float(S_tabular_function.GetValue(c_double(0)))
        y0 = float(request.args.get('y0'))

        ad_server = AdServer(
            rho_tabular_function.obj,
            S_tabular_function.obj,
            f_beta.obj,
            z_tabular_function.obj,
            c_double(x0),
            c_double(y0),
            c_double(T),
            c_double(step)
        )

        ad_server_auto_setup = AdServerAutoSetup(
                ad_server.obj,
                c_double(float(request.args.get("beta_min"))),
                c_double(float(request.args.get("beta_max"))),
                c_double(float(request.args.get("beta_precision"))),
        )

        ad_server_auto_setup.SetupOptimalBeta()

        optimized_ad_server = AdServer(ad_server_auto_setup.GetAdServer(), constructor='Copy')

        beta = float(optimized_ad_server.GetBeta())
        c_1 = float(optimized_ad_server.C1())
        c_2 = float(optimized_ad_server.C2())
        phi = float(optimized_ad_server.Phi())

        x_tabular_function = TabularFunction(optimized_ad_server.GetX(), constructor='Copy')
        y_tabular_function = TabularFunction(optimized_ad_server.GetY(), constructor='Copy')

        S_x_data = merge_functions(tabulator.get_points(S_tabular_function), tabulator.get_points(x_tabular_function))
        y_data=tabulator.get_points(y_tabular_function)
        x_data=tabulator.get_points(x_tabular_function)
        S_data=tabulator.get_points(S_tabular_function)

        print "Done optimizing server"

        S_x_sets = []
        new_step = 0.2
        x0_new = x0 - 3 * new_step
        while x0_new < x0 + 3 * new_step:
            y0_new = y0 - 3 * new_step
            while y0_new < y0 + 3 * new_step:
                optimized_ad_server.SetX0(c_double(x0_new))
                optimized_ad_server.SetY0(c_double(y0_new))
                optimized_ad_server.SolveCauchyProblem()
                x_tabular_function = TabularFunction(optimized_ad_server.GetX(), constructor='Copy')
                S_x_sets.append(
                        merge_functions(tabulator.get_points(S_tabular_function), tabulator.get_points(x_tabular_function))
                )
                y0_new += new_step
            x0_new += new_step


        return render_template(
            "auto_mode/output.html",
            elements=add_default_values(elements, request),
            S_x_data=S_x_data,
            y_data=y_data,
            x_data=x_data,
            S_data=S_data,
            S_x_sets=S_x_sets,
            output_elements=[
                {
                    'title' : 'beta',
                    'value' : beta,
                },
                {
                    'title' : 'C1',
                    'value' : c_1,
                },
                {
                    'title' : 'C2',
                    'value' : c_2,
                },
                {
                    'title' : 'Phi',
                    'value' : phi,
                },
            ],
            return_url=return_url,
            demos=demos,
        )
    else:
        return render_template(
            "input.html",
            elements=elements,
            return_url=return_url,
            demos=demos,
        )




if __name__ == "__main__":
    app.jinja_env.tests['equalto'] = lambda value, other : value == other
    app.run(
        host='::',
        port=5001,
        use_reloader=False,
        debug=True,
        threaded=False,
    )

