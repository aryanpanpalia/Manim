from abc import ABC

from manim import *


class TrackingDotsAndRelatedGroups(Scene):

    def create_orbit(self, points, dots, indices, color):
        """
        Creates an orbit with the dots given the indices and then colors the dots in the orbits using the color
        :param points: points on where the dots are
        :param dots: the dots that could be in the orbit
        :param indices: which dots are in the orbit (first and last index should be the same for it to be an orbit).
                        Draws an arrow from the dot at the last index to the dot at the next index. 
        :param color: The color to color all the dots in the orbits
        """
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

        for c, angle in enumerate(np.linspace(0, TAU, num_points, endpoint=False)):
            p = circle.point_at_angle(angle)
            points.append(p)
            d = Dot(point=p)
            dots.append(d)
            label = Integer(number=c + 1).move_to(p * 1.1).scale(0.5)
            self.add(d, label)

        self.create_orbit(points, dots, [0, 4, 10, 17, 7, 0], RED)
        self.create_orbit(points, dots, [1, 9, 16, 1], DARK_BLUE)
        self.create_orbit(points, dots, [2, 6, 14, 5, 19, 2], GREEN)
        self.create_orbit(points, dots, [3, 11, 15, 18, 3], PURPLE_C)
        self.create_orbit(points, dots, [8, 12, 13, 8], ORANGE)


class CustomArrowTip(ArrowTip, Triangle, ABC):
    def __init__(self, **kwargs):
        Triangle.__init__(self)
        self.scale(0.05)
        self.set_color(WHITE)
        self.set_fill(color=WHITE, opacity=100)


class Permutation(Scene):
    def permute(self, dots, labels, permutations):
        transforms = []
        create_arrows = []
        destroy_arrows = []
        fade_out_labels = [FadeOut(label) for label in labels]

        for permutation in permutations:
            for index in range(len(permutation) - 1):
                transforms.append(
                    Transform(
                        dots[permutation[index]], dots[permutation[index + 1]]
                    )
                )
                arrow = Arrow(
                    dots[permutation[index]].get_center(),
                    dots[permutation[index + 1]].get_center(),
                    stroke_width=2,
                    tip_shape=CustomArrowTip,
                    buff=0.15
                )
                create_arrows.append(Create(arrow))
                destroy_arrows.append(Uncreate(arrow))

        self.play(*create_arrows)
        self.play(*fade_out_labels)
        self.play(*transforms, run_time=3)
        self.play(*destroy_arrows)

        fade_in_labels = [FadeIn(label) for label in labels]
        for label, dot in zip(labels, dots):
            label.move_to(dot.get_center() * 1.1)

        self.play(*fade_in_labels)

    def construct(self):
        circle = Circle(radius=3, color=BLACK)
        self.add(circle)

        num_points = 20

        points = []
        dots = []
        labels = []

        for c, angle in enumerate(np.linspace(0, TAU, num_points, endpoint=False)):
            point = circle.point_at_angle(angle)
            points.append(point)
            dot = Dot(point=point)
            dots.append(dot)
            label = Integer(number=c + 1).scale(0.5).move_to(dot.get_center() * 1.1)
            labels.append(label)
            self.add(dot, label)

        permutations = [
            [0, 4, 10, 17, 7, 0],
            [1, 9, 16, 1],
            [2, 6, 14, 5, 19, 2],
            [3, 11, 15, 18, 3],
            [8, 12, 13, 8],
        ]

        self.permute(dots, labels, permutations)
        self.wait()
        self.permute(dots, labels, permutations)
        self.wait()
        self.permute(dots, labels, permutations)
        self.wait()
