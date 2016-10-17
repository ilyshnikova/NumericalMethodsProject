# -*- coding: utf8 -*-

from flask import Flask, send_from_directory, render_template, request
from modules.tabulator import Tabulator
from modules.cauchy_problem import CauchyProblem, CauchySolution
from modules.interpolated_function import PolynomialFunction
from modules.functions import F1
from ctypes import c_double, c_bool
import json

app = Flask(__name__)

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
                'disabled' : True,
            },
            {
                'title' : ' Решение задачи Коши',
                'href' : '/test-modules/cauchy-problem',
            },
            {
                'title' : 'Интерполяция',
                'disabled' : True,
            }
        ],
    )


@app.route('/test-modules/cauchy-problem')
def cauchy_problem_input():
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

        solution = cauchy_problem.Solve()
        return "Done"
    else:
        return render_template(
            "input.html",
            elements=[
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


            ],
        )

@app.route('/test-modules/tabulator')
def tabulator_input():
    if request.args.get('result'):
        tabulator = Tabulator()
        tabular_function = tabulator.tabulting(
            request.args.get('expression'),
            float(request.args.get('from_arg')),
            float(request.args.get('to_arg')),
            float(request.args.get('step')),
        )
        points = tabulator.get_points(tabular_function)
        chart = {'type' : 'line', 'renderTo': "progresschart", "height": 400}
        xAxis = {'title' : {'text': 'x'}}
        yAxis ={'title' : {'text': 'x'}}
        series = {'name': 'f(x)', 'data' : points}
        title = {"text": 'Tabular Function'}
#        return render_template('graph.html', chartID='tabular_function', chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
        return json.dumps(points)
    else:
        return render_template(
            "input.html",
            elements=[
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
            ],
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

