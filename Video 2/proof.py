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


class Learning(Scene):

    @staticmethod
    def integral(f, lambd):
        return integrate(lambda x: f(x) * np.sin(lambd * x), 0, 1)

    def construct(self):
        axes = Axes(
            x_range=[0, 250, 50],
            y_range=[-5, 5, 5],
            x_axis_config={"numbers_to_include": np.arange(0, 251, 50)},
            y_axis_config={"numbers_to_include": [-5, 0, 5]},
            y_length=5,
            tips=False
        )
        labels = axes.get_axis_labels(
            x_label=MathTex("\lambda"), y_label=MathTex("\int_0^1 20x^2 \sin(\lambda x) \\text{d}x")
        )
        print(axes.x_axis_config)

        graph = axes.get_graph(
            lambda lambd: self.integral(lambda x: 20 * x ** 2, lambd),
            x_range=[0, 250],
            color=YELLOW
        )

        self.play(Create(axes), Write(labels))
        self.play(Create(graph))
        self.wait()
