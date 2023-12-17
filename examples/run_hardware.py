import numpy as np
import qiskit

from wigners_friend.config import ANGLES, BETA
from wigners_friend.stats import compute_inequalities
from wigners_friend.utils import generate_all_experiments


IBM_PROVIDER_TOKEN = os.getenv("IBM_PROVIDER_TOKEN")

# Save an IBM Quantum account and set it as your default account.
QiskitRuntimeService.save_account(channel="ibm_quantum", token=IBM_PROVIDER_TOKEN, set_as_default=True, overwrite=True)

# Load saved credentials
service = QiskitRuntimeService()
BACKEND = service.backend("ibmq_kolkata")
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
