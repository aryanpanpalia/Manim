from abc import ABC

from manim import *


class CustomArrowTip(ArrowTip, Triangle, ABC):
	def __init__(self, **kwargs):
		Triangle.__init__(self)
		self.scale(0.05)
		self.set_color(WHITE)
		self.set_fill(color=WHITE, opacity=0)


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

	def show_arrows(self, run_time=1, lag_ratio=0):
		return [FadeIn(arrow, run_time=run_time, lag_ratio=lag_ratio) for arrow in self.arrows]

	def hide_arrows(self, run_time=1, lag_ratio=0):
		return [FadeOut(arrow, run_time=run_time, lag_ratio=lag_ratio) for arrow in self.arrows]

	def show_labels(self, run_time=1, lag_ratio=0):
		return [FadeIn(label, run_time=run_time, lag_ratio=lag_ratio) for label in self.labels]

	def hide_labels(self, run_time=1, lag_ratio=0):
		return [FadeOut(label, run_time=run_time, lag_ratio=lag_ratio) for label in self.labels]

	def scale(self, scale_factor):
		pass


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


def approx(array1, array2):
	for element1, element2 in zip(array1, array2):
		if not (element1 - 0.05 < element2 < element1 + 0.05):
			return False
	return True


class Logo(Scene):
	def construct(self):
		num_integrals = 5

		rate_func = rate_functions.ease_in_out_cubic
		channel_name = MathTex(*[r'\text{The Geometers}']).shift(2.6 * DOWN)
		initial_circ = Circle(radius=0.037, fill_color=BLUE, fill_opacity=1, stroke_color=BLUE, stroke_width=4)

		circ_list = [initial_circ]
		for current_radius in np.arange(0.037 * 2, 1, 0.037):
			circ_list.append(
				Circle(
					radius=current_radius,
					stroke_width=4,
					stroke_color=BLUE,
					stroke_opacity=np.exp(-6 * current_radius ** 2)
				)
			)
		circles = VGroup(initial_circ, *circ_list)

		integral_list = [MathTex(r'\int').rotate(PI * index / num_integrals).scale(3) for index in range(num_integrals)]
		integrals = VGroup(*integral_list)

		delay = 0.75
		hacking_delay = Rotate(Square(1).set_opacity(0), run_time=delay)
		integral_fade_ins = [hacking_delay]

		def update_sector(mob, alpha):
			mob.become(mob.set_opacity(interpolate(0, 1, alpha)))

		run_time = 2
		for integral in integrals[1:]:
			integral_fade_ins.append(
				UpdateFromAlphaFunc(
					integral, update_sector, rate_func=rate_func, run_time=run_time - 2 * delay / (num_integrals - 1)
				)
			)

		integral_fade_ins.append(hacking_delay)
		fade_in_group = AnimationGroup(*integral_fade_ins, lag_ratio=1)

		self.play(Write(integrals[0]), run_time=run_time)
		self.play(
			Rotate(integrals, angle=np.round(2 * np.pi, 5), run_time=4 * run_time, rate_func=rate_func),
			fade_in_group,
			Rotate(integrals[0], angle=np.round(2 * np.pi, 5), run_time=4 * run_time, rate_func=rate_func),
			FadeIn(circles, run_time=4 * run_time),
			Write(channel_name, run_time=4 * run_time)
		)
		self.wait()
		self.play(
			FadeOut(circles)
		)
		self.play(FadeOut(integrals), FadeOut(channel_name))


class WriteQuestionToScreen(Scene):
	def construct(self):
		text_part1 = MathTex(
			r"\text{Find the least positive integer } n"
			r"\text{ for which there exists a permutation } f \text{ on } n \text{ objects}"
		).scale(0.6).shift(UP * 0.5)
		text_part2 = MathTex(
			r"\text{ such that } f^{1000} \text{ is the identity function}"
			r"\text{ and } 1000 \text{ is the least positive integer for which this holds.}"
		).scale(0.6)

		self.play(Write(text_part1))
		self.play(Write(text_part2))
		self.wait(17)
		self.play(Unwrite(text_part1), Unwrite(text_part2))
		self.wait()


