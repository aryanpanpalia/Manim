import math

from manim import *
from sympy.ntheory import factorint


def prime_factorization_in_tex(num_to_be_factored):
	tex_strs = []
	for prime in factorint(num_to_be_factored):
		exponent = factorint(num_to_be_factored)[prime]
		tex_strs.append(str(prime))
		if exponent > 1:
			tex_strs.append('^{' + str(factorint(num_to_be_factored)[prime]) + '}')
		tex_strs.append(r'\cdot ')

	if tex_strs[len(tex_strs) - 1] == r'\cdot ':
		tex_strs.pop(len(tex_strs) - 1)

	return tex_strs


def prime_factorization_in_tex_wexp_1(num_to_be_factored):
	tex_strs = []
	for prime in factorint(num_to_be_factored):
		tex_strs.append(str(prime))
		tex_strs.append('^{' + str(factorint(num_to_be_factored)[prime]) + '}')
		tex_strs.append(r'\cdot ')

	if tex_strs[len(tex_strs) - 1] == r'\cdot ':
		tex_strs.pop(len(tex_strs) - 1)

	return tex_strs


def move_to(mobject, move_to_location, run_time):
	mobject.generate_target()
	mobject.target.shift(move_to_location)
	return MoveToTarget(mobject, run_time=run_time)


def factorize_array(int_array):
	tex_strs = []
	for num in int_array:
		tex_strs.append(str(num))
		tex_strs.append('&=')
		for string in prime_factorization_in_tex(num):
			tex_strs.append(string)
		tex_strs.append(r'\\')
	tex_strs.pop()
	return tex_strs


def factorize_array_1(int_array):
	tex_strs = []
	for num in int_array:
		tex_strs.append(str(num))
		tex_strs.append('&=')
		for string in prime_factorization_in_tex_wexp_1(num):
			tex_strs.append(string)
		tex_strs.append(r'\\')
	tex_strs.pop()
	return tex_strs


def factorize_with_exp_0(int_array):
	tex_strs = []

	all_primes_with_duplicates = [prime for thingy in int_array for prime in factorint(thingy)]

	all_primes = []

	for x in all_primes_with_duplicates:
		if x not in all_primes:
			all_primes.append(x)

	all_primes.sort()

	for index in range(len(int_array)):
		tex_strs.append(str(int_array[index]))
		tex_strs.append('&=')
		for prime in all_primes:
			exponent = 0
			if prime in factorint(int_array[index]).keys():
				exponent = factorint(int_array[index])[prime]
			tex_strs.append(str(prime))

			if exponent != 1:
				tex_strs.append('^{' + str(exponent) + '}')

			tex_strs.append(r'\cdot ')

		if tex_strs[len(tex_strs) - 1] == r'\cdot ':
			tex_strs.pop(len(tex_strs) - 1)
		tex_strs.append(r'\\')
	tex_strs.pop()
	return tex_strs


def factorize_with_boxed(int_array):
	tex_strs = []

	all_primes_with_duplicates = []
	for index in range(len(int_array)):
		for prime in factorint(int_array[index]):
			all_primes_with_duplicates.append(prime)

	all_primes = []
	for x in all_primes_with_duplicates:
		if x not in all_primes:
			all_primes.append(x)
	all_primes.sort()

	max_exponent_of_prime = []
	for prime in all_primes:
		max_exp = 0
		max_exp_index = 0
		if prime in factorint(int_array[0]):
			max_exp = factorint(int_array[0])[prime]

		for index in range(len(int_array)):
			if prime in factorint(int_array[index]) and factorint(int_array[index])[prime] > max_exp:
				max_exp = factorint(int_array[index])[prime]
				max_exp_index = index
		max_exponent_of_prime.append(max_exp_index)

	for index in range(len(int_array)):
		tex_strs.append(str(int_array[index]))
		tex_strs.append('&=')
		for prime_index in range(len(all_primes)):
			exponent = 0
			if all_primes[prime_index] in factorint(int_array[index]).keys():
				exponent = factorint(int_array[index])[all_primes[prime_index]]
			tex_strs.append(str(all_primes[prime_index]))

			if index == max_exponent_of_prime[prime_index]:
				tex_strs.append(r'^{\color{red}' + str(exponent) + '}')
			else:
				tex_strs.append('^{' + str(exponent) + '}')

			if prime_index != len(all_primes) - 1:
				tex_strs.append(r'\cdot ')

		tex_strs.append(r'\\')

	return tex_strs


def locations_of_lcm_inputs(general_array):
	input_index_array = [0]
	while '&=' in general_array[input_index_array[-1] + 1: len(general_array) - 1: 1]:
		input_index_array.append(general_array.index('&=', input_index_array[-1] + 1, len(general_array) - 1))
	input_index_array.pop(0)

	for index in range(len(input_index_array)):
		input_index_array[index] += -1

	return input_index_array


