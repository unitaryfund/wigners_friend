import numpy as np
import qiskit

from wigners_friend.config import ANGLES, BETA
from wigners_friend.stats import compute_inequalities
from wigners_friend.utils import generate_all_experiments


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
print(violations)