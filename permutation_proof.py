from abc import ABC

import colour
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
                arrow = make_arrow_between(dots[permutation[index]], dots[permutation[index + 1]])
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
                arrow = make_arrow_between(last_dot, this_dot)
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


class IdentityIn5(Scene):
    num_permutes = 0

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
                arrow = make_arrow_between(dots[permutation[index]], dots[permutation[index + 1]])
                create_arrows.append(FadeIn(arrow))
                destroy_arrows.append(FadeOut(arrow))

        self.play(*create_arrows)
        self.play(*fade_out_labels)
        self.play(*transforms, *destroy_arrows, run_time=2)
        self.num_permutes += 1
        fade_in_labels = [FadeIn(label) for label in labels]
        for label, dot in zip(labels, dots):
            label.move_to(dot.get_center() * 1.1)

        self.play(*fade_in_labels)

    def construct(self):
        circle = Circle(radius=3, color=BLACK)
        self.add(circle)

        num_points = 20

        dots = []
        labels = []

        for c, angle in enumerate(np.linspace(0, TAU, num_points, endpoint=False)):
            point = circle.point_at_angle(angle)
            dot = Dot(point=point)
            dots.append(dot)
            label = Integer(number=c + 1).scale(0.5).move_to(dot.get_center() * 1.1)
            labels.append(label)
            self.add(dot, label)

        permutations = [
            [0, 4, 8, 12, 16, 0],
            [1, 5, 9, 13, 17, 1],
            [2, 6, 10, 14, 18, 2],
            [3, 7, 11, 15, 19, 3],
        ]

        counter = Integer(0).scale(0.5).move_to(RIGHT * 4 + UP * 3.5)
        counter.add_updater(lambda i: i.set_value(self.num_permutes))
        self.add(counter)

        for _ in range(5):
            self.permute(dots, labels, permutations)
            self.wait()


def make_arrow_between(dot1, dot2):
    arrow = Arrow(
        dot1.get_center(),
        dot2.get_center(),
        stroke_width=2,
        tip_shape=CustomArrowTip,
        buff=0.15
    )

    return arrow


def arrow_add_sticky_updater(arrow, dot1, dot2):
    arrow.add_updater(
        lambda arw: arw.put_start_and_end_on(
            Line(start=dot1.get_center(), end=dot2.get_center()).scale(0.9).get_start(),
            Line(start=dot1.get_center(), end=dot2.get_center()).scale(0.9).get_end()
        )
    )


def make_sticky_arrow_between(dot1, dot2):
    arrow = make_arrow_between(dot1, dot2)
    arrow_add_sticky_updater(arrow, dot1, dot2)

    return arrow


class TrackingOne(Scene):

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
            d = Dot(point=p).set_color(colour.Color("#222222"))
            dots.append(d)
            label = Integer(number=c + 1).move_to(p * 1.15).scale(0.5)
            labels.append(label)

        for c in range(1, 7, 1):
            labels[-c].set_value(1001 - c)

        dot_loc = dots[13].get_center()
        dots[13].set_color(BLACK)
        labels[13].set_color(BLACK)

        angle = Line(start=dots[12].get_center(), end=dots[14].get_center()).get_angle()
        etc = Text('...').move_to(dot_loc).rotate(angle).set_color("#222222")

        self.play(*[FadeIn(dot) for dot in dots], *[FadeIn(label) for label in labels], FadeIn(etc))
        self.wait()

        one = dots[0]
        start_one = one.get_center()

        self.play(ApplyMethod(one.set_color, WHITE))

        self.play(ApplyMethod(one.move_to, dots[4]), FadeOut(dots[4]))
        self.play(ApplyMethod(one.move_to, dots[10]), FadeIn(dots[4]), FadeOut(dots[10]))
        self.play(ApplyMethod(one.move_to, dots[16]), FadeIn(dots[10]), FadeOut(dots[16]))
        self.play(ApplyMethod(one.move_to, dots[7]), FadeIn(dots[16]), FadeOut(dots[7]))
        self.play(ApplyMethod(one.move_to, start_one), FadeIn(dots[7]))

        self.wait(2)

        five = dots[4]
        start_five = five.get_center()
        self.play(ApplyMethod(five.set_color, WHITE))

        self.play(ApplyMethod(one.move_to, five), ApplyMethod(five.move_to, dots[10]), FadeOut(dots[10]))
        self.play(ApplyMethod(one.move_to, dots[10]), ApplyMethod(five.move_to, dots[16]), FadeOut(dots[16]))
        self.play(ApplyMethod(one.move_to, dots[16]), ApplyMethod(five.move_to, dots[7]), FadeOut(dots[7]),
                  FadeIn(dots[10]))
        self.play(ApplyMethod(one.move_to, dots[7]), ApplyMethod(five.move_to, start_one), FadeIn(dots[16]))
        self.play(ApplyMethod(one.move_to, start_one), ApplyMethod(five.move_to, start_five), FadeIn(dots[7]))