class ExplainingPermutations(Scene):
	def permute(self, dots, permutation: dict):
		transforms = []
		create_arcs = []
		fadeout_arcs = []

		for key, value in permutation.items():
			this = dots[key]
			other = dots[value]
			transforms.append(Transform(this, other, path_arc=PI))

			halfdist = np.linalg.norm(np.array(this.get_center()) - np.array(other.get_center())) / 2
			center = ArcBetweenPoints(
				this.get_center(), other.get_center(), radius=halfdist, stroke_opacity=0.5
			).get_arc_center()

			arrowtip = Triangle().scale(0.05).move_to(center)
			if this.get_x() > other.get_x():
				arc = Arc(start_angle=PI + 0.3, angle=PI - 0.6, arc_center=center, radius=-halfdist)
				arrowtip.shift(UP * halfdist).rotate(3 * PI / 6).set_fill(WHITE).set_color(WHITE)
			else:
				arc = Arc(start_angle=PI + 0.3, angle=PI - 0.6, arc_center=center, radius=halfdist)
				arrowtip.shift(DOWN * halfdist).rotate(PI / 6).set_fill(WHITE).set_color(WHITE)

			arc.add(arrowtip)
			create_arcs.append(Write(arc))
			fadeout_arcs.append(FadeOut(arc))

		self.play(*create_arcs)
		self.play(*transforms, *fadeout_arcs)

	def permute_no_arrows(self, dots, permutation: dict, run_time=1.0):
		transforms = []

		for key, value in permutation.items():
			this = dots[key]
			other = dots[value]
			transforms.append(Transform(this, other, path_arc=PI, run_time=run_time))

		return transforms

	def construct(self):
		dots = [Dot(RIGHT * mult) for mult in range(-2, 3)]
		labels = [Integer(num + 1).scale(0.5).next_to(dot, DOWN) for num, dot in enumerate(dots)]

		dots_copy = [dot.copy() for dot in dots]
		labels_copy = [label.copy() for label in labels]

		group_of_dots = VGroup(*dots)
		group_of_labels = VGroup(*labels)
		group_of_copy_dots = VGroup(*dots_copy)
		group_of_labels_copy = VGroup(*labels_copy)

		for dot, label in zip(dots, labels):
			label.add_updater(lambda l, dot=dot, label=label: l.next_to(dot, DOWN))

		permutation = {
			0: 2,
			1: 4,
			2: 0,
			3: 1,
			4: 3
		}

		inverse = {v: k for k, v in permutation.items()}

		self.play(*[FadeIn(dot) for dot in dots], *[Write(label) for label in labels], run_time=0.5)
		self.wait(3)
		self.permute(dots, permutation)
		self.wait(2)
		self.play(*self.permute_no_arrows(dots, inverse))
		self.wait()

		self.add(*labels_copy, *dots_copy)
		self.wait(1)

		self.play(
			ApplyMethod(group_of_dots.shift, DOWN),
			ApplyMethod(group_of_copy_dots.shift, UP),
			ApplyMethod(group_of_labels_copy.shift, UP * 2),
		)

		self.play(ApplyMethod(group_of_copy_dots.set_fill, GRAY), ApplyMethod(group_of_labels_copy.set_fill, GRAY))

		self.permute(dots, permutation)
		scale_factor_table = 0.75
		fof3 = MathTex("f(3)=1").move_to(5.75 * LEFT + 3.25 * UP).scale(scale_factor_table)
		fof4 = MathTex("f(4)=2").move_to(5.75 * LEFT + 2.5 * UP).scale(scale_factor_table)
		fof1 = MathTex("f(1)=3").move_to(5.75 * LEFT + 1.75 * UP).scale(scale_factor_table)
		fof5 = MathTex("f(5)=4").move_to(5.75 * LEFT + 1 * UP).scale(scale_factor_table)
		fof2 = MathTex("f(2)=5").move_to(5.75 * LEFT + 0.25 * UP).scale(scale_factor_table)

		self.wait(4)
		self.play(Write(fof3))
		self.wait(4)
		self.play(Write(fof4))
		self.wait(1)
		self.play(Write(fof1))
		self.wait(scale_factor_table)
		self.play(Write(fof5, run_time=1))
		self.wait(scale_factor_table)
		self.play(Write(fof2, run_time=1))
		self.wait(10)

		comp_notation = [
			Transform(fof1, MathTex(r"(f \circ f)(1) = 1").move_to(fof1.get_center()).scale(scale_factor_table)),
			Transform(fof2, MathTex(r"(f \circ f)(2) = 4").move_to(fof2.get_center()).scale(scale_factor_table)),
			Transform(fof3, MathTex(r"(f \circ f)(3) = 3").move_to(fof3.get_center()).scale(scale_factor_table)),
			Transform(fof4, MathTex(r"(f \circ f)(4) = 5").move_to(fof4.get_center()).scale(scale_factor_table)),
			Transform(fof5, MathTex(r"(f \circ f)(5) = 2").move_to(fof5.get_center()).scale(scale_factor_table)),
		]
		func_exp_notation = [
			Transform(fof1, MathTex(r"f^2(1) = 1").move_to(fof1.get_center()).scale(scale_factor_table)),
			Transform(fof2, MathTex(r"f^2(2) = 4").move_to(fof2.get_center()).scale(scale_factor_table)),
			Transform(fof3, MathTex(r"f^2(3) = 3").move_to(fof3.get_center()).scale(scale_factor_table)),
			Transform(fof4, MathTex(r"f^2(4) = 5").move_to(fof4.get_center()).scale(scale_factor_table)),
			Transform(fof5, MathTex(r"f^2(5) = 2").move_to(fof5.get_center()).scale(scale_factor_table)),
		]

		self.play(*self.permute_no_arrows(dots, permutation, run_time=1.1), *comp_notation)
		self.play(*func_exp_notation)
		self.wait()

		func_exp_notation = [
			Transform(fof1, MathTex(r"f^3(1) = 3").move_to(fof1.get_center()).scale(scale_factor_table)),
			Transform(fof2, MathTex(r"f^3(2) = 2").move_to(fof2.get_center()).scale(scale_factor_table)),
			Transform(fof3, MathTex(r"f^3(3) = 1").move_to(fof3.get_center()).scale(scale_factor_table)),
			Transform(fof4, MathTex(r"f^3(4) = 4").move_to(fof4.get_center()).scale(scale_factor_table)),
			Transform(fof5, MathTex(r"f^3(5) = 5").move_to(fof5.get_center()).scale(scale_factor_table)),
		]

		self.play(*self.permute_no_arrows(dots, permutation, run_time=1.1), *func_exp_notation)

		func_exp_notation = [
			Transform(fof1, MathTex(r"f^4(1) = 1").move_to(fof1.get_center()).scale(scale_factor_table)),
			Transform(fof2, MathTex(r"f^4(2) = 5").move_to(fof2.get_center()).scale(scale_factor_table)),
			Transform(fof3, MathTex(r"f^4(3) = 3").move_to(fof3.get_center()).scale(scale_factor_table)),
			Transform(fof4, MathTex(r"f^4(4) = 2").move_to(fof4.get_center()).scale(scale_factor_table)),
			Transform(fof5, MathTex(r"f^4(5) = 4").move_to(fof5.get_center()).scale(scale_factor_table)),
		]

		self.play(*self.permute_no_arrows(dots, permutation, run_time=1.1), *func_exp_notation)

		func_exp_notation = [
			Transform(fof1, MathTex(r"f^5(1) = 3").move_to(fof1.get_center()).scale(scale_factor_table)),
			Transform(fof2, MathTex(r"f^5(2) = 4").move_to(fof2.get_center()).scale(scale_factor_table)),
			Transform(fof3, MathTex(r"f^5(3) = 1").move_to(fof3.get_center()).scale(scale_factor_table)),
			Transform(fof4, MathTex(r"f^5(4) = 5").move_to(fof4.get_center()).scale(scale_factor_table)),
			Transform(fof5, MathTex(r"f^5(5) = 2").move_to(fof5.get_center()).scale(scale_factor_table)),
		]

		self.play(*self.permute_no_arrows(dots, permutation, run_time=1.1), *func_exp_notation)

		func_exp_notation = [
			Transform(fof1, MathTex(r"f^6(1) = 1").move_to(fof1.get_center()).scale(scale_factor_table)),
			Transform(fof2, MathTex(r"f^6(2) = 2").move_to(fof2.get_center()).scale(scale_factor_table)),
			Transform(fof3, MathTex(r"f^6(3) = 3").move_to(fof3.get_center()).scale(scale_factor_table)),
			Transform(fof4, MathTex(r"f^6(4) = 4").move_to(fof4.get_center()).scale(scale_factor_table)),
			Transform(fof5, MathTex(r"f^6(5) = 5").move_to(fof5.get_center()).scale(scale_factor_table)),
		]

		self.play(*self.permute_no_arrows(dots, permutation, run_time=1.1), *func_exp_notation)

		self.play(FadeOut(group_of_copy_dots), FadeOut(group_of_labels_copy))
		self.play(
			ApplyMethod(group_of_dots.shift, UP),
		)
		self.wait(12)

		text = MathTex(r"f^6 = \text{Identity}").shift(UP * 2)
		self.play(Write(text))

		self.wait(5)
		circle = Circle(radius=3)

		new_dot1 = Dot(circle.point_at_angle(TAU / 4 + 2 * TAU / 5))
		new_dot2 = Dot(circle.point_at_angle(TAU / 4 + TAU / 5))
		new_dot3 = Dot(circle.point_at_angle(TAU / 4))
		new_dot5 = Dot(circle.point_at_angle(TAU / 4 - TAU / 5))
		new_dot4 = Dot(circle.point_at_angle(TAU / 4 + 3 * TAU / 5))

		self.play(
			Transform(dots[2], new_dot1),
			Transform(dots[1], new_dot2),
			Transform(dots[0], new_dot3),
			Transform(dots[3], new_dot4),
			Transform(dots[4], new_dot5),
			FadeOut(fof1), FadeOut(fof2), FadeOut(fof3), FadeOut(fof4), FadeOut(fof5), FadeOut(text),
		)
		self.wait(12)
		self.play(FadeOut(group_of_dots), FadeOut(group_of_labels))


