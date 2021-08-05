from manim import *


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