class Cycle:
    def __init__(self, circle, dots, labels):
        self.circle = circle
        self.dots = [dot for dot in dots]
        self.labels = [label for label in labels]

        self.length = len(self.dots)

        self.arrows = []

        self.dot_group = VGroup(*self.dots)
        self.label_group = VGroup(*self.labels)
        self.dot_and_label_group = VGroup(*self.dots, *self.labels)
        self.BADDONTKEEP = VGroup(self.circle)

    def add_label_updaters(self):
        for dot, label in zip(self.dots, self.labels):
            label.add_updater(
                lambda l, dot=dot, label=label: l.move_to(
                    (dot.get_center() - self.circle.get_center()) * 1.15 + self.circle.get_center()
                )
            )

    def remove_label_updaters(self):
        for label in self.labels:
            label.clear_updaters()

    def make_arrows_normal(self):
        if len(self.arrows) > 0:
            for arrow in self.arrows:
                arrow.clear_updaters()
        else:
            self.arrows = [
                make_arrow_between(
                    self.dots[index], self.dots[(index + 1) % self.length]
                ) for index in range(self.length)
            ]

    def make_arrows_sticky(self):
        if len(self.arrows) > 0:
            for index, arrow in enumerate(self.arrows):
                arrow_add_sticky_updater(arrow, self.dots[index], self.dots[(index + 1) % self.length])
        else:
            self.arrows = [
                make_sticky_arrow_between(
                    self.dots[index], self.dots[(index + 1) % self.length]
                ) for index in range(self.length)
            ]

    def change_center(self, new_center):
        old_center = self.circle.get_center()
        self.circle.move_to(new_center)
        return ApplyMethod(self.dot_and_label_group.shift, new_center - old_center)

    def untangle(self):
        methods = []
        for index, dot in enumerate(self.dots):
            methods.append(ApplyMethod(dot.move_to, self.circle.point_at_angle(index * TAU / self.length)))
        return methods

    def permute(self):
        transforms = []
        fade_out_labels = [FadeOut(label) for label in self.labels]
        fade_in_labels = [FadeIn(label) for label in self.labels]

        for index in range(self.length):
            transforms.append(
                Transform(
                    self.dots[index - 1], self.dots[index]
                )
            )

        return transforms, fade_out_labels, fade_in_labels

    def scale(self, scale_factor):
        pass


class BringingInto2Circles(ZoomedScene, MovingCameraScene):
    def permute(self, dots, labels, permutations, *cycles):
        transforms = []
        fade_out_labels = [FadeOut(label) for label in labels]
        fade_in_labels = [FadeIn(label) for label in labels]

        for permutation in permutations:
            for index in range(len(permutation) - 1):
                transforms.append(
                    Transform(
                        dots[permutation[index]], dots[permutation[index + 1]]
                    )
                )

        for cycle in cycles:
            cycle_transforms, fade_out_cycle_labels, fade_in_cycle_labels = cycle.permute()
            transforms.extend(cycle_transforms)
            fade_out_labels.extend(fade_out_cycle_labels)
            fade_in_labels.extend(fade_in_cycle_labels)

        self.play(*fade_out_labels)
        self.play(*transforms, run_time=3)

        for label, dot in zip(labels, dots):
            label.move_to(dot.get_center() * 1.1)

        self.play(*fade_in_labels)

    def construct(self):
        circle = Circle(radius=3, color=RED)

        num_points = 20

        dots = []
        labels = []

        for c, angle in enumerate(np.linspace(0, TAU, num_points, endpoint=False)):
            p = circle.point_at_angle(angle)
            d = Dot(point=p)
            dots.append(d)
            label = Integer(number=c + 1).move_to(p * 1.15).scale(0.5)
            labels.append(label)

        for c in range(1, 7, 1):
            labels[-c].set_value(1001 - c)

        # Hides the 14th dot and puts a '...' in its place
        dot_loc = dots[13].get_center()
        dots[13].set_color(BLACK)
        labels[13].set_color(BLACK)

        angle = Line(start=dots[12].get_center(), end=dots[14].get_center()).get_angle()
        etc = Text('...').move_to(dot_loc).rotate(angle)

        self.play(*[FadeIn(dot) for dot in dots], *[FadeIn(label) for label in labels], FadeIn(etc))
        self.wait()

        arrows = []

        cycle1order = [0, 4, 10, 16, 7, 0]
        cycle2order = [1, 18, 9, 1]

        for index in range(1, len(cycle1order)):
            arrows.append(make_arrow_between(dots[cycle1order[index - 1]], dots[cycle1order[index]]))
        for index in range(1, len(cycle2order)):
            arrows.append(make_arrow_between(dots[cycle2order[index - 1]], dots[cycle2order[index]]))

        for arrow in arrows:
            self.play(Create(arrow), run_time=0.5)

        self.wait()

        self.play(self.camera.frame.animate.scale(2))
        self.play(self.camera.frame.animate.shift(DOWN * 4))

        cycle1 = Cycle(
            circle=circle.copy(),
            dots=[dots[index].copy() for index in [0, 4, 10, 16, 7]],
            labels=[labels[index].copy() for index in [0, 4, 10, 16, 7]]
        )

        cycle2 = Cycle(
            circle=circle.copy(),
            dots=[dots[index].copy() for index in [1, 18, 9]],
            labels=[labels[index].copy() for index in [1, 18, 9]]
        )

        cycle1.make_arrows_sticky()
        cycle2.make_arrows_sticky()

        self.add(*cycle1.dots, *cycle1.labels, *cycle1.arrows)
        self.add(*cycle2.dots, *cycle2.labels, *cycle2.arrows)

        self.play(cycle1.change_center(6 * LEFT + 8 * DOWN), cycle2.change_center(6 * RIGHT + 8 * DOWN))

        cycle1.add_label_updaters()
        cycle2.add_label_updaters()

        # untangles the dots and arrows
        self.play(*cycle1.untangle(), *cycle2.untangle())

        permutations = [
            [0, 4, 10, 16, 7, 0],
            [1, 9, 18, 1],
            [2, 6, 14, 5, 19, 2],
            [3, 11, 15, 17, 3],
            [8, 12, 8],
        ]

        cycle1.make_arrows_normal()
        cycle2.make_arrows_normal()

        self.permute(dots, labels, permutations, cycle1, cycle2)
        self.permute(dots, labels, permutations, cycle1, cycle2)

        cycle1.make_arrows_sticky()
        self.permute(dots, labels, permutations, cycle1, cycle2)


