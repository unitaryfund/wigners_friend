# Known LHS violation values. Extracted from Excel file from `data/`
import numpy as np
import qiskit
import pytest

from wigners_friend.config import ANGLES, BETA
from wigners_friend.stats import compute_inequalities
from wigners_friend.utils import generate_all_experiments


lhs_violation_vals = {
    "mu": {
        "1": {
            "lf": 0.57028,
            "I3322": 0.299348,
            "brukner": 0.124336,
            "semi_brukner": 0.380364,
            "bell_non_lf": 0.59116
        }
    }
}


def test_violation_lhs():
    BACKEND = qiskit.Aer.get_backend("aer_simulator")
    SHOTS = 100_000
    NOISE_MODEL = None
    friend_size = 1

    results = generate_all_experiments(
        backend=BACKEND,
        noise_model=NOISE_MODEL,
        shots=SHOTS,
        angles=ANGLES,
        beta=BETA,
        charlie_size=friend_size,
        debbie_size=friend_size
    )
    violations = compute_inequalities(results)

    assert np.isclose(violations["lf"], lhs_violation_vals["mu"]["1"]["lf"], atol=0.1)
    assert np.isclose(violations["I3322"], lhs_violation_vals["mu"]["1"]["I3322"], atol=0.1)
    assert np.isclose(violations["brukner"], lhs_violation_vals["mu"]["1"]["brukner"], atol=0.1)
    assert np.isclose(violations["semi_brukner"], lhs_violation_vals["mu"]["1"]["semi_brukner"], atol=0.1)
    assert np.isclose(violations["bell_non_lf"], lhs_violation_vals["mu"]["1"]["bell_non_lf"], atol=0.1)
