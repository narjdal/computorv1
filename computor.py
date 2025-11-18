# import re
# import cmath
# import argparse
# from fractions import Fraction
# from math import sqrt
# def parse_term(term):
#     term = term.strip()
#     if term == '0':  # allow lone 0
#         return 0, 0.0
#     match = re.match(r'([+-]?\s*\d*\.?\d*)\s*\*\s*X\^(\d+)', term.replace(' ', ''))
#     if not match:
#         raise ValueError(f"Invalid term: {term}")
#     coef_str = match.group(1)
#     coef = float(coef_str) if coef_str not in ('', '+', '-') else float(coef_str+'1')
#     power = int(match.group(2))
#     return power, coef

# def parse_equation(eq):
#     left, right = eq.split('=')
#     terms = {}
#     for term in re.split(r'(?=[+-])', left):
#         if term.strip():
#             power, coef = parse_term(term)
#             terms[power] = terms.get(power, 0) + coef
#     for term in re.split(r'(?=[+-])', right):
#         if term.strip():
#             power, coef = parse_term(term)
#             terms[power] = terms.get(power, 0) - coef
#     # Remove tiny floating point errors
#     for k in terms:
#         if abs(terms[k]) < 1e-12:
#             terms[k] = 0.0
#     return terms

# def reduced_form_str(terms):
#     parts = []
#     for power in sorted(terms.keys()):
#         coef = terms[power]
#         if coef == 0:
#             continue

#         sign = "+" if coef > 0 else "-"
#         abs_coef = abs(coef)

#         if not parts:
#             # first term: no leading plus
#             parts.append(f"{abs_coef:g} * X^{power}" if coef > 0 else f"- {abs_coef:g} * X^{power}")
#         else:
#             parts.append(f"{sign} {abs_coef:g} * X^{power}")

#     if not parts:
#         return "0 * X^0 = 0"

#     return " ".join(parts) + " = 0"

# # def reduced_form_str(terms):
# #     items = []
# #     for power in sorted(terms.keys()):
# #         coef = terms[power]
# #         if coef == 0:
# #             continue
# #         coef_str = f"{coef:g}"  # removes unnecessary .0
# #         sign = '+' if coef > 0 else '-'
# #         if items:
# #             items.append(f" {sign} {abs(float(coef_str))} * X^{power}")
# #         else:
# #             items.append(f"{coef_str} * X^{power}" if coef > 0 else f"- {abs(float(coef_str))} * X^{power}")
# #     if not items:
# #         items.append("0 * X^0")
# #     return " + ".join(items).replace('+ -', '- ') + " = 0"

# def solve(terms):
#     degree = max((power for power, coef in terms.items() if coef != 0), default=0)
#     print("Reduced form:", reduced_form_str(terms))
#     print("Polynomial degree:", degree)

#     if degree > 2:
#         print("The polynomial degree is strictly greater than 2, I can't solve.")
#         return

#     if degree == 0:
#         if terms.get(0, 0) == 0:
#             print("Any real number is a solution.")
#         else:
#             print("No solution.")
#         return

#     if degree == 1:
#         a = terms.get(1, 0)
#         b = terms.get(0, 0)
#         solution = -b / a
#         print("The solution is:")
#         print(f"{solution:g}")
#         return
#     if degree == 2:
#     # Convert to Fraction for exact math
#         a = Fraction(terms.get(2, 0)).limit_denominator()
#         b = Fraction(terms.get(1, 0)).limit_denominator()
#         c = Fraction(terms.get(0, 0)).limit_denominator()

#         delta = b**2 - 4*a*c

#         if delta > 0:
#             print("Discriminant is strictly positive, the two solutions are:")
#             x1 = (-b + sqrt(delta)) / (2*a)
#             x2 = (-b - sqrt(delta)) / (2*a)
#             # print(f"{x2}")
#             # print(f"{x1}")
#             print(f"{float(x2):.6f}")
#             print(f"{float(x1):.6f}")

#         elif delta == 0:
#             print("Discriminant is zero, the solution is:")
#             x = -b / (2*a)
#             print(f"{x}")

#         else:
#             print("Discriminant is strictly negative, the two complex solutions are:")

