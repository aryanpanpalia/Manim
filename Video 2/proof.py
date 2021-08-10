from typing import Awaitable
from manim import *


def integrate(f, a, b):
    delta_x = ((b - a) / 10000)
    iterations = int(abs((b - a) / delta_x))
    area = 0.0
    x = a
    for _ in range(iterations):
        delta_area = f(x) * delta_x
        x = x + delta_x
        area = area + delta_area

    return area


class IntoduceProblem(Scene):

    @staticmethod
    def integral(f, lambd):
        return integrate(lambda x: f(x) * np.cos(lambd * x), 0, 1)

    def construct(self):
        axes = Axes(
            x_range=[-0.1, 1.1, 1],
            y_range=[-10, 10, 5],
            x_axis_config={"numbers_to_include": np.array([0, 1])},
            y_axis_config={"numbers_to_include": [-10, -5, 0, 5, 10]},
            x_length=10,
            y_length=5,
            tips=True
        ).shift(DOWN * 1)
        labels = axes.get_axis_labels(
            x_label=MathTex("x"), y_label=MathTex("y")
        )

        graph = axes.get_graph(
            lambda x: 120 * (x - 0.5) ** 3 - 9 * x ** 2 + 5,
            x_range=[0, 1],
            color
            =YELLOW
        )

        equation = MathTex("f(x)", ".").shift(UP * 3)

        self.play(Create(axes), Write(labels))
        self.play(Create(graph), Write(equation))

        lambd = ValueTracker(25)
        new_graph = axes.get_graph(
            lambda x: (120 * (x - 0.5) ** 3 - 9 * x ** 2 + 5) * np.cos(lambd.get_value() * x),
            x_range=[0, 1],
            color=YELLOW
        )
        new_equation = MathTex("f(x)", "\cos(\lambda x).").shift(UP * 3)
        lambda_onscreen = MathTex("\lambda = ", f"{lambd.get_value()}").shift(UP * 3 + RIGHT * 5)

        self.play(Transform(graph, new_graph), Transform(equation[0], new_equation[0]), Transform(equation[1], new_equation[1]), FadeIn(lambda_onscreen))
        self.wait()
        graph = new_graph
        area = axes.get_area(graph, [0, 1], color=BLUE, opacity=0.5, dx_scaling=0.5)
        self.play(FadeIn(area))
        self.wait()
        # def update_for_lambda():
        #     graph = axes.get_graph(
        #         lambda x: (120 * (x - 0.5) ** 3 - 9 * x ** 2 + 5) * np.cos(lambd.get_value() * x),
        #         x_range=[0, 1],
        #         color=YELLOW
        #     )
        #     area = axes.get_area(graph, [0, 1], color=BLUE, opacity=0.5)
        #     lambda_onscreen = MathTex("\lambda = ", f"{round(lambd.get_value(), 2)}").shift(UP * 3 + RIGHT * 5)
        #     return VGroup(graph, area, lambda_onscreen)

        # update = always_redraw(update_for_lambda)

        # self.remove(graph, lambda_onscreen, area)
        # self.add(update)

        # self.play(lambd.animate(rate_func=rate_functions.linear).set_value(50), run_time=1)
        # self.wait()
