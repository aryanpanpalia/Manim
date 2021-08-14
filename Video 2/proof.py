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
            x_range=[0, 1, 1e-3],
            color
            =YELLOW
        )

        equation = MathTex("f(x)").shift(UP * 3)

        self.play(Create(axes), Write(labels))
        self.play(Create(graph), Write(equation))

        lambd = ValueTracker(0)
        new_graph = axes.get_graph(
            lambda x: (120 * (x - 0.5) ** 3 - 9 * x ** 2 + 5) * np.cos(lambd.get_value() * x),
            x_range=[0, 1, 1e-3],
            color=YELLOW
        )
        new_equation = MathTex("f(x) \cos(\lambda x)").shift(UP * 3)
        lambda_onscreen = MathTex("\lambda = ", f"{lambd.get_value()}").shift(UP * 3 + RIGHT * 5)

        self.play(Transform(graph, new_graph), Transform(equation, new_equation), FadeIn(lambda_onscreen))
        self.wait()
        
        new_equation = MathTex(r"\int_0^1 f(x) \cos(\lambda x) \text{d}x = ").shift(UP * 3 + LEFT)
        integral_value_text = MathTex(
            f"{round(integrate(lambda x: (120 * (x - 0.5) ** 3 - 9 * x ** 2 + 5) * np.cos(lambd.get_value() * x), 0, 1), 2)}"
        ).next_to(new_equation, RIGHT)

        area = axes.get_area(graph, [0, 1], color=BLUE, opacity=0.5, dx_scaling=0.1)
        self.play(FadeIn(area), Transform(equation, new_equation), FadeIn(integral_value_text))

        def update_for_lambda():
            graph = axes.get_graph(
                lambda x: (120 * (x - 0.5) ** 3 - 9 * x ** 2 + 5) * np.cos(lambd.get_value() * x),
                x_range=[0, 1, 1e-3],
                color=YELLOW
            )
            area = axes.get_area(graph, [0, 1], color=BLUE, opacity=0.5)
            lambda_onscreen = MathTex("\lambda = ", f"{round(lambd.get_value(), 2)}").shift(UP * 3 + RIGHT * 5)
            integral_value_text = MathTex(
                f"{round(integrate(lambda x: (120 * (x - 0.5) ** 3 - 9 * x ** 2 + 5) * np.cos(lambd.get_value() * x), 0, 1), 2)}"
            ).next_to(new_equation, RIGHT)
            return VGroup(graph, area, lambda_onscreen, integral_value_text)

        update = always_redraw(update_for_lambda)

        self.remove(graph, lambda_onscreen, area, new_graph, integral_value_text)
        self.add(update)

        self.play(lambd.animate(rate_func=rate_functions.linear).set_value(50), run_time=1)
        self.wait()


class IntegrationByParts(Scene):
    def construct(self):
        formula = MathTex(
            "\int", "_", "a", "^", "b", "u(x)", "v'(x)", r"\text{d}x", "=", "u(x)", "v(x)", "\\bigg|", 
            "_", "a", "^", "b", "-", "\int", "_", "a", "^", "b", "u'(x)", "v(x)", "\\text{d}x"
        )

        step = MathTex(
            "\int", "_", "0", "^", "1", "f(x)", "\cos(\lambda x)", r"\text{d}x", "=", "f(x)", "\\frac{\sin(\lambda x)}{\lambda}", "\\bigg|", 
            "_", "0", "^", "1", "-", "\int", "_", "0", "^", "1", "f'(x)", "\\frac{\sin(\lambda x)}{\lambda}", "\\text{d}x"
        )
        
        self.play(FadeIn(formula))
        self.wait()
        self.play(*[Transform(formula[index], step[index]) for index in range(25)])
        self.wait()

        step = MathTex(
            "\int", "_", "0", "^", "1", "\cos(\lambda x)", "f(x)", r"\text{d}x", "=", "\cos(\lambda x)", "\int f(x) \\text{d}x", "\\bigg|", 
            "_", "0", "^", "1", "-", "\int", "_", "0", "^", "1", "-\lambda\sin(\lambda x)", "\int f(x) \\text{d}x", "\\text{d}x"
        ).scale(0.8)

        self.play(*[Transform(formula[index], step[index]) for index in range(25)])
        self.wait()