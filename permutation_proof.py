from abc import ABC

from manim import *


def approx(array1, array2):
    for element1, element2 in zip(array1, array2):
        if not (element1 - 0.05 < element2 < element1 + 0.05):
            return False
    return True


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
        self.set_fill(color=WHITE, opacity=0)


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


class ExplainingPermutations(Scene):
    num_permutes = 0

    def permute(self, dots, permutation: dict):
        transforms = []
        create_arcs = []
        uncreate_arcs = []

        for key, value in permutation.items():
            this = dots[key]
            other = dots[value]
            transforms.append(Transform(this, other, path_arc=PI))

            halfdist = np.linalg.norm(np.array(this.get_center()) - np.array(other.get_center())) / 2
            arc = CurvedArrow(this.get_center(), other.get_center(), radius=halfdist, tip_shape=CustomArrowTip,
                              stroke_opacity=0.5)

            center = arc.get_arc_center()
            arrowtip = Triangle().scale(0.05).move_to(center)
            if this.get_x() > other.get_x():
                arc = Arc(start_angle=PI + 0.3, angle=PI - 0.6, arc_center=center, radius=-halfdist)
                arrowtip.shift(UP * halfdist).rotate(3 * PI / 6).set_fill(WHITE).set_color(WHITE)
            else:
                arc = Arc(start_angle=PI + 0.3, angle=PI - 0.6, arc_center=center, radius=halfdist)
                arrowtip.shift(DOWN * halfdist).rotate(PI / 6).set_fill(WHITE).set_color(WHITE)

            arc.add(arrowtip)
            create_arcs.append(Create(arc))
            uncreate_arcs.append(Uncreate(arc))

        self.play(*create_arcs)
        self.play(*transforms)
        self.num_permutes += 1
        self.play(*uncreate_arcs)

    def construct(self):
        dot1 = Dot(LEFT * 2)
        dot2 = Dot(LEFT)
        dot3 = Dot()
        dot4 = Dot(RIGHT)
        dot5 = Dot(RIGHT * 2)

        label1 = Integer(1).scale(0.5).next_to(dot1, UP)
        label2 = Integer(2).scale(0.5).next_to(dot2, UP)
        label3 = Integer(3).scale(0.5).next_to(dot3, UP)
        label4 = Integer(4).scale(0.5).next_to(dot4, UP)
        label5 = Integer(5).scale(0.5).next_to(dot5, UP)

        dots = [dot1, dot2, dot3, dot4, dot5]
        labels = [label1, label2, label3, label4, label5]

        dots_copy = [dot.copy() for dot in dots]
        labels_copy = [label.copy() for label in labels]

        group_of_dots = VGroup(*dots)

        group_of_copy_dots = VGroup(*dots_copy)
        group_of_labels_copy = VGroup(*labels_copy)

        label1.add_updater(lambda l: l.next_to(dot1, UP))
        label2.add_updater(lambda l: l.next_to(dot2, UP))
        label3.add_updater(lambda l: l.next_to(dot3, UP))
        label4.add_updater(lambda l: l.next_to(dot4, UP))
        label5.add_updater(lambda l: l.next_to(dot5, UP))

        counter = Integer(0).scale(0.5).move_to(RIGHT * 4 + UP * 3.5)
        counter.add_updater(lambda i: i.set_value(self.num_permutes))
        self.add(counter)

        permutation = {
            0: 2,
            1: 4,
            2: 0,
            3: 1,
            4: 3
        }

        self.play(*[FadeIn(dot) for dot in dots], *[Write(label) for label in labels], run_time=0.5)
        self.add(*labels_copy, *dots_copy)

        self.play(ApplyMethod(group_of_dots.shift, UP * 2),
                  ApplyMethod(group_of_copy_dots.shift, DOWN),
                  ApplyMethod(group_of_labels_copy.shift, DOWN),
                  )

        self.play(ApplyMethod(group_of_copy_dots.set_fill, GRAY), ApplyMethod(group_of_labels_copy.set_fill, GRAY))

        self.permute(dots, permutation)
        self.wait()
        self.permute(dots, permutation)
        self.wait()
        self.permute(dots, permutation)
        self.wait()


class RotatePermutation(Scene):

    def rotate_permutation(self, dots, labels, dot_loc, label_loc):
        transforms = []
        fade_in_arrows = []
        fade_out_arrows = []
        for index in range(20):
            last_dot = dots[index - 1]
            this_dot = dots[index]
            last_label = labels[index - 1]
            this_label = labels[index]

            transforms.append(Transform(last_dot, this_dot))

            if approx(last_label.get_center(), label_loc):
                last_label = last_label.set_value(this_label.get_value() - 1)

            transforms.append(
                Transform(last_label, this_label.copy().set_value(last_label.get_value()))
            )

            if not (approx(this_dot.get_center(), dot_loc) or approx(last_dot.get_center(), dot_loc)):
                arrow = Arrow(
                    last_dot.get_center(),
                    this_dot.get_center(),
                    stroke_width=2,
                    tip_shape=CustomArrowTip,
                    buff=0.15
                )
                fade_in_arrows.append(FadeIn(arrow))
                fade_out_arrows.append(FadeOut(arrow))

        self.play(*fade_in_arrows)
        self.play(*transforms)
        self.play(*fade_out_arrows)

    def construct(self):
        circle = Circle(radius=3, color=BLACK)
        self.add(circle)

        num_points = 20

        points = []
        dots = []
        labels = []

        for c, angle in enumerate(np.linspace(0, TAU, num_points, endpoint=False)):
            p = circle.point_at_angle(angle)
            points.append(p)
            d = Dot(point=p)
            dots.append(d)
            label = Integer(number=c + 1).move_to(p * 1.15).scale(0.5)
            labels.append(label)

        for c in range(1, 7, 1):
            labels[-c].set_value(1001 - c)

        dot_loc = dots[13].get_center()
        label_loc = labels[13].get_center()
        dots[13].set_color(BLACK)
        labels[13].set_color(BLACK)

        angle = Line(start=dots[12].get_center(), end=dots[14].get_center()).get_angle()
        etc = Text('...').move_to(dot_loc).rotate(angle)

        self.play(*[FadeIn(dot) for dot in dots], *[FadeIn(label) for label in labels], FadeIn(etc))

        self.rotate_permutation(dots, labels, dot_loc, label_loc)
        self.rotate_permutation(dots, labels, dot_loc, label_loc)
        self.rotate_permutation(dots, labels, dot_loc, label_loc)
        self.rotate_permutation(dots, labels, dot_loc, label_loc)