#             real_part = -b / (2 * a)

#             imag_num = sqrt(abs(delta))
#             if abs(imag_num - round(imag_num)) < 1e-12:
#                 imag_num = int(round(imag_num))

#             imag_part = Fraction(imag_num, 2 * a)

#             print(f"{real_part} + {imag_part}i")
#             print(f"{real_part} - {imag_part}i")


#     # if degree == 2:
#     #     a = terms.get(2, 0)
#     #     b = terms.get(1, 0)
#     #     c = terms.get(0, 0)
#     #     delta = b**2 - 4*a*c
#     #     if delta > 0:
#     #         print("Discriminant is strictly positive, the two solutions are:")
#     #         x1 = (-b + delta**0.5)/(2*a)
#     #         x2 = (-b - delta**0.5)/(2*a)
#     #         print(f"{x2:g}")
#     #         print(f"{x1:g}")

#     #     elif delta == 0:
#     #         print("Discriminant is zero, the solution is:")
#     #         x = -b / (2*a)
#     #         print(f"{x:g}")
#     #     else:
#     #         print("Discriminant is strictly negative, the two complex solutions are:")
#     #            # Use Fraction for exact rational parts
#     #         real_part = Fraction(-b, 2 * a)

#     #         # Imaginary part: sqrt(|Δ|) / (2a)
#     #         imag_num = sqrt(abs(delta))

#     #         # Convert numerator to integer if it is actually an integer
#     #         if abs(imag_num - round(imag_num)) < 1e-12:
#     #             imag_num = int(round(imag_num))

#     #         imag_part = Fraction(imag_num, 2 * a)

#     # print(f"{real_part} + {imag_part}i")
#     # print(f"{real_part} - {imag_part}i")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Solve a polynomial equation of degree ≤ 2.")
#     parser.add_argument("equation", nargs='?', help='Polynomial equation e.g. "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"')
#     args = parser.parse_args()

#     if args.equation:
#         eq = args.equation
#     else:
#         eq = input("Enter an equation: ")

#     try:
#         terms = parse_equation(eq)
#         solve(terms)
#     except Exception as e:
#         print("Error:", e)


import re
import cmath
import argparse
from fractions import Fraction
from math import sqrt


# -------------------------------------------------------------
#  PARSE A SINGLE TERM (example: "5 * X^2")
# -------------------------------------------------------------
def parse_term(term):
    """
    Takes one term like '5 * X^2' and extracts:
      - its exponent (power)
      - its coefficient (coef)

    Returns: (power, coef)
    """

    term = term.strip()

    # Special case: the term is literally "0"
    if term == '0':
        return 0, 0.0

    # Regex to extract:   coefficient * X^power
    match = re.match(r'([+-]?\s*\d*\.?\d*)\s*\*\s*X\^(\d+)', term.replace(' ', ''))

    if not match:
        raise ValueError(f"Invalid term: {term}")

    coef_str = match.group(1)

    # If coef is "" or "+" or "-", it means ±1
    coef = float(coef_str) if coef_str not in ('', '+', '-') else float(coef_str + '1')

    power = int(match.group(2))

    return power, coef


# -------------------------------------------------------------
#  PARSE THE WHOLE EQUATION INTO A DICTIONARY OF TERMS
# -------------------------------------------------------------
def parse_equation(eq):
    """
    Splits the equation into left and right, then moves everything to the left.
    Builds and returns a dict:
        { power: coefficient }
    Example: "5 * X^0 + 4 * X^1 = 1 * X^0" becomes:
        { 0: 4, 1: 4 }
    """

    left, right = eq.split('=')
    terms = {}

    # --- Parse the left side, add coefficients ---
    for term in re.split(r'(?=[+-])', left):
        if term.strip():
            power, coef = parse_term(term)
            terms[power] = terms.get(power, 0) + coef

    # --- Parse the right side, subtract coefficients (move to left) ---
    for term in re.split(r'(?=[+-])', right):
        if term.strip():
            power, coef = parse_term(term)
            terms[power] = terms.get(power, 0) - coef

    # Remove floating-point noise
    for k in terms:
        if abs(terms[k]) < 1e-12:
            terms[k] = 0.0

    return terms


