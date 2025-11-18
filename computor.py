import re
import cmath
import argparse

def parse_term(term):
    term = term.strip()
    if term == '0':  # allow lone 0
        return 0, 0.0
    match = re.match(r'([+-]?\s*\d*\.?\d*)\s*\*\s*X\^(\d+)', term.replace(' ', ''))
    if not match:
        raise ValueError(f"Invalid term: {term}")
    coef_str = match.group(1)
    coef = float(coef_str) if coef_str not in ('', '+', '-') else float(coef_str+'1')
    power = int(match.group(2))
    return power, coef

def parse_equation(eq):
    left, right = eq.split('=')
    terms = {}
    for term in re.split(r'(?=[+-])', left):
        if term.strip():
            power, coef = parse_term(term)
            terms[power] = terms.get(power, 0) + coef
    for term in re.split(r'(?=[+-])', right):
        if term.strip():
            power, coef = parse_term(term)
            terms[power] = terms.get(power, 0) - coef
    # Remove tiny floating point errors
    for k in terms:
        if abs(terms[k]) < 1e-12:
            terms[k] = 0.0
    return terms

def reduced_form_str(terms):
    items = []
    for power in sorted(terms.keys()):
        coef = terms[power]
        if coef == 0:
            continue
        coef_str = f"{coef:g}"  # removes unnecessary .0
        sign = '+' if coef > 0 else '-'
        if items:
            items.append(f" {sign} {abs(float(coef_str))} * X^{power}")
        else:
            items.append(f"{coef_str} * X^{power}" if coef > 0 else f"- {abs(float(coef_str))} * X^{power}")
    if not items:
        items.append("0 * X^0")
    return " + ".join(items).replace('+ -', '- ') + " = 0"

def solve(terms):
    degree = max((power for power, coef in terms.items() if coef != 0), default=0)
    print("Reduced form:", reduced_form_str(terms))
    print("Polynomial degree:", degree)

    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return

    if degree == 0:
        if terms.get(0, 0) == 0:
            print("Any real number is a solution.")
        else:
            print("No solution.")
        return

    if degree == 1:
        a = terms.get(1, 0)
        b = terms.get(0, 0)
        solution = -b / a
        print("The solution is:")
        print(f"{solution:g}")
        return

    if degree == 2:
        a = terms.get(2, 0)
        b = terms.get(1, 0)
        c = terms.get(0, 0)
        delta = b**2 - 4*a*c
        if delta > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            x1 = (-b + delta**0.5)/(2*a)
            x2 = (-b - delta**0.5)/(2*a)
            print(f"{x1:g}")
            print(f"{x2:g}")
        elif delta == 0:
            print("Discriminant is zero, the solution is:")
            x = -b / (2*a)
            print(f"{x:g}")
        else:
            print("Discriminant is strictly negative, the two complex solutions are:")
            real = -b / (2*a)
            imag = (abs(delta)**0.5)/(2*a)
            print(f"{real:g} + {imag:g}i")
            print(f"{real:g} - {imag:g}i")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a polynomial equation of degree ≤ 2.")
    parser.add_argument("equation", nargs='?', help='Polynomial equation e.g. "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"')
    args = parser.parse_args()

    if args.equation:
        eq = args.equation
    else:
        eq = input("Enter an equation: ")

    try:
        terms = parse_equation(eq)
        solve(terms)
    except Exception as e:
        print("Error:", e)
