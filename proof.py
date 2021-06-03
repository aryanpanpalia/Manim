from manim import *


class Permutation(Scene):

    def create_orbit(self, points, dots, indices, color):
        arrows = []
        for c in range(len(indices)):
            this_index = indices[c]
            last_index = indices[c - 1]
            arrow = Arrow(points[last_index], points[this_index], stroke_width=2)
            arrows.append(arrow)

        for arrow in arrows:
            self.play(Create(arrow), run_time=0.5)

        change_colors = [ApplyMethod(dots[i].set_color, color) for i in indices]
        self.play(*change_colors, run_time=0.5)
        fade_out_arrows = [FadeOut(arrow) for arrow in arrows]
        self.play(*fade_out_arrows, run_time=0.5)
        self.wait()


    def construct(self):
        circle = Circle(radius=3, color=BLACK)
        self.add(circle)

        num_points = 20

        points = []
        dots = []

        for c, angle in enumerate(np.linspace(0, TAU, num_points + 1)):
            p = circle.point_at_angle(angle)
            points.append(p)
            d = Dot(point=p)
            dots.append(d)
            if c != 20:
                label = Integer(number=c + 1).move_to(p * 1.1).scale(0.5)
                self.add(d, label)
            else:
                self.add(d)

        self.create_orbit(points, dots, [0, 4, 10, 17, 7, 20], RED)
        self.create_orbit(points, dots, [1, 9, 16, 1], DARK_BLUE)
        self.create_orbit(points, dots, [2, 6, 14, 5, 19, 2], GREEN)
        self.create_orbit(points, dots, [3, 11, 16, 18, 3], PURPLE)
        self.create_orbit(points, dots, [8, 12, 13, 8], ORANGE)
        self.create_orbit(points, dots, [15, 15], PINK)
