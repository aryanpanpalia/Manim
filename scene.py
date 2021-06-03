import manim
from manim import *


class Square2Circle2Square(manim.Scene):
    def construct(self):
        circle = manim.Circle()
        circle.set_fill(manim.PINK, opacity=0.5)

        square = manim.Square()
        square.flip(manim.RIGHT)
        square.rotate(manim.TAU / 8)

        square2 = manim.Square()
        square2.flip(manim.RIGHT)
        square2.rotate(manim.TAU / 8)
        square2.scale(2)

        self.play(manim.Create(square))
        self.play(manim.Transform(square, circle))
        self.play(manim.Transform(square, square2))
        self.play(manim.Rotate(square, np.array(manim.TAU / 2)))
        self.play(manim.FadeOut(square))


class TextScene(Scene):
    def construct(self):
        text = Text('I will now show the definition of a limit using Manim.').scale(0.75)
        self.play(Write(text))
        self.wait()
        self.play(Unwrite(text), run_time=1.5)
        self.wait()

        limit = MathTex(
            r'\lim_{x\to c} f(x) = L \Longleftrightarrow (',
            r'\forall\epsilon > 0, \exists\delta>0,\forall x \in D,0<|x-c|<\delta \Rightarrow |f(x) - L| < \epsilon',
            r')')

        limit.scale(0.75)

        framebox = SurroundingRectangle(limit[1], buff=.3)
        framebox_text = Text('This is the hard part.').next_to(framebox, UP)

        self.play(Write(limit))
        self.wait()
        self.play(Create(framebox))
        self.play(Write(framebox_text))
        self.wait()
        self.play(Unwrite(limit), FadeOut(framebox), Unwrite(framebox_text), run_time=1)
        self.wait()


class PointsOnCircle(Scene):
    def construct(self):
        circle = Circle(radius=2.0)
        points = circle.points
        for point in points:
            dot = Dot(point=point)
            self.add(dot)
