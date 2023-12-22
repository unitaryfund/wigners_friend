import os
from dotenv import load_dotenv

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_aer.noise import NoiseModel

from wigners_friend.config import ANGLES, BETA
from wigners_friend.stats import compute_inequalities
from wigners_friend.utils import generate_all_experiments

# Get the path to the directory this file is in
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Connect the path with your '.env' file name
load_dotenv(os.path.join(BASEDIR, "wigners_friend", ".env"))


IBM_PROVIDER_TOKEN = os.getenv("IBM_PROVIDER_TOKEN")

# Save an IBM Quantum account and set it as your default account.
QiskitRuntimeService.save_account(channel="ibm_quantum", token=IBM_PROVIDER_TOKEN, set_as_default=True, overwrite=True)

# Load saved credentials
service = QiskitRuntimeService()

# Put in whatever backend here you want.
BACKEND = service.backend("ibmq_kolkata")
NOISE_MODEL = NoiseModel.from_backend(BACKEND)
SHOTS = 1000
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
