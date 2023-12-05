"""X."""
import os
import numpy as np
from observer import Observer
from setting import Setting

import qiskit
from qiskit_ibm_runtime import QiskitRuntimeService


####################################
# * Noise model and hardware.      *
####################################
USE_HARDWARE = True

if USE_HARDWARE:
    IBM_PROVIDER_TOKEN = os.getenv("IBM_PROVIDER_TOKEN")
    # Save an IBM Quantum account and set it as your default account.
    QiskitRuntimeService.save_account(channel="ibm_quantum", token=IBM_PROVIDER_TOKEN, set_as_default=True, overwrite=True)
    
    # Load saved credentials
    service = QiskitRuntimeService()
    BACKEND = service.backend("ibmq_kolkata")
else:
    # Define the backend simulator or hardware.
    BACKEND = qiskit.Aer.get_backend("aer_simulator")

# Create an empty noise model
NOISE_MODEL = None

# Sampling shots to run.
SHOTS = 1000

####################################
# * EWFS configurational settings. *
####################################

# Experiment settings (peek, reverse_1, and reverse_2).
PEEK = Setting.PEEK.value
REVERSE_1 = Setting.REVERSE_1.value
REVERSE_2 = Setting.REVERSE_2.value
SETTINGS = [PEEK, REVERSE_1, REVERSE_2]

# "Super"-observers (Alice and Bob).
ALICE = Observer.ALICE.value
BOB = Observer.BOB.value
OBSERVERS = [ALICE, BOB]

# Alice and Bob share a bipartite system of equal size.
ALICE_SIZE = 1
BOB_SIZE = 1

# Size of the systems held by the "friends" (Charlie and Debbie).
CHARLIE_SIZE = 1
DEBBIE_SIZE = 1

# Size of the bipartite quantum system.
SYS_SIZE = ALICE_SIZE + BOB_SIZE

# Two output bits for Alice and Bob.
MEAS_SIZE = 2

# Size of entire circuit
CIRCUIT_SIZE = SYS_SIZE + CHARLIE_SIZE + DEBBIE_SIZE

# Ranges for Charlie and Debbie's qubits depending on the size of their systems:
CHARLIE_QUBITS = range(SYS_SIZE, (SYS_SIZE + CHARLIE_SIZE))
DEBBIE_QUBITS = range(SYS_SIZE + CHARLIE_SIZE, SYS_SIZE + (CHARLIE_SIZE + DEBBIE_SIZE))

# Angles and beta term used for Alice and Bob measurement operators from arXiv:1907.05607.
# Note that despite the fact that degrees are used, we need to convert this to radians.
ANGLES = {PEEK: np.deg2rad(168), REVERSE_1: np.deg2rad(0), REVERSE_2: np.deg2rad(118)}
BETA = np.deg2rad(175)