class RotationPermutationWith1000(Scene):
	num_permutes = 0
	counter = Integer(0).scale(0.5).move_to(RIGHT * 6.5 + UP * 3.5)

	def rotate_permutation(self, dots, labels, dot_loc, label_loc, fadein_arrows=True, fadeout_arrows=True, foa=None):
		transforms = []
		fade_in_arrows = []
		fade_out_arrows = []
		for index in range(20):
			this_dot = dots[index - 1]
			next_dot = dots[index]
			this_label = labels[index - 1]
			next_label = labels[index]

			transforms.append(Transform(this_dot, next_dot))

			if approx(this_label.get_center(), label_loc):
				this_label.set_value(next_label.get_value() - 1)

			target_label = this_label.copy().move_to(next_label.get_center())

			if approx(next_label.get_center(), label_loc):
				target_label.set_color(BLACK)
			else:
				target_label.set_color(WHITE)

			transforms.append(Transform(this_label, target_label))

			if not (approx(next_dot.get_center(), dot_loc) or approx(this_dot.get_center(), dot_loc)):
				arrow = make_arrow_between(this_dot, next_dot)
				fade_in_arrows.append(FadeIn(arrow))
				fade_out_arrows.append(FadeOut(arrow))

		if fadein_arrows:
			self.play(*fade_in_arrows)

		self.num_permutes += 1
		self.play(*transforms, ApplyMethod(self.counter.set_value, self.num_permutes))

		if fadeout_arrows:
			if foa is None:
				self.play(*fade_out_arrows)
			else:
				self.play(*fade_out_arrows, *foa)

		return fade_out_arrows

	def construct(self):
		circle = Circle(radius=3, color=BLACK)

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

		self.play(*[FadeIn(dot) for dot in dots], *[FadeIn(label) for label in labels], FadeIn(etc),
		          FadeIn(self.counter))

		foa = self.rotate_permutation(dots, labels, dot_loc, label_loc, fadein_arrows=True, fadeout_arrows=False)
		self.wait(0.25)

		for _ in range(12):
			self.rotate_permutation(dots, labels, dot_loc, label_loc, fadein_arrows=False, fadeout_arrows=False)
			self.wait(0.5)

		self.rotate_permutation(dots, labels, dot_loc, label_loc, fadein_arrows=False, fadeout_arrows=True, foa=foa)
		self.wait(1.75)

		self.play(*[FadeOut(dot) for dot in dots], *[FadeOut(label) for label in labels], FadeOut(etc),
		          FadeOut(self.counter))


class RotationPermutationWith4(Scene):
	num_permutes = 0
	counter = Integer(0).scale(0.5).move_to(RIGHT * 6.5 + UP * 3.5)

	def rotate_permutation(self, dots, labels, fadein_arrows=True, fadeout_arrows=True, foa=None):
		transforms = []
		fade_in_arrows = []
		fade_out_arrows = []
		for index in range(4):
			this_dot = dots[index - 1]
			next_dot = dots[index]
			this_label = labels[index - 1]
			next_label = labels[index]

			transforms.append(Transform(this_dot, next_dot))

			target_label = this_label.copy().move_to(next_label.get_center())
			target_label.set_color(WHITE)

			transforms.append(Transform(this_label, target_label))

			arrow = make_arrow_between(this_dot, next_dot)
			fade_in_arrows.append(FadeIn(arrow))
			fade_out_arrows.append(FadeOut(arrow))

		if fadein_arrows:
			self.play(*fade_in_arrows)

		self.num_permutes += 1
		self.play(*transforms, ApplyMethod(self.counter.set_value, self.num_permutes))

		if fadeout_arrows:
			if foa is None:
				self.play(*fade_out_arrows)
			else:
				self.play(*fade_out_arrows, *foa)

		return fade_out_arrows

	def construct(self):
		circle = Circle(radius=3, color=BLACK)

		num_points = 4

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

		self.play(*[FadeIn(dot) for dot in dots], *[FadeIn(label) for label in labels], FadeIn(self.counter))

		foa = self.rotate_permutation(dots, labels, fadein_arrows=True, fadeout_arrows=False)
		self.wait(0.25)

		for _ in range(7):
			self.rotate_permutation(dots, labels, fadein_arrows=False, fadeout_arrows=False)
			self.wait(0.5)

		self.rotate_permutation(dots, labels, fadein_arrows=False, fadeout_arrows=True, foa=foa)
		self.wait(0.25)

		self.play(*[FadeOut(dot) for dot in dots], *[FadeOut(label) for label in labels], FadeOut(self.counter))


