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
      - its exponent (puissance) 2 
      - its coefficient (cofficient ) 5 

    Returns: (power, coef)
    """

    term = term.strip() # removes useless spaces 

    # Special case: the term is literally "0" 
    if term == '0':
        return 0, 0.0

    # Regex to extract:   coefficient * X^power
    # regex : 
    # ([+-]?\s*\d*\.?\d*) 
    #  [+-]?  capture    optional +- 
    # \s* optional spaces 
    # \d* optional digits 
    #  \.? optional decimal point 
    # \d*  optional digits after decimal 
    # this becomes match.group(1) since they are all wrapper in () 
    # \s*\*\s* matches * sign with optional spaces 
    # X\^(\d+) to match X^  \d is to take one or more digits after the ^  this becomes match group(2)
    # 

    match = re.match(r'([+-]?\s*\d*\.?\d*)\s*\*\s*X\^(\d+)', term.replace(' ', ''))

    if not match:
        raise ValueError(f"Invalid term: {term}")

    coef_str = match.group(1) # extract coeficient string 

    # If coef is empty :  "" or "+" or "-", it means  coef is : ±1 based on sign
    #   example:  "X^2" means 1 * X^2 
    coef = float(coef_str) if coef_str not in ('', '+', '-') else float(coef_str + '1')

    power = int(match.group(2))

    return power, coef


# -------------------------------------------------------------
#  PARSE THE WHOLE EQUATION INTO A DICTIONARY OF TERMS
# -------------------------------------------------------------
def parse_equation(eq):
    """
    Splits the equation into left and right, then moves everything to the left.
    Builds and returns  un dictionnaire Python 
        { power: coefficient }
    C'est l'equvalent d'un map [key] - value
    Si plusieurs term on la meme puissance , on soustrais ou additionne la puissance en 
    fonction de si le term est positif ou negatif 
    Example:
      "5 *x^0 + 4 * x^1 = 1 * x^0" 
      (5*x^0) + (4*x^1) - (1*x^0) = 0
      (5 - 1)*x^0 + 4*x^1 = 0
      4*x^0 + 4*x^1 = 0
      {0: 4.0, 1: 4.0,}
        
    """

    left, right = eq.split('=') # split the equation into left and right sides , using split on the
    terms = {}

    # --- Parse the left side, add coefficients ---
    for term in re.split(r'(?=[+-])', left): #  splits the string before every + or - sign. si il ny en as pas , ne split rien et continue 
        if term.strip(): # removes blank strings 
           # print(term)
            power, coef = parse_term(term)
            terms[power] = terms.get(power, 0) + coef
            #terms.get verifie si power existe deja dans le dictionnaire  si elle nexiste pas return 0
            # si oui : return le coef actuel  et addition ou soustrais en fonction le nouveaux coef 
            # Example :   "5 *x^0  = 1 * x^0" 
            # dans ce cas  les deux terms on la  meme puissance 
            # donc : terms[0] = terms.get(0,0)  - 1 
            # terms[0] =  5 - 1 = 4 
            # map : {0: 4.0} 
            # si non return 0 

    # --- Parse the right side, subtract coefficients (move to left) ---
    for term in re.split(r'(?=[+-])', right):
        if term.strip():
            #print(term)
            power, coef = parse_term(term)
            terms[power] = terms.get(power, 0) - coef

    # Remove floating-point noise
    # Floating-point arithmetic in Python can produce tiny errors: 
    # if the coefficient is extremely small (close to 0), treat it as 0. 
    for k in terms:
        if abs(terms[k]) < 1e-12: # abs : absolute value 
            terms[k] = 0.0

   # print (terms)
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

    for power in sorted(terms.keys()): # loop through powers in sorted order 
        coef = terms[power]
        if coef == 0:
            continue

        sign = "+" if coef > 0 else "-" # determine sign 
        abs_coef = abs(coef) # remove neg sign sign we alreaady  putted it in sign variable 

        # First term: no leading "+"
        if not parts: # if its the first term dont aadd the + sign to the equation (i use  abs_coef) if its positive ,  if its neg add it 
            parts.append(f"{abs_coef:g} * X^{power}" if coef > 0 else f"- {abs_coef:g} * X^{power}")
        else:
            parts.append(f"{sign} {abs_coef:g} * X^{power}")

    # if all coefs are 0 , return the canonical form for the zero polynomial 
    if not parts:
        return "0 * X^0 = 0"
    # join all parts and add = 0 for the canonical reduced form 
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
    solves(terms) takes a dictionnary {power:coef}
    Example : 
    {0: 4, 1: 3, 2: -1}
    which represents this equation
    -1*X² + 3*X + 4 = 0
    """

    degree = max((power for power, coef in terms.items() if coef != 0), default=0)
    #  looks at every degree in the dict , ignoring terms with coef 0
    # take the highest power that  has a non zero coeficient 
    # highest power = degree of euation 

    print("Reduced form:", reduced_form_str(terms))
    print("Polynomial degree:", degree)

    # ------------------- DEGREE > 2 -------------------
    if degree > 2: # not asked by the subject to slove 
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
    # degree 1 equation looks like : 
    # aX + b = 0
    # Example  : 
    # 3x + 6 = 0
    #x = -6/3 = -2


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
        nargs='?', # optional 
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