# -------------------------------------------------------------
#  PRINT THE EQUATION IN REDUCED FORM
# -------------------------------------------------------------
def reduced_form_str(terms):
    """
    Formats the polynomial in canonical reduced form.
    Example:
        {0: 4, 1: 2, 2: -9.3}
    becomes:
        "4 * X^0 + 2 * X^1 - 9.3 * X^2 = 0"
    """

    parts = []

    for power in sorted(terms.keys()):
        coef = terms[power]
        if coef == 0:
            continue

        sign = "+" if coef > 0 else "-"
        abs_coef = abs(coef)

        # First term: no leading "+"
        if not parts:
            parts.append(f"{abs_coef:g} * X^{power}" if coef > 0 else f"- {abs_coef:g} * X^{power}")
        else:
            parts.append(f"{sign} {abs_coef:g} * X^{power}")

    if not parts:
        return "0 * X^0 = 0"

    return " ".join(parts) + " = 0"


# -------------------------------------------------------------
#  SOLVE THE POLYNOMIAL OF DEGREE ≤ 2
# -------------------------------------------------------------
def solve(terms):
    """
    Solves the polynomial depending on its degree:
    - Degree 0: constant equation
    - Degree 1: linear equation ax + b = 0
    - Degree 2: quadratic, solved using discriminant Δ = b² - 4ac
    """

    degree = max((power for power, coef in terms.items() if coef != 0), default=0)

    print("Reduced form:", reduced_form_str(terms))
    print("Polynomial degree:", degree)

    # ------------------- DEGREE > 2 -------------------
    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return

    # ------------------- DEGREE 0 ----------------------
    if degree == 0:
        if terms.get(0, 0) == 0:
            print("Any real number is a solution.")  # 0 = 0
        else:
            print("No solution.")  # c = 0 but c ≠ 0
        return

    # ------------------- DEGREE 1 ----------------------
    if degree == 1:
        a = terms.get(1, 0)
        b = terms.get(0, 0)
        solution = -b / a
        print("The solution is:")
        print(f"{solution:g}")
        return

    # ---------------------------------------------------
    #                 DEGREE 2 (Quadratic)
    # ---------------------------------------------------
    if degree == 2:

        # Convert to Fraction for exact Δ and exact rational output
        a = Fraction(terms.get(2, 0)).limit_denominator()
        b = Fraction(terms.get(1, 0)).limit_denominator()
        c = Fraction(terms.get(0, 0)).limit_denominator()

        delta = b**2 - 4*a*c

        # ------------------ Δ > 0 : two real solutions ------------------
        if delta > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            x1 = (-b + sqrt(delta)) / (2*a)
            x2 = (-b - sqrt(delta)) / (2*a)

            # Format with exactly 6 digits after decimal
            print(f"{float(x2):.6f}")
            print(f"{float(x1):.6f}")

        # ------------------ Δ = 0 : one real solution -------------------
        elif delta == 0:
            print("Discriminant is zero, the solution is:")
            x = -b / (2*a)
            print(f"{x}")

        # ------------------ Δ < 0 : complex solutions -------------------
        else:
            print("Discriminant is strictly negative, the two complex solutions are:")

            # Real part = -b / (2a)
            real_part = -b / (2 * a)

            # Imaginary part = sqrt(|Δ|) / (2a)
            imag_num = sqrt(abs(delta))

            # Convert imaginary numerator to int if perfect square
            if abs(imag_num - round(imag_num)) < 1e-12:
                imag_num = int(round(imag_num))

            imag_part = Fraction(imag_num, 2 * a)

            print(f"{real_part} + {imag_part}i")
            print(f"{real_part} - {imag_part}i")


# -------------------------------------------------------------
#  ENTRY POINT — HANDLE COMMAND LINE ARGUMENTS
# -------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a polynomial equation of degree ≤ 2.")
    parser.add_argument(
        "equation",
        nargs='?',
        help='Polynomial equation, e.g.: "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"'
    )

    args = parser.parse_args()

    # If no argument provided → prompt user
    eq = args.equation if args.equation else input("Enter an equation: ")

    try:
        terms = parse_equation(eq)
        solve(terms)
    except Exception as e:
        print("Error:", e)
