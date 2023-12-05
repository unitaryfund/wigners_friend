from config import (
    ALICE, BOB,
    CHARLIE_SIZE, DEBBIE_SIZE,
    SETTINGS,
    PEEK, REVERSE_1, REVERSE_2
)
from setting import Setting
from observer import Observer


def single_expect(observer: Observer, setting: Setting, results: dict):
    """Compute single expectation values for either Alice or Bob."""
    if observer is ALICE:
        ret = 0
        for settings in results.keys():
            if settings[ALICE] is setting:
                if setting == PEEK:
                    zero_la = "0" * CHARLIE_SIZE
                    one_la = "1" * CHARLIE_SIZE
                    zero_lb = "0" * DEBBIE_SIZE
                    one_lb = "1" * DEBBIE_SIZE
                    probs = results[settings]
                    # <A> = P(00) + P(01) - P(10) - P(11)
                    ret += (
                        probs.get(zero_la + "0", 0)
                        + probs.get(zero_la + "1", 0)
                        - probs.get(one_la + "0", 0)
                        - probs.get(one_la + "1", 0)
                        + probs.get(zero_la + zero_lb, 0)
                        + probs.get(zero_la + one_lb, 0)
                        - probs.get(one_la + zero_lb, 0)
                        - probs.get(one_la + one_lb, 0)
                    )
                else:
                    zero_lb = "0" * DEBBIE_SIZE
                    one_lb = "1" * DEBBIE_SIZE
                    probs = results[settings]
                    # <A> = P(00) + P(01) - P(10) - P(11)
                    ret += (
                        probs.get("00", 0)
                        + probs.get("01", 0)
                        - probs.get("10", 0)
                        - probs.get("11", 0)
                        + probs.get("0" + zero_lb, 0)
                        + probs.get("0" + one_lb, 0)
                        - probs.get("1" + zero_lb, 0)
                        - probs.get("1" + one_lb, 0)
                    )

        return ret / len(SETTINGS)
    else:
        ret = 0
        for settings in results.keys():
            if settings[BOB] is setting:
                if setting == PEEK:
                    zero_la = "0" * CHARLIE_SIZE
                    one_la = "1" * CHARLIE_SIZE
                    zero_lb = "0" * DEBBIE_SIZE
                    one_lb = "1" * DEBBIE_SIZE
                    probs = results[settings]
                    # <A> = P(00) - P(01) + P(10) - P(11)
                    ret += (
                        probs.get("0" + zero_lb, 0)
                        - probs.get("0" + one_lb, 0)
                        + probs.get("1" + zero_lb , 0)
                        - probs.get("1" + one_lb, 0)
                        + probs.get(zero_la + zero_lb, 0)
                        - probs.get(zero_la + one_lb, 0)
                        + probs.get(one_la + zero_lb, 0)
                        - probs.get(one_la + one_lb, 0)
                    )
                else:
                    zero_la = "0" * CHARLIE_SIZE
                    one_la = "1" * CHARLIE_SIZE
                    probs = results[settings]
                    # <A> = P(00) - P(01) + P(10) - P(11)
                    ret += (
                        probs.get("00", 0)
                        - probs.get("01", 0)
                        + probs.get("10", 0)
                        - probs.get("11", 0)
                        + probs.get(zero_la + "0", 0)
                        - probs.get(zero_la + "1", 0)
                        + probs.get(one_la + "0", 0)
                        - probs.get(one_la + "1", 0)
                    )
        return ret / len(SETTINGS)


def double_expect(settings: list[Setting], results: dict) -> float:
    """Expectation value of product of two operators."""
    probs = results[settings]
    if settings == (PEEK, REVERSE_1) or settings == (PEEK, REVERSE_2):
        # <AB> = P(00, 0) - P(00, 1) - P(11, 0) + P(11, 1) for logical qubit of size 2 of ALICE
        zero_l = "0" * CHARLIE_SIZE
        one_l = "1" * CHARLIE_SIZE
        return (
            probs.get(zero_l + "0", 0) 
            - probs.get(zero_l + "1", 0) 
            - probs.get(one_l + "0", 0) 
            + probs.get(one_l + "1", 0)
        )    
    elif settings == (REVERSE_1, PEEK) or settings == (REVERSE_2, PEEK):
        # <AB> = P(0,00) - P(0, 11) - P(1, 00) + P(1, 11) for logical qubit of size 2 of BOB
        zero_l = "0" * DEBBIE_SIZE
        one_l = "1" * DEBBIE_SIZE
        return (
            probs.get("0" + zero_l, 0) 
            - probs.get("0" + one_l, 0) 
            - probs.get("1" + zero_l, 0) 
            + probs.get("1" + one_l, 0)
        ) 
    elif settings == (PEEK, PEEK):
        # <AB> = P(00, 00) - P(00, 11) - P(11, 00) + P(11, 11) for logical qubit of size 2 of ALICE and BOB
        zero_la = "0" * CHARLIE_SIZE
        one_la = "1" * CHARLIE_SIZE
        zero_lb = "0" * DEBBIE_SIZE
        one_lb = "1" * DEBBIE_SIZE
        return (
            probs.get(zero_la + zero_lb, 0) 
            - probs.get(zero_la + one_lb, 0) 
            - probs.get(one_la + zero_lb, 0) 
            + probs.get(one_la + one_lb, 0)
        ) 
    else:
        # <AB> = P(0, 0) - P(0, 1) - P(1, 0) + P(1, 1)
        return (
            probs.get("00", 0) 
            - probs.get("01", 0) 
            - probs.get("10", 0) 
            + probs.get("11", 0)
        ) 