class BringingInto2Circles(ZoomedScene, MovingCameraScene):
	num_permutes = 0
	counter = Integer(0).scale(1).move_to(RIGHT * 13 + UP * 3)

	def permute1(self, dots, labels, permutations):
		transforms = []
		write_arrows = []
		fade_out_arrows = []
		fade_out_labels = [FadeOut(label) for label in labels]

		for permutation in permutations:
			for index in range(len(permutation) - 1):
				transforms.append(
					Transform(
						dots[permutation[index]], dots[permutation[index + 1]]
					)
				)
				arrow = make_arrow_between(dots[permutation[index]], dots[permutation[index + 1]])
				write_arrows.append(Write(arrow))
				fade_out_arrows.append(FadeOut(arrow))

		self.play(*write_arrows, run_time=1)
		self.play(*fade_out_labels, run_time=0.5)
		self.play(*transforms, *fade_out_arrows, run_time=2)

		fade_in_labels = [FadeIn(label) for label in labels]
		for label, dot in zip(labels, dots):
			label.move_to(dot.get_center() * 1.15)

		self.play(*fade_in_labels)

	def permute2(self, dots, labels, permutations, *cycles):
		speed_ratio = 1.5
		transforms = []
		fade_out_labels = [FadeOut(label) for label in labels]
		fade_in_labels = [FadeIn(label) for label in labels]

		for permutation in permutations:
			for index in range(len(permutation) - 1):
				transforms.append(Transform(dots[permutation[index]], dots[permutation[index + 1]]))

		for cycle in cycles:
			for index in range(cycle.length):
				transforms.append(Transform(cycle.dots[index - 1], cycle.dots[index]))

		self.play(*fade_out_labels, run_time=0.5 / speed_ratio)

		self.num_permutes += 1
		self.play(*transforms, ApplyMethod(self.counter.set_value, self.num_permutes), run_time=1.5 / speed_ratio)

		for label, dot in zip(labels, dots):
			label.move_to(dot.get_center() * 1.15)

		self.play(*fade_in_labels, run_time=0.5 / speed_ratio)

	def unpermute(self, dots, labels, permutations):
		transforms = []
		fade_out_labels = [FadeOut(label) for label in labels]

		for permutation in permutations:
			for index in range(len(permutation) - 1):
				transforms.append(
					Transform(
						dots[permutation[index + 1]], dots[permutation[index]]
					)
				)

		self.play(*fade_out_labels, run_time=0.5)
		self.play(*transforms, run_time=1)

		fade_in_labels = [FadeIn(label) for label in labels]
		for label, dot in zip(labels, dots):
			label.move_to(dot.get_center() * 1.15)

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
			label = MathTex(f"{c + 1}").move_to(p * 1.15).scale(0.5)
			labels.append(label)

		labels[-1] = MathTex(f"n").move_to(labels[-1].get_center()).scale(0.5)
		for c in range(2, 7, 1):
			labels[-c] = MathTex(f"n - {c - 1}").move_to(labels[-c].get_center()).scale(0.5)

		# Hides the 14th dot and puts a '...' in its place
		dot_loc = dots[13].get_center()
		dots[13].set_color(BLACK)
		labels[13].set_color(BLACK)

		angle = Line(start=dots[12].get_center(), end=dots[14].get_center()).get_angle()
		etc = Text('...').move_to(dot_loc).rotate(angle)

		self.play(*[FadeIn(dot) for dot in dots], *[FadeIn(label) for label in labels], FadeIn(etc))
		self.wait(2)

		permutations = [
			[0, 4, 10, 16, 7, 0],
			[3, 9, 18, 14, 3],
			[11, 12, 8, 17, 19, 6, 5, 15, 1, 2, 11]
		]

		self.permute1(dots, labels, permutations)
		self.wait(0.5)
		self.unpermute(dots, labels, permutations)

		darken_dots = []
		lighten_dots = []
		for dot in dots[1:13]:
			darken_dots.append(ApplyMethod(dot.set_color, GRAY_E))
			lighten_dots.append(ApplyMethod(dot.set_color, WHITE))

		for dot in dots[14:]:
			darken_dots.append(ApplyMethod(dot.set_color, GRAY_E))
			lighten_dots.append(ApplyMethod(dot.set_color, WHITE))

		self.play(*darken_dots, ApplyMethod(etc.set_color, GRAY_E))
		self.wait()

		one = dots[0]
		start_one = one.get_center()
		self.play(ApplyMethod(one.move_to, dots[4]), FadeOut(dots[4]))
		self.play(ApplyMethod(one.move_to, dots[10]), FadeIn(dots[4]), FadeOut(dots[10]))
		self.play(ApplyMethod(one.move_to, dots[16]), FadeIn(dots[10]), FadeOut(dots[16]))
		self.play(ApplyMethod(one.move_to, dots[7]), FadeIn(dots[16]), FadeOut(dots[7]))
		self.play(ApplyMethod(one.move_to, start_one), FadeIn(dots[7]))
		self.wait()
		self.play(*lighten_dots, ApplyMethod(etc.set_color, WHITE))
		self.wait(17)

		# ---------------------------------------------------------------------------------------------------------

		self.play(ApplyMethod(dots[3].set_color, RED, run_time=0.5))
		self.play(ApplyMethod(dots[11].set_color, BLUE_E, run_time=0.5))

		cycle1order = permutations[1]
		cycle2order = permutations[2]
		cycle1arrows = []
		cycle2arrows = []

		for index in range(1, len(cycle1order)):
			cycle1arrows.append(make_arrow_between(dots[cycle1order[index - 1]], dots[cycle1order[index]]))
		for index in range(1, len(cycle2order)):
			cycle2arrows.append(make_arrow_between(dots[cycle2order[index - 1]], dots[cycle2order[index]]))

		self.wait()
		self.play(
			*[Write(arrow) for arrow in cycle1arrows],
			*[ApplyMethod(dots[index].set_color, RED) for index in permutations[1][1:-1]],
			run_time=0.75
		)
		self.play(
			*[Write(arrow) for arrow in cycle2arrows],
			*[ApplyMethod(dots[index].set_color, BLUE_E) for index in permutations[2][1:-1]],
			run_time=0.75
		)

		self.wait(2)

		self.play(self.camera.frame.animate.scale(2))
		self.play(self.camera.frame.animate.shift(DOWN * 4))

		cycle1 = Cycle(
			circle=circle.copy(),
			dots=[dots[index].copy() for index in cycle1order[:-1]],
			labels=[labels[index].copy() for index in cycle1order[:-1]]
		)

		cycle2 = Cycle(
			circle=circle.copy(),
			dots=[dots[index].copy() for index in cycle2order[:-1]],
			labels=[labels[index].copy() for index in cycle2order[:-1]]
		)

		cycle1.make_arrows_sticky()
		cycle2.make_arrows_sticky()

		self.add(*cycle1.dots, *cycle1.labels, *cycle1.arrows)
		self.add(*cycle2.dots, *cycle2.labels, *cycle2.arrows)
		self.play(
			cycle1.change_center(6 * LEFT + 8 * DOWN), cycle2.change_center(6 * RIGHT + 8 * DOWN),
			FadeIn(self.counter)
		)

		cycle1.add_label_updaters()
		cycle2.add_label_updaters()

		# untangles the dots and arrows
		self.wait(2.5)
		self.play(*cycle1.untangle(), *cycle2.untangle())

		cycle1.make_arrows_normal()
		cycle2.make_arrows_normal()

		self.wait()

		for _ in range(20):
			self.permute2(dots, labels, permutations, cycle1, cycle2)

		self.wait()
		self.play(
			*[FadeOut(dot) for dot in dots], *[FadeOut(label) for label in labels],
			*[FadeOut(dot) for dot in cycle1.dots], *[FadeOut(label) for label in cycle1.labels],
			*[FadeOut(dot) for dot in cycle2.dots], *[FadeOut(label) for label in cycle2.labels],
			*[FadeOut(arrow) for arrow in cycle1arrows], *[FadeOut(arrow) for arrow in cycle2arrows],
			*cycle1.hide_arrows(), *cycle2.hide_arrows(),
			FadeOut(self.counter), FadeOut(etc)
		)


