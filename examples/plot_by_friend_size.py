import numpy as np
import qiskit
from qiskit.providers import fake_provider
from qiskit_aer.noise import NoiseModel, depolarizing_error

from wigners_friend.config import (ANGLES, BETA)
from wigners_friend.stats import compute_inequalities
from wigners_friend.utils import generate_all_experiments
from wigners_friend.plots import plot_friend_size_vs_violation, plot_noise_levels_vs_violation


BACKEND = fake_provider.FakeKolkata()
NOISE_MODEL = NoiseModel.from_backend(BACKEND)
SHOTS = 1000

friend_sizes = range(1, 4)
violations = []
for friend_size in friend_sizes:
    results = generate_all_experiments(
        backend=BACKEND,
        noise_model=NOISE_MODEL,
        shots=SHOTS,
        angles=ANGLES,
        beta=BETA,
        charlie_size=friend_size,
        debbie_size=friend_size
    )
    violations.append(compute_inequalities(results, verbose=True))
plot_friend_size_vs_violation(friend_sizes, violations, SHOTS)