class BreakingIntoCycles(ZoomedScene, MovingCameraScene):
    def permute(self, *cycles):
        transforms = []
        fade_out_labels = []
        fade_in_labels = []
        for cycle in cycles:
            cycle_transforms, fade_out_cycle_labels, fade_in_cycle_labels = cycle.permute()
            transforms.extend(cycle_transforms)
            fade_out_labels.extend(fade_out_cycle_labels)
            fade_in_labels.extend(fade_in_cycle_labels)

        self.play(*fade_out_labels)
        self.play(*transforms, run_time=2)
        self.play(*fade_in_labels)

    def construct(self):
        circle = Circle(radius=3, color=RED)

        num_points = 20

        dots = []
        labels = []

        for c, angle in enumerate(np.linspace(0, TAU, num_points, endpoint=False)):
            p = circle.point_at_angle(angle)
            d = Dot(point=p)
            dots.append(d)
            label = Integer(number=c + 1).move_to(p * 1.15).scale(0.5)
            labels.append(label)

        for c in range(1, 7, 1):
            labels[-c].set_value(1001 - c)

        # Hides the 14th dot and puts a '...' in its place
        dot_loc = dots[13].get_center()
        dots[13].set_color(BLACK)
        labels[13].set_color(BLACK)

        angle = Line(start=dots[12].get_center(), end=dots[14].get_center()).get_angle()
        etc = Text('...').move_to(dot_loc).rotate(angle)

        self.play(*[FadeIn(dot) for dot in dots], *[FadeIn(label) for label in labels], FadeIn(etc))
        self.wait()

        cycle1order = [0, 4, 10, 16, 7]
        cycle2order = [3, 1, 8, 19]
        cyclemorder = [14, 5, 12, 11, 15, 18, 6, 9]

        cycle1 = Cycle(
            circle=circle.copy(),
            dots=[dots[index] for index in cycle1order],
            labels=[labels[index] for index in cycle1order]
        )
        cycle2 = Cycle(
            circle=circle.copy(),
            dots=[dots[index] for index in cycle2order],
            labels=[labels[index] for index in cycle2order]
        )
        cyclem = Cycle(
            circle=circle.copy(),
            dots=[dots[index] for index in cyclemorder],
            labels=[labels[index] for index in cyclemorder]
        )

        cycle1.make_arrows_sticky()
        cycle2.make_arrows_sticky()
        cyclem.make_arrows_sticky()

        self.play(self.camera.frame.animate.scale(2))

        arrows = []
        arrows.extend(cycle1.arrows)
        arrows.extend(cycle2.arrows)
        arrows.extend(cyclem.arrows)

        self.add(*cycle1.dots, *cycle1.labels)
        self.add(*cycle2.dots, *cycle2.labels)
        self.add(*cyclem.dots, *cyclem.labels)

        self.play(*[FadeIn(arrow) for arrow in arrows])

        mystical_dot = Dot(10/3 * RIGHT).set_color(BLACK)
        mystical_etc = Text('...').move_to(10/3 * RIGHT)

        self.play(
            cycle1.change_center(10 * LEFT),
            cycle2.change_center(7/3 * LEFT),
            cyclem.change_center(10 * RIGHT),
            Transform(dots[2], mystical_dot),
            Transform(dots[17], mystical_dot),
            Transform(labels[2], mystical_dot),
            Transform(labels[17], mystical_dot),
            Transform(etc, mystical_etc)
        )
        self.wait()

        cycle1.add_label_updaters()
        cycle2.add_label_updaters()
        cyclem.add_label_updaters()

        self.play(*cycle1.untangle(), *cycle2.untangle(), *cyclem.untangle())

        cycle1.make_arrows_normal()
        cycle2.make_arrows_normal()
        cyclem.make_arrows_normal()

        self.permute(cycle1, cycle2, cyclem)
        self.permute(cycle1, cycle2, cyclem)
        self.permute(cycle1, cycle2, cyclem)