class BreakingCircleIntoCycles(ZoomedScene, MovingCameraScene):
	num_permutes = 0
	counter = Integer(0).scale(1).move_to(RIGHT * 13 + UP * 7)

	def permute(self, *cycles):
		transforms = []
		for cycle in cycles:
			for index in range(cycle.length):
				transforms.append(Transform(cycle.dots[index - 1], cycle.dots[index], run_time=2))

		self.num_permutes += 1
		self.play(*transforms, ApplyMethod(self.counter.set_value, self.num_permutes))

	def construct(self):
		circle = Circle(radius=3)

		num_points = 20

		dots = []
		labels = []

		for c, angle in enumerate(np.linspace(0, TAU, num_points, endpoint=False)):
			p = circle.point_at_angle(angle)
			d = Dot(point=p)
			dots.append(d)
			label = MathTex(f"{c + 1}").move_to(p * 1.15).scale(0.5)
			labels.append(label)

		labels[-1] = MathTex(f"n").move_to(labels[-1].get_center()).scale(0.5)
		for c in range(2, 7, 1):
			labels[-c] = MathTex(f"n - {c - 1}").move_to(labels[-c].get_center()).scale(0.5)

		# Hides the 14th dot and puts a '...' in its place
		dot_loc = dots[13].get_center()
		dots[13].set_color(BLACK)
		labels[13].set_color(BLACK)

		angle = Line(start=dots[12].get_center(), end=dots[14].get_center()).get_angle()
		etc = Text('...').move_to(dot_loc).rotate(angle)

		self.play(*[FadeIn(dot) for dot in dots], *[FadeIn(label) for label in labels], FadeIn(etc))
		self.wait(2)

		permutations = [
			[0, 4, 10, 16, 7, 0],
			[3, 9, 18, 14, 3],
			[11, 12, 8, 17, 19, 6, 5, 15, 1, 2, 11]
		]

		cycle1order = permutations[1]
		cycle2order = permutations[2]
		cycleMorder = permutations[0]

		cycle1 = Cycle(
			circle=circle.copy(),
			dots=[dots[index] for index in cycle1order[:-1]],
			labels=[labels[index] for index in cycle1order[:-1]]
		)

		cycle2 = Cycle(
			circle=circle.copy(),
			dots=[dots[index] for index in cycle2order[:-1]],
			labels=[labels[index] for index in cycle2order[:-1]]
		)

		cycleM = Cycle(
			circle=circle.copy(),
			dots=[dots[index] for index in cycleMorder[:-1]],
			labels=[labels[index] for index in cycleMorder[:-1]]
		)

		cycle1.make_arrows_sticky()
		cycle2.make_arrows_sticky()
		cycleM.make_arrows_sticky()

		self.play(self.camera.frame.animate.scale(2))

		self.add(*cycle1.dots, *cycle1.labels)
		self.add(*cycle2.dots, *cycle2.labels)
		self.add(*cycleM.dots, *cycleM.labels)

		self.play(
			*cycle1.show_arrows(), *cycle2.show_arrows(), *cycleM.show_arrows()
		)
		# total screen width at this point is 256/9
		left_end = LEFT * (128 / 9)
		right_end = RIGHT * (128 / 9)
		mystic_space = 1.5
		buffer = ((256 / 9) - (18 + 3 * mystic_space)) / 3

		mystical_dot = Dot(right_end + (buffer + 6 + 1.5 * mystic_space) * LEFT).set_color(BLACK)
		mystical_etc = Text('...').move_to(right_end + (buffer + 6 + 1.5 * mystic_space) * LEFT)

		cycle1name = Text('Cycle 1').move_to(left_end + (buffer + 3) * RIGHT + 4 * DOWN).scale(0.5)
		cycle2name = Text('Cycle 2').move_to(left_end + (buffer + 6 + buffer + 3) * RIGHT + 4 * DOWN).scale(0.5)
		cycleMname = Text('Cycle m').move_to(right_end + (buffer + 3) * LEFT + 4 * DOWN).scale(0.5)

		self.play(
			cycle1.change_center(left_end + (buffer + 3) * RIGHT),
			cycle2.change_center(left_end + (buffer + 6 + buffer + 3) * RIGHT),
			cycleM.change_center(right_end + (buffer + 3) * LEFT),
			Transform(dots[13], mystical_dot),
			Transform(labels[13], mystical_dot),
			Transform(etc, mystical_etc),
			Write(cycle1name),
			Write(cycle2name),
			Write(cycleMname),
			FadeIn(self.counter)
		)

		cycle1.add_label_updaters()
		cycle2.add_label_updaters()
		cycleM.add_label_updaters()

		# untangles the dots and arrows
		self.wait()
		self.play(*cycle1.untangle(), *cycle2.untangle(), *cycleM.untangle())
		self.wait()

		cycle1.make_arrows_normal()
		cycle2.make_arrows_normal()
		cycleM.make_arrows_normal()

		self.wait()

		for _ in range(3):
			self.permute(cycle1, cycle2, cycleM)

		cycle1.make_arrows_sticky()
		cycle2.make_arrows_sticky()
		cycleM.make_arrows_sticky()
		cycle1.remove_label_updaters()
		cycle2.remove_label_updaters()
		cycleM.remove_label_updaters()

		self.play(
			cycle1.change_center(cycle1.circle.get_center() + 4 * UP),
			cycle2.change_center(cycle2.circle.get_center() + 4 * UP),
			cycleM.change_center(cycleM.circle.get_center() + 4 * UP),
			ApplyMethod(cycle1name.shift, 4 * UP),
			ApplyMethod(cycle2name.shift, 4 * UP),
			ApplyMethod(cycleMname.shift, 4 * UP),
			ApplyMethod(mystical_etc.shift, 4 * UP),
			ApplyMethod(etc.shift, 4 * UP)
		)

		equation1 = MathTex(r"f^{\text{lcm}(c_1, c_2, ..., c_m)} = \text{Identity}").shift(2 * DOWN).scale(2)
		equation2 = MathTex(r"\text{lcm}(c_1, c_2, ..., c_m) = 1000").shift(4 * DOWN + 1.3 * LEFT).scale(2)
		equation3 = MathTex(r"c_1 + c_2 + ... + c_m = n").shift(6 * DOWN + 2 * LEFT).scale(2)
		self.play(Write(equation1))
		self.wait(16)
		self.play(Write(equation2))
		self.wait(10)
		self.play(Write(equation3))

		self.wait(10)
		self.play(
			*[FadeOut(dot) for dot in dots], *[FadeOut(label) for label in labels],
			*[FadeOut(dot) for dot in cycle1.dots], *[FadeOut(label) for label in cycle1.labels],
			*[FadeOut(dot) for dot in cycle2.dots], *[FadeOut(label) for label in cycle2.labels],
			*[FadeOut(dot) for dot in cycleM.dots], *[FadeOut(label) for label in cycleM.labels],
			*cycle1.hide_arrows(), *cycle2.hide_arrows(), *cycleM.hide_arrows(),
			FadeOut(self.counter), FadeOut(etc), FadeOut(mystical_etc),
			FadeOut(cycle1name), FadeOut(cycle2name), FadeOut(cycleMname),
			FadeOut(equation1), FadeOut(equation2), FadeOut(equation3)
		)


