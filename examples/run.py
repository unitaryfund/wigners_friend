from wigners_friend.config import (ANGLES, BETA, BACKEND, NOISE_MODEL, SHOTS)
from wigners_friend.stats import compute_inequalities
from wigners_friend.utils import generate_all_experiments


results = generate_all_experiments(backend=BACKEND, noise_model=NOISE_MODEL, shots=SHOTS, angles=ANGLES, beta=BETA)
print(compute_inequalities(results, verbose=True))