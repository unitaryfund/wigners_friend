from exp_vals import single_expect, double_expect
from config import (
    ALICE, BOB,
    PEEK, REVERSE_1, REVERSE_2,
)

def compute_inequalities(results, verbose=False):
    A1 = single_expect(ALICE, PEEK, results)
    B1 = single_expect(BOB, PEEK, results)

    A2 = single_expect(ALICE, REVERSE_1, results)
    B2 = single_expect(BOB, REVERSE_1, results)

    A3 = single_expect(ALICE, REVERSE_2, results)
    B3 = single_expect(BOB, REVERSE_2, results)

    A1B1 = double_expect((PEEK, PEEK), results)
    A1B2 = double_expect((PEEK, REVERSE_1), results)
    A1B3 = double_expect((PEEK, REVERSE_2), results)

    A2B1 = double_expect((REVERSE_1, PEEK), results)
    A2B2 = double_expect((REVERSE_1, REVERSE_1), results)
    A2B3 = double_expect((REVERSE_1, REVERSE_2), results)

    A3B1 = double_expect((REVERSE_2, PEEK), results)
    A3B2 = double_expect((REVERSE_2, REVERSE_1), results)
    A3B3 = double_expect((REVERSE_2, REVERSE_2), results)
    
    # Local-friendliness inequalities:
    # Eq. (13) from [1].
    lf_1 = -A1 - A2 - B1 - B2 - A1B1 - 2*A1B2 - 2*A2B1 + 2*A2B2 - A2B3 - A3B2 - A3B3 - 6
    # Eq. (14) from [1].
    lf_2 = -A1 - A2 - A3 - B1 - A1B1 - A2B1 - A3B1 - 2*A1B2 + A2B2 + A3B2 - A2B3 + A3B3 - 5
    # Eq. (15) from [1].
    lf_3 = -A1 + A2 + B1 - B2 + A1B1 - A1B2 - A1B3 - A2B1 + A2B2 - A2B3 - A3B1 - A3B2 - 4 
    # Eq. (16) from [1].
    lf_4 = -A2 - A3 - B2 - B3 - A1B2 + A1B3 - A2B1 - A2B2 - A2B3 + A3B1 - A3B2 - A3B3 - 4

    # Brukner inequalities:
    # Eq. (17) from [1].
    brukner = A1B1 - A1B3 - A2B1 - A2B3 - 2
    # Eq. (18) from [1].
    semi_brukner = -A1B2 + A1B3 - A3B2 - A3B3 - 2

    # Positivity inequalities:
    # Eq. (19) from [1].
    pos_1 = 1 + A1 + B1 + A1B1
    # Eq. (20) from [1].
    pos_2 = 1 + A1 + B2 + A1B2
    # Eq. (21) from [1].
    pos_3 = 1 + A2 + B2 + A2B2

    # Bell non-LF 
    # Eq. (22) from [1].
    bell_non_lf = A2B2 - A2B3 - A3B2 - A3B3 - 2
    
    if verbose:
        print("******Inequalities******")
        print(f"{semi_brukner=} -- is violated: {semi_brukner > 0}")
        print(f"{brukner=} -- is violated: {brukner > 0}")
        print(f"{lf_1=} -- is violated: {lf_1 > 0}")
        print(f"{lf_2=} -- is violated: {lf_2 > 0}")
        print(f"{lf_3=} -- is_violated: {lf_3 > 0}")
        print(f"{lf_4=} -- is_violated: {lf_4 > 0}")
        print(f"{bell_non_lf=} -- is_violated: {bell_non_lf > 0}")
        print("**************************")
        
        print("******Expectation values******")
        print(f"{A1=}")
        print(f"{A2=}")
        print(f"{A3=}")
        print(f"{B1=}")
        print(f"{B2=}")
        print(f"{B3=}")
        print(f"{A1B1=}")
        print(f"{A1B2=}")
        print(f"{A1B3=}")
        print(f"{A2B1=}")
        print(f"{A2B2=}")
        print(f"{A2B3=}")
        print(f"{A3B1=}")
        print(f"{A3B2=}")
        print(f"{A3B3=}")
        print("******************************")