class Solving(Scene):
	def construct(self):
		self.wait(3.5)

		equations = MathTex(
			r"\text{lcm}(",
			r"c_1, c_2, c_3, c_4, \dots, c_m",
			")&=",
			"1000",
			r"\\",
			r"c_1 + c_2 + c_3 + c_4 + \dots + c_m",
			"&= n"
		)

		self.play(FadeIn(equations))

		step = MathTex(
			r"\text{lcm}(",
			r"c_1, c_2, c_3, c_4, \dots, c_m",
			")&=",
			r"2^3 \cdot 5^3",
			r"\\",
			r"c_1 + c_2 + c_3 + c_4 + \dots + c_m",
			"&= n"
		)

		self.play(
			Transform(
				equations[3],
				MathTex(r"2^3 \cdot 5^3").set_x(step[3].get_x() - step[2].get_x() + equations[2].get_x()).set_y(step[3].get_y()),
			)
		)

		step = MathTex(
			r"\text{lcm}(",
			r"1000",
			")&=",
			r"2^3 \cdot 5^3",
			r"\\",
			r"1000",
			"&= n"
		)
		self.wait(11.5)
		self.play(
			*[ApplyMethod(equations[index].move_to, step[index]) for index in [0, 2, 3, 4, 6]],
			Transform(equations[1], MathTex(r"1000").move_to(step[1])),
			Transform(equations[5], MathTex(r"1000").move_to(step[5]))
		)

		step = MathTex(
			r"\text{lcm}(",
			r"2^3, 5^3",
			")&=",
			r"2^3 \cdot 5^3",
			r"\\",
			r"2^3 + 5^3",
			"&= n"
		)
		self.wait(7)
		self.play(
			*[ApplyMethod(equations[index].move_to, step[index]) for index in [0, 2, 3, 4, 6]],
			Transform(equations[1], MathTex(r"2^3, 5^3").move_to(step[1])),
			Transform(equations[5], MathTex(r"2^3 + 5^3").move_to(step[5]))
		)

		step = MathTex(
			r"\text{lcm}(",
			r"2^3, 5^3",
			")&=",
			r"2^3 \cdot 5^3",
			r"\\",
			r"133",
			"&= n"
		)

		self.play(
			*[ApplyMethod(equations[index].move_to, step[index]) for index in [0, 1, 2, 3, 4, 6]],
			Transform(equations[5], MathTex(r"133").move_to(step[5]))
		)
		self.wait(14)

		step = MathTex(
			r"\text{lcm}(",
			r"c_1, c_2, c_3, c_4, \dots, c_m",
			")&=",
			r"2^3 \cdot 5^3",
			r"\\",
			r"c_1 + c_2 + c_3 + c_4 + \dots + c_m",
			"&= n"
		)
		self.play(
			*[ApplyMethod(equations[index].move_to, step[index]) for index in [0, 2, 3, 4, 6]],
			Transform(equations[1], MathTex(r"c_1, c_2, c_3, c_4, \dots, c_m").move_to(step[1])),
			Transform(equations[5], MathTex(r"c_1 + c_2 + c_3 + c_4 + \dots + c_m").move_to(step[5]))
		)
		self.wait(9)

		equationsPart2 = MathTex(
			r"\text{lcm}(",
			r"c_1", r",", r"c_2", r",", r"c_3", ",", "c_4", ",", r"\dots", r",", r"c_m",
			r") &= 2^3 \cdot 5^3",
			r"\\c_1 + c_2 + c_3 + c_4 + \dots + c_m &= n"
		)

		self.add(equationsPart2)
		self.remove(equations)

		vertical_ci = MathTex(
			'c_1', '&=', '2', '^{a_1}', '5', r'^{b_1}', r'\geq ', r'5^{b_1}\\',
			'c_2', '&=', '2', '^{a_2}', '5', r'^{b_2}', r'\geq ', r'2^{a_2}', r' + ', r'5^{b_2}\\',
			'c_3', '&=', '2', '^{a_3}', '5', r'^{b_3}', r'\geq ', r'2^{a_3}\\',
			'c_4', '&=', '2', '^{a_4}', '5', r'^{b_4}', r'\geq ', r'5^{b_4}\\',
			r'\vdots \\',
			'c_m', '&=', '2', '^{a_m}', '5', r'^{b_m}', r'\geq ', r'2^{a_m}', r' + ', r'5^{b_m}\\',
		).shift(UP + RIGHT)

		step = MathTex(
			'c_1', '&=', '2', '^{a_m}', '5', r'^{b_m}', r'\geq ', r'5^{b_m}\\',
			'c_2', '&=', '2', '^{a_m}', '5', r'^{b_m}', r'\geq ', r'2^{a_m}', r' + ', r'5^{b_m}\\',
			'c_3', '&=', '2', '^{a_m}', '5', r'^{b_m}', r'\geq ', r'2^{a_m}\\',
			'c_4', '&=', '2', '^{a_m}', '5', r'^{b_m}', r'\geq ', r'5^{b_m}\\',
			r'\vdots \\',
			'c_m', '&=', '2', '^{a_m}', '5', r'^{b_m}', r'\geq ', r'2^{a_m}', r' + ', r'5^{b_m}\\',
		).shift(UP + RIGHT)

		for index in [6, 7, 14, 15, 16, 17, 24, 25, 32, 33, 41, 42, 43, 44]:
			vertical_ci[index].set_x(step[index].get_x())

		vertical_ci[34].set_x(vertical_ci[0].get_x())

		lcm_expression = MathTex(r'\text{lcm}(c_1, c_2, c_3, c_4, \dots, c_m)', r'=', r'2^3 \cdot 5^3')
		lcm_expression.shift((vertical_ci[36].get_x() - lcm_expression[1].get_x()) * RIGHT)
		lcm_expression.set_y(vertical_ci[35].get_y() - (vertical_ci[0].get_y() - vertical_ci[8].get_y()))

		self.play(
			ApplyMethod(equationsPart2[1].move_to, vertical_ci[0].get_center()),
			ApplyMethod(equationsPart2[3].move_to, vertical_ci[8].get_center()),
			ApplyMethod(equationsPart2[5].move_to, vertical_ci[18].get_center()),
			ApplyMethod(equationsPart2[7].move_to, vertical_ci[26].get_center()),
			equationsPart2[9].animate.move_to(vertical_ci[34].get_center()).rotate(PI / 2),
			ApplyMethod(equationsPart2[11].move_to, vertical_ci[35].get_center()),
			*[FadeOut(equationsPart2[index]) for index in [0, 2, 4, 6, 8, 10, 12, 13]]
		)

		self.play(
			*[FadeIn(vertical_ci[index]) for index in
			  [item for item in range(45) if item not in [6, 7, 14, 15, 16, 17, 24, 25, 32, 33, 41, 42, 43, 44]]],
			FadeIn(lcm_expression),
			*[FadeOut(equationsPart2[index]) for index in [1, 3, 5, 7, 9, 11]]
		)
		self.wait(14)

		self.play(
			ApplyMethod(vertical_ci[3].set_color, RED),
			ApplyMethod(vertical_ci[23].set_color, RED),
			ApplyMethod(vertical_ci[29].set_color, RED),
		)
		self.play(
			ApplyMethod(vertical_ci[2].set_color, BLACK),
			ApplyMethod(vertical_ci[3].set_color, BLACK),
			ApplyMethod(vertical_ci[22].set_color, BLACK),
			ApplyMethod(vertical_ci[23].set_color, BLACK),
			ApplyMethod(vertical_ci[28].set_color, BLACK),
			ApplyMethod(vertical_ci[29].set_color, BLACK),
			ApplyMethod(vertical_ci[4].move_to, (vertical_ci[2].get_center())),
			ApplyMethod(vertical_ci[5].move_to, (vertical_ci[3].get_center())),
			ApplyMethod(vertical_ci[30].move_to, (vertical_ci[28].get_center())),
			ApplyMethod(vertical_ci[31].move_to, (vertical_ci[29].get_center())),
		)

		self.wait(9.5)
		self.play(
			*[FadeIn(vertical_ci[index]) for index in [6, 7, 14, 15, 16, 17, 24, 25, 32, 33, 41, 42, 43, 44]]
		)

		self.wait(4)

		inequality = MathTex(
			r"c_1",  # 0
			r" + ",  # 1
			r"c_2",  # 2
			r" + ",  # 3
			r"c_3",  # 4
			r" + ",  # 5
			r"c_4",  # 6
			r" + ",  # 7
			r"\cdots",  # 8
			r" + ",  # 9
			r"c_m",  # 10
			r"\geq",  # 11
			r"5^{b_1}",  # 12
			r" + ",  # 13
			r"2^{a_2}",  # 14
			r" + ",  # 15
			r"5^{b_2}",  # 16
			r" + ",  # 17
			r"2^{a_3}",  # 18
			r" + ",  # 19
			r"5^{b_4}",  # 20
			r" + ",  # 21
			r"\cdots",  # 22
			r" + ",  # 23
			r"2^{a_m}",  # 24
			r" + ",  # 25
			r"5^{b_m}",  # 26
		).scale(0.8)

		etc_copy = vertical_ci[34].copy()
		self.play(
			Transform(vertical_ci[0], inequality[0]),
			Transform(vertical_ci[8], inequality[2]),
			Transform(vertical_ci[18], inequality[4]),
			Transform(vertical_ci[26], inequality[6]),
			Transform(vertical_ci[35], inequality[10]),

			Transform(vertical_ci[7], inequality[12]),

			Transform(vertical_ci[15], inequality[14]),
			Transform(vertical_ci[16], inequality[15]),
			Transform(vertical_ci[17], inequality[16]),

			Transform(vertical_ci[25], inequality[18]),

			Transform(vertical_ci[33], inequality[20]),

			Transform(vertical_ci[42], inequality[24]),
			Transform(vertical_ci[43], inequality[25]),
			Transform(vertical_ci[44], inequality[26]),

			Transform(vertical_ci[34], inequality[8]),
			Transform(etc_copy, inequality[22]),

			*[
				ApplyMethod(vertical_ci[index].set_color, BLACK)
				for index in [item for item in range(45) if item not in [0, 8, 18, 26, 35, 7, 15, 16, 17, 25, 33, 42, 43, 44, 34]]
			],
			FadeOut(lcm_expression),
		)
		self.play(FadeIn(inequality), FadeOut(vertical_ci))

		grouped = MathTex(
			r"c_1",  # 0
			r" + ",  # 1
			r"c_2",  # 2
			r" + ",  # 3
			r"c_3",  # 4
			r" + ",  # 5
			r"c_4",  # 6
			r" + ",  # 7
			r"\cdots",  # 8
			r" + ",  # 9
			r"c_m",  # 10
			r"\geq",  # 11
			r"(",  # 12
			r"2^{a_2}",  # 13
			r" + ",  # 14
			r"2^{a_3}",  # 15
			r" + ",  # 16
			r"\cdots",  # 17
			r" + ",  # 18
			r"2^{a_m}",  # 19
			r")",  # 20
			r" + ",  # 21
			r"(",  # 22
			r"5^{b_1}",  # 23
			r" + ",  # 24
			r"5^{b_2}",  # 25
			r" + ",  # 26
			r"5^{b_4}",  # 27
			r" + ",  # 28
			r"\cdots",  # 29
			r" + ",  # 30
			r"5^{b_m}",  # 31
			r")",  # 32
		).scale(0.7)

		copy_plus = inequality[25].copy()
		self.add(copy_plus, etc_copy)

		self.wait()
		self.play(
			*[Transform(inequality[index], grouped[index]) for index in range(12)],
			Transform(inequality[12], grouped[23]),
			Transform(inequality[14], grouped[13]),
			Transform(inequality[16], grouped[25]),
			Transform(inequality[18], grouped[15]),
			Transform(inequality[20], grouped[27]),
			Transform(inequality[24], grouped[19]),
			Transform(inequality[26], grouped[31]),

			Transform(inequality[13], grouped[14]),
			Transform(inequality[15], grouped[16]),
			Transform(inequality[17], grouped[18]),
			Transform(inequality[19], grouped[21]),
			Transform(inequality[21], grouped[24]),
			Transform(inequality[23], grouped[26]),
			Transform(inequality[25], grouped[28]),
			Transform(copy_plus, grouped[30]),

			Transform(inequality[22], grouped[17]),
			Transform(etc_copy, grouped[29]),
			*[FadeIn(grouped[index]) for index in [12, 20, 22, 32]]
		)
		self.play(
			*[FadeIn(grouped[index]) for index in [item for item in range(33) if item not in [12, 20, 22, 32]]],
			FadeOut(inequality), FadeOut(etc_copy), FadeOut(copy_plus)
		)

		self.wait(3)

		brace_under_2 = BraceBetweenPoints(grouped[12].get_center(), grouped[20].get_center())
		brace_under_2_text = brace_under_2.get_tex(r"\geq 2^3").scale(0.7).shift(UP * 0.3)
		brace_under_5 = BraceBetweenPoints(grouped[22].get_center(), grouped[32].get_center())
		brace_under_5_text = brace_under_5.get_tex(r"\geq 5^3").scale(0.7).shift(UP * 0.3)

		self.play(FadeIn(brace_under_2))
		self.wait(3)
		self.play(FadeIn(brace_under_2_text))
		self.wait(2)
		self.play(FadeIn(brace_under_5))
		self.wait(0.5)
		self.play(FadeIn(brace_under_5_text))
		self.wait()

		final_inequality_split = MathTex(
			r"c_1",  # 0
			r" + ",  # 1
			r"c_2",  # 2
			r" + ",  # 3
			r"c_3",  # 4
			r" + ",  # 5
			r"c_4",  # 6
			r" + ",  # 7
			r"\cdots",  # 8
			r" + ",  # 9
			r"c_m",  # 10
			r"\geq",  # 11
			r"(",  # 12
			r"2^{a_2}",  # 13
			r" + ",  # 14
			r"2^{a_3}",  # 15
			r" + ",  # 16
			r"\cdots",  # 17
			r" + ",  # 18
			r"2^{a_m}",  # 19
			r")",  # 20
			r" + ",  # 21
			r"(",  # 22
			r"5^{b_1}",  # 23
			r" + ",  # 24
			r"5^{b_2}",  # 25
			r" + ",  # 26
			r"5^{b_4}",  # 27
			r" + ",  # 28
			r"\cdots",  # 29
			r" + ",  # 30
			r"5^{b_m}",  # 31
			r")",  # 32
			r"\geq",
			r"2^3",
			r"+",
			r"5^3"
		).scale(0.65)

		self.play(
			*[Transform(grouped[index], final_inequality_split[index]) for index in range(33)],
			Transform(brace_under_2_text, final_inequality_split[34]),
			Transform(brace_under_5_text, final_inequality_split[36]),
			FadeOut(brace_under_2), FadeOut(brace_under_5),
			*[FadeIn(final_inequality_split[index]) for index in [33, 35]]
		)
		self.play(
			*[FadeIn(final_inequality_split[index]) for index in [item for item in range(37) if item not in [33, 35]]],
			FadeOut(grouped)),
		self.wait()

		final_inequality_clumped = MathTex(
			r"c_1 + c_2 + c_3 + c_4 + \cdots + c_m",
			r"\geq",
			r"(",
			r"2^{a_2} + 2^{a_3} + \cdots + 2^{a_m}",
			r")",
			r" + ",
			r"(",
			r"5^{b_1} + 5^{b_2} + 5^{b_4} + \cdots + 5^{b_m}",
			r")",
			r"\geq",
			r"2^3 + 5^3"
		).scale(0.65).move_to(final_inequality_split)

		self.play(FadeIn(final_inequality_clumped))
		self.play(FadeOut(final_inequality_split), FadeOut(brace_under_2_text), FadeOut(brace_under_5_text))

		step = MathTex(
			r"c_1 + c_2 + c_3 + c_4 + \cdots + c_m",
			r"\geq",
			r"2^3 + 5^3"
		)

		self.wait(2)
		self.play(*[FadeOut(final_inequality_clumped[index]) for index in [1, 2, 3, 4, 5, 6, 7, 8]])
		self.play(
			Transform(final_inequality_clumped[0], step[0]),
			Transform(final_inequality_clumped[9], step[1]),
			Transform(final_inequality_clumped[10], step[2]),
		)

		step = MathTex(
			r"c_1 + c_2 + c_3 + c_4 + \cdots + c_m",
			r"\geq",
			r"133"
		)

		self.play(
			Transform(final_inequality_clumped[0], step[0]),
			Transform(final_inequality_clumped[9], step[1]),
			Transform(final_inequality_clumped[10], step[2]),
		)

		self.wait(5)

		step = MathTex(
			r"n",
			r"\geq",
			r"133"
		)

		self.play(
			Transform(final_inequality_clumped[0], step[0]),
			Transform(final_inequality_clumped[9], step[1]),
			Transform(final_inequality_clumped[10], step[2]),
		)

		self.wait(17)
		self.play(*[FadeOut(mobject) for mobject in self.mobjects])


