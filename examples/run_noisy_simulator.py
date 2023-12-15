import numpy as np
import qiskit
from qiskit.test import mock

from wigners_friend.config import ANGLES, BETA
from wigners_friend.stats import compute_inequalities
from wigners_friend.utils import generate_all_experiments


BACKEND = mock.FakeKolkata()
NOISE_MODEL = NoiseModel.from_backend(BACKEND)
SHOTS = 10_000
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