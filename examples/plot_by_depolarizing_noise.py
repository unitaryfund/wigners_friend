import numpy as np
import qiskit
from qiskit_aer.noise import NoiseModel, depolarizing_error

from wigners_friend.config import ANGLES, BETA
from wigners_friend.stats import compute_inequalities
from wigners_friend.utils import generate_all_experiments
from wigners_friend.plots import plot_noise_levels_vs_violation


BACKEND = qiskit.Aer.get_backend("aer_simulator")
SHOTS = 10_000

violations = []
noise_levels = []
friend_size = 1
# Ranges from 0% -> 1% of noise.
for noise_level in np.linspace(0, 0.1, 11):
    NOISE_MODEL = NoiseModel()

    error = depolarizing_error(noise_level, 1)
    NOISE_MODEL.add_all_qubit_quantum_error(error, ["u1", "u2", "u3"])

    results = generate_all_experiments(
        backend=BACKEND,
        noise_model=NOISE_MODEL,
        shots=SHOTS,
        angles=ANGLES,
        beta=BETA,
        charlie_size=friend_size,
        debbie_size=friend_size,
    )
    violations.append(compute_inequalities(results, verbose=True))
    noise_levels.append(noise_level)

plot_noise_levels_vs_violation(noise_levels, violations, SHOTS, friend_size)