class ShowingValidPermutation(ZoomedScene, MovingCameraScene):
	def permute(self, dot_loc, label_loc, *cycles, fadein_arrows=True, fadeout_arrows=True, foa=None):
		transforms = []
		fade_in_arrows = []
		fade_out_arrows = []
		for cycle in cycles:
			dots = cycle.dots
			labels = cycle.labels
			for index in range(len(dots)):
				this_dot = dots[index - 1]
				next_dot = dots[index]
				this_label = labels[index - 1]
				next_label = labels[index]

				transforms.append(Transform(this_dot, next_dot))

				if approx(this_label.get_center(), label_loc):
					this_label.set_value(next_label.get_value() - 1)

				target_label = this_label.copy().move_to(next_label.get_center())

				if approx(next_label.get_center(), label_loc):
					target_label.set_color(BLACK)
				else:
					target_label.set_color(WHITE)

				transforms.append(Transform(this_label, target_label))

				if not (approx(next_dot.get_center(), dot_loc) or approx(this_dot.get_center(), dot_loc)):
					arrow = make_arrow_between(this_dot, next_dot)
					fade_in_arrows.append(FadeIn(arrow))
					fade_out_arrows.append(FadeOut(arrow))

		if fadein_arrows:
			self.play(*fade_in_arrows)

		self.play(*transforms)

		if fadeout_arrows:
			if foa is None:
				self.play(*fade_out_arrows)
			else:
				self.play(*fade_out_arrows, *foa)

		return fade_out_arrows

	def construct(self):
		circle = Circle(radius=3, color=RED)

		num_points = 20

		dots = []
		labels = []

		for c, angle in enumerate(np.linspace(0, TAU, num_points, endpoint=False)):
			p = circle.point_at_angle(angle)
			d = Dot(point=p)
			dots.append(d)
			label = Integer(c + 1).move_to(p * 1.15).scale(0.5)
			labels.append(label)

		labels[-1] = Integer(133).move_to(labels[-1].get_center()).scale(0.5)
		for c in range(2, 7, 1):
			labels[-c] = Integer(134 - c).move_to(labels[-c].get_center()).scale(0.5)

		# Hides the 14th dot and puts a '...' in its place
		dot_loc = dots[13].get_center()
		dots[13].set_color(BLACK).set_opacity(0)
		labels[13].set_color(BLACK)

		angle = Line(start=dots[12].get_center(), end=dots[14].get_center()).get_angle()
		etc = Text('...')
		etc.save_state()
		etc.move_to(dot_loc).rotate(angle)

		self.wait(2)
		self.play(*[FadeIn(dot) for dot in dots], *[FadeIn(label) for label in labels], FadeIn(etc))

		permutations = [
			[0, 1, 2, 3, 4, 5, 6, 7, 0],
			[8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 8]
		]

		cycle1order = permutations[0]
		cycle2order = permutations[1]

		cycle1 = Cycle(
			circle=circle.copy(),
			dots=[dots[index] for index in cycle1order[:-1]],
			labels=[labels[index] for index in cycle1order[:-1]]
		)

		cycle2 = Cycle(
			circle=circle.copy(),
			dots=[dots[index] for index in cycle2order[:-1]],
			labels=[labels[index] for index in cycle2order[:-1]]
		)

		def etc_updater(mob):
			mob.restore()
			mob.move_to(dots[13])
			line = Line(start=dots[12].get_center(), end=dots[14].get_center())
			mob.rotate(line.get_angle())

		etc.add_updater(etc_updater)

		self.wait(8)
		self.play(self.camera.frame.animate.scale(2))
		self.play(cycle1.change_center(6 * LEFT), cycle2.change_center(6 * RIGHT))

		cycle1.add_label_updaters()
		cycle2.add_label_updaters()

		# untangles the dots and arrows
		self.play(*cycle1.untangle(), *cycle2.untangle())

		etc.remove_updater(etc_updater)

		cycle1.remove_label_updaters()
		cycle2.remove_label_updaters()

		dot_loc = dots[13].get_center()
		label_loc = labels[13].get_center()

		self.wait(3)

		foa = self.permute(dot_loc, label_loc, cycle1, cycle2, fadein_arrows=True, fadeout_arrows=False)

		self.permute(dot_loc, label_loc, cycle1, cycle2, fadein_arrows=False, fadeout_arrows=False)

		self.permute(dot_loc, label_loc, cycle1, cycle2, fadein_arrows=False, fadeout_arrows=True, foa=foa)

		self.wait(11)

		self.play(
			*[FadeOut(dot) for dot in cycle1.dots], *[FadeOut(label) for label in cycle1.labels],
			*[FadeOut(dot) for dot in cycle2.dots], *[FadeOut(label) for label in cycle2.labels],
			FadeOut(etc)
		)


