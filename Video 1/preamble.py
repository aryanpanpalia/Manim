from abc import ABC

from manim import *
from numpy.linalg import linalg


class CustomArrowTip(ArrowTip, Triangle, ABC):
	def __init__(self, **kwargs):
		Triangle.__init__(self)
		self.scale(0.05)
		self.set_color(WHITE)
		self.set_fill(color=WHITE, opacity=0)


def make_arrow_between(dot1, dot2, buff):
	arrow = Line(
		dot1.get_center(),
		dot2.get_center(),
		stroke_width=3,
		buff=buff
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


def scale_from_point(group, point, factor):
	moves = []
	for obj in group:
		dist = linalg.norm(obj.get_center() - point.get_center())
		if dist != 0:
			direction = (obj.get_center() - point.get_center()) / dist
			moves.append(obj.animate.move_to(point.get_center() + direction * dist * factor))

	return moves


class Preamble(Scene):
	def construct(self):
		num_dots = 5
		spacing = 1
		ddots = [Dot(LEFT * (num_dots - 1) / 2 * spacing + spacing * ind * RIGHT) for ind in range(num_dots)]
		labels = [Integer(num + 1).scale(0.5).next_to(dot, DOWN) for num, dot in enumerate(ddots)]
		for dot, label in zip(ddots, labels):
			label.add_updater(lambda l, dot=dot, label=label: l.next_to(dot, DOWN))

		self.play(FadeIn(*ddots, *labels))

		curre = [num_dots - 1]

		def permute():
			anims = []
			loc = ddots[(curre[0] + 1) % num_dots].get_center()
			run_time = 1
			new_dot = Dot(loc)
			copy = labels[curre[0]].next_to(ddots[curre[0]], DOWN)
			self.remove(labels[curre[0]])
			lab = Integer(curre[0] + 1).scale(0.5).next_to(new_dot, DOWN)
			for index in range(num_dots):
				if index == curre[0]:
					g1 = AnimationGroup(FadeOut(copy), FadeOut(ddots[curre[0]]), run_time=run_time / 2)
					g3 = AnimationGroup(FadeIn(new_dot, run_time=run_time / 2), FadeIn(lab, run_time=run_time / 2))
					group = AnimationGroup(g1, g3, lag_ratio=1)
					anims.append(group)
				else:
					anims.append(ddots[index].animate(run_time=run_time).move_to(ddots[(index + 1) % num_dots]))
			self.play(*anims, run_time=0.75)
			ddots[curre[0] % num_dots].move_to(loc)
			self.add(labels[curre[0]], ddots[curre[0]])
			self.remove(lab, new_dot)
			curre[0] = (curre[0] - 1) % num_dots

		num_permute = 2

		for ind in range(num_permute):
			permute()

		shift_vec = 0.25 * LEFT

		dots = [Dot(ddots[(ind - num_permute) % 5].get_center()) for ind in range(5)]
		dots_copy = [dot.copy().set_opacity(0) for dot in dots]
		self.add(*dots, *dots_copy)
		self.remove(*ddots)

		# moves = [
		# 	dots[-1].animate.move_to(dots[3].get_center() + shift_vec),
		# 	dots[3].animate.shift(0.5 * UP + 0.5 * LEFT + shift_vec),
		# 	dots[2].animate.shift(RIGHT + 0.5 * DOWN + 0.5 * LEFT + shift_vec),
		# 	dots[1].animate.shift(RIGHT * 1.1 + UP * 1.1 + shift_vec),
		# 	dots[0].animate.shift(RIGHT * 2.1 + DOWN * 1.1 + shift_vec)
		# ]
		#
		# self.play(*moves, FadeOut(*labels), run_time=0.5)
		# grp = VGroup(*dots)
		# self.play(*scale_from_point(grp, dots[-1], 1.5), run_time=0.5)

		moves = [
			dots_copy[-1].animate.move_to(dots[3].get_center() + shift_vec),
			dots_copy[3].animate.shift(0.5 * UP + 0.5 * LEFT + shift_vec),
			dots_copy[2].animate.shift(RIGHT + 0.5 * DOWN + 0.5 * LEFT + shift_vec),
			dots_copy[1].animate.shift(RIGHT * 1.1 + UP * 1.1 + shift_vec),
			dots_copy[0].animate.shift(RIGHT * 2.1 + DOWN * 1.1 + shift_vec)
		]
		self.play(*moves, run_time=0.001)
		grp = VGroup(*dots_copy)
		self.play(*scale_from_point(grp, dots_copy[-1], 1.5), run_time=0.001)

		self.play(
			*[Transform(dot, copy.copy().set_opacity(1)) for dot, copy in zip(dots, dots_copy)],
			FadeOut(*labels), run_time=0.6
		)

		grp = VGroup(*dots)
		Fg = Arrow(start=[0, 0, 0], end=1.5 * DOWN, tip_shape=CustomArrowTip, buff=0, stroke_width=2)

		buff1 = 0.25

		bond1 = make_arrow_between(dots[4], dots[3], buff=buff1)
		bond2 = make_arrow_between(dots[4], dots[2], buff=buff1)
		bond3 = make_arrow_between(dots[2], dots[3], buff=buff1).shift(LEFT * 0.05)
		bond4 = make_arrow_between(dots[2], dots[3], buff=buff1).shift(RIGHT * 0.05)
		bond5 = make_arrow_between(dots[1], dots[3], buff=buff1)
		bond6 = make_arrow_between(dots[0], dots[2], buff=buff1)

		c4 = MathTex('C').scale(0.5).move_to(dots[4].get_center())
		c3 = MathTex('C').scale(0.5).move_to(dots[3].get_center())
		c2 = MathTex('C').scale(0.5).move_to(dots[2].get_center())
		c1 = MathTex('H').scale(0.5).move_to(dots[1].get_center())
		c0 = MathTex('H').scale(0.5).move_to(dots[0].get_center())

		electron1 = Dot().scale(0.3).move_to(dots[4].get_center() + 0.1 * (RIGHT + UP) + RIGHT * 0.05)
		electron2 = Dot().scale(0.3).move_to(dots[4].get_center() + 0.1 * (RIGHT + DOWN) + RIGHT * 0.05)

		self.play(
			Transform(dots[4], c4),
			Transform(dots[3], c3),
			Transform(dots[2], c2),
			Transform(dots[1], c1),
			Transform(dots[0], c0),
			FadeIn(bond1, bond2, bond3, bond4, bond5, bond6),
			FadeIn(electron1, electron2),
			run_time=0.75
		)

		self.wait(0.5)

		line1 = make_arrow_between(dots[4], dots[3], 0)
		line2 = make_arrow_between(dots[4], dots[2], 0)
		line6 = make_arrow_between(dots[0], dots[2], 0)
		line5 = make_arrow_between(dots[1], dots[3], 0)

		new_dots = [Dot(dots[ind].get_center()) for ind in range(num_dots)]

		self.play(
			Transform(bond1, line1),
			Transform(bond2, line2),
			Transform(bond5, line5),
			Transform(bond6, line6),
			Transform(dots[4], new_dots[4]),
			Transform(dots[3], new_dots[3]),
			Transform(dots[2], new_dots[2]),
			Transform(dots[1], new_dots[1]),
			Transform(dots[0], new_dots[0]),
			FadeOut(bond3, bond4, electron1, electron2),
			run_time=0.75
		)

		arrow_add_sticky_updater(bond5, dots[1], dots[3])
		arrow_add_sticky_updater(bond6, dots[0], dots[2])

		arrow_add_sticky_updater(bond1, dots[4], dots[3])

		self.play(
			dots[0].animate.move_to(dots[4].get_center() + 1.5 * LEFT),
			dots[1].animate.move_to(dots[4].get_center() + 1.5 * LEFT),
			FadeIn(Fg),
			run_time=0.5
		)

		self.play(
			grp.animate(rate_func=rate_functions.ease_in_quad).move_to(DOWN * 5),
			Fg.animate(rate_func=rate_functions.ease_in_quad).shift(DOWN * 5),
			bond2.animate(rate_func=rate_functions.ease_in_quad).shift(DOWN * 5),
			run_time=2
		)

		poly = RegularPolygon(10, stroke_color=WHITE).scale(2)

		self.wait(4.5)
		self.play(FadeIn(poly), run_time=1)
		self.play(Rotate(poly, np.round(TAU / 5, 13)))
		self.play(Rotate(poly, axis=UP))

		abstract = MathTex('\\text{Aut}(C_p^n)=\{f: C_p^n\\to C_p^n\mid f\\text{ is an isomorphism}\}')

		self.play(Transform(poly, abstract), run_time=1)
		self.wait(2)
		self.play(FadeOut(poly))

		uses = MathTex(
			r"&1. \text{ Diffie-Hellman Key Exchange (Cryptography)}\\"
			r"&2. \text{ Noether's Theorem (Physics)}\\"
			r"&3. \text{ Monstrous Moonshine (String Theory)}\\"
			r"&4. \text{ Periodic Tilings (Mathematics)}"
		).scale(0.6)

		addendum = MathTex(
			r"\text{The makers of the video are profoundly unknowledgeable about all the items in this list}"
		).scale(0.4).shift(3.5 * DOWN)
		self.play(FadeIn(uses), FadeIn(addendum))
		self.wait(11)
		self.play(FadeOut(uses), FadeOut(addendum))

		orb = MathTex('\\text{Orbit-Stabilizer Theorem}').shift(UP * 0.25)
		below_text_1 = MathTex('\\text{Nope, deeper than this}').scale(0.5).shift(DOWN * 0.40)

		self.play(FadeIn(orb))
		self.play(FadeIn(below_text_1))
		self.wait()

		classification = MathTex('\\text{The Classification of Finite Simple Groups}').shift(UP * 0.25)
		below_text_2 = MathTex('\\text{No, not }that\\text{ deep}').scale(0.5).shift(DOWN * 0.4)

		unsolvability = MathTex('\\text{Unsolvability of the Quintic}').shift(UP * 0.25)
		below_text_3 = MathTex('\\text{Perfect!}').scale(0.5).shift(DOWN * 0.4)

		self.play(FadeOut(below_text_1), Transform(orb, classification))
		self.play(FadeIn(below_text_2))
		self.wait()

		self.play(FadeOut(below_text_2), Transform(orb, unsolvability))
		self.play(FadeIn(below_text_3))
		self.wait()

		self.play(FadeOut(orb, below_text_3))