class LCMExplanation(Scene):

	def construct(self):
		lcm_inputs = [455, 500, 340, 117]
		lcm = 1
		for num in lcm_inputs:
			lcm = lcm * num // math.gcd(lcm, num)

		lcm_expression_starr = [r'\text{lcm}(', '455', ',', '500', ',', '340', ',', '117', ')']
		lcm_expression = MathTex(*lcm_expression_starr)

		factored_inputs_starr = factorize_array(lcm_inputs)
		factored_inputs = MathTex(*factored_inputs_starr)

		factored_exp_1_starr = factorize_array_1(lcm_inputs)
		factored_exp_1 = MathTex(*factored_exp_1_starr)

		factored_exp_0_starr = factorize_with_exp_0(lcm_inputs)
		factored_exp_0 = MathTex(*factored_exp_0_starr)

		factored_colored_exp_starr = factorize_with_boxed(lcm_inputs)
		factored_colored_exp = MathTex(*factored_colored_exp_starr).shift(RIGHT)

		indices_of_factored_lcm_inputs = locations_of_lcm_inputs(factored_inputs_starr)
		indices_of_lcm_inputs_colored_exp = locations_of_lcm_inputs(factored_colored_exp_starr)

		lcm_closed_paren_index = 2 * len(lcm_inputs)

		lcm_expression_final_location = factored_colored_exp[indices_of_lcm_inputs_colored_exp[-1]].get_corner(
			DOWN + RIGHT) + DOWN - lcm_expression[lcm_closed_paren_index].get_corner(UP + RIGHT)

		factored_inputs.shift(factored_colored_exp.get_corner(UP + LEFT) - factored_inputs.get_corner(UP + LEFT))
		factored_exp_0.shift(factored_colored_exp.get_corner(UP + LEFT) - factored_exp_0.get_corner(UP + LEFT))
		factored_exp_1.shift(factored_colored_exp.get_corner(UP + LEFT) - factored_exp_1.get_corner(UP + LEFT))

		input_copies = [lcm_expression[1 + 2 * index].copy() for index in range(len(lcm_inputs))]

		move_copies = [
			input_copies[index].animate.move_to(factored_inputs[indices_of_factored_lcm_inputs[index]].get_center())
			for index in range(len(lcm_inputs))
		]

		moves_to_final_locations_1 = []
		moves_to_final_locations_2 = []
		alt_moves_to_final_locations_1 = []

		previous_index_1 = 0
		alt_prev_index = 0
		for index in range(len(factored_inputs)):
			next_index = factored_exp_0_starr.index(
				factored_inputs_starr[index], previous_index_1,
				len(factored_exp_0_starr)
			)
			move = factored_inputs[index].animate.move_to(factored_exp_0[next_index].get_center())
			previous_index_1 = next_index
			moves_to_final_locations_1.append(move)

		for index in range(len(factored_inputs)):
			next_index = factored_exp_1_starr.index(
				factored_inputs_starr[index], alt_prev_index,
				len(factored_exp_1_starr)
			)
			move = factored_inputs[index].animate.move_to(factored_exp_1[next_index].get_center())
			alt_prev_index = next_index
			alt_moves_to_final_locations_1.append(move)

		previous_index_2 = 0
		for index in range(len(factored_exp_1)):
			color_string = r'^{\color{red}' + factored_exp_1_starr[index][2: -1: 1] + '}'
			next_index_cand_1 = len(factored_colored_exp_starr) + 1
			next_index_cand_2 = len(factored_colored_exp_starr) + 1
			if color_string in factored_colored_exp_starr[previous_index_2: len(factored_colored_exp_starr)]:
				next_index_cand_1 = factored_colored_exp_starr.index(
					color_string, previous_index_2,
					len(factored_colored_exp_starr)
				)
			if factored_exp_1_starr[index] in factored_colored_exp_starr[previous_index_2: len(factored_colored_exp_starr)]:
				next_index_cand_2 = factored_colored_exp_starr.index(
					factored_exp_1_starr[index], previous_index_2,
					len(factored_colored_exp_starr)
				)
			next_index_2 = min(next_index_cand_1, next_index_cand_2)
			move = factored_exp_1[index].animate.move_to(factored_colored_exp[next_index_2].get_center())
			previous_index_2 = next_index_2
			moves_to_final_locations_2.append(move)

		lcm_expression_starr.append('=')

		for string in factorize_with_boxed([lcm])[2: -1]:
			lcm_expression_starr.append(string)

		lcm_expression_final = MathTex(*lcm_expression_starr)
		lcm_expression_final.shift(
			lcm_expression[0].get_center() - lcm_expression_final[0].get_center() + lcm_expression_final_location
		)
		lcm_expression_final.set_color_by_tex(r'\color{red}', RED)

		expression = MathTex(r"455 \text{ } 500 \text{ } 340 \text{ } 117")

		self.play(FadeIn(expression))
		self.wait(1.5)
		self.play(Transform(expression, lcm_expression))

		self.wait(4)
		self.add(*input_copies)
		self.play(expression.animate.move_to(lcm_expression_final_location), *move_copies)
		self.wait()
		self.play(FadeIn(factored_inputs))
		self.remove(*input_copies)
		self.play(*alt_moves_to_final_locations_1)
		self.wait(6.5)
		self.play(FadeIn(factored_exp_1))
		self.remove(factored_inputs)
		self.wait(4)
		self.play(*moves_to_final_locations_2)
		self.wait(1.5)
		self.play(FadeIn(factored_colored_exp))
		self.wait(6)
		self.play(factored_colored_exp.animate.set_color_by_tex(r'\color{red}', RED))
		self.play(FadeIn(lcm_expression_final))
		self.wait(1)
		self.play(FadeOut(expression), FadeOut(factored_exp_1), FadeOut(factored_colored_exp), FadeOut(lcm_expression_final))
		self.wait()