class Summarize(Scene):
	def construct(self):
		summarize = Text("In conclusion:").shift(UP * 2)
		equation = MathTex(
			r"\min"
			r"\{"
			r"n\in \mathbb{N}: \exists f\in [n]^{[n]} "
			r"("
			r"\forall x_1,x_2\in [n] f(x_1)=f(x_2)\implies x_1=x_2"
			r") \land ( "
			r"\min \{ k \in \mathbb{N}: f^k=\text{Id}"
			r"\}"
			r"=1000"
			r")"
			r"\}"
			r"=133."
		).scale(0.6)

		self.play(Write(summarize))
		self.play(Write(equation))
		self.wait(2)
		self.play(FadeOut(summarize), FadeOut(equation))


class ReshowProblem(Scene):
	def construct(self):
		text_part1 = MathTex(
			r"\text{Find the least positive integer } n"
			r"\text{ for which there exists a permutation } f \text{ on } n \text{ objects}"
		).scale(0.6).shift(UP * 0.5)
		text_part2 = MathTex(
			r"\text{ such that } f^{1000} \text{ is the identity function}"
			r"\text{ and } 1000 \text{ is the least positive integer for which this holds.}"
		).scale(0.6)
		self.play(FadeIn(text_part1), FadeIn(text_part2))
		self.wait(5)
		self.play(FadeOut(text_part1), FadeOut(text_part2))
