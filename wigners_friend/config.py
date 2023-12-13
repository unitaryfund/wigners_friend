"""Configuration file for EWFS circuit."""
import os
import numpy as np
import qiskit

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.test import mock
from qiskit_aer.noise import NoiseModel

from wigners_friend.observer import Observer
from wigners_friend.setting import Setting

####################################
# * Noise model and hardware.      *
####################################
USE_HARDWARE = False
USE_SIMULATOR = True
USE_NOISY_SIMULATOR = False

if USE_HARDWARE:
    IBM_PROVIDER_TOKEN = os.getenv("IBM_PROVIDER_TOKEN")
    # Save an IBM Quantum account and set it as your default account.
    QiskitRuntimeService.save_account(channel="ibm_quantum", token=IBM_PROVIDER_TOKEN, set_as_default=True, overwrite=True)
    
    # Load saved credentials
    service = QiskitRuntimeService()
    BACKEND = service.backend("ibmq_kolkata")
    NOISE_MODEL = NoiseModel.from_backend(BACKEND)

if USE_SIMULATOR:
    BACKEND = qiskit.Aer.get_backend("aer_simulator")
    NOISE_MODEL = None

if USE_NOISY_SIMULATOR:
    BACKEND = mock.FakeKolkata()
    NOISE_MODEL = NoiseModel.from_backend(BACKEND)

# Sampling shots to run.
SHOTS = 100_000

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

# Size of the bipartite quantum system.
SYS_SIZE = ALICE_SIZE + BOB_SIZE

# Two output bits for Alice and Bob.
MEAS_SIZE = 2

# Angles and beta term used for Alice and Bob measurement operators from arXiv:1907.05607.
# Note that despite the fact that degrees are used, we need to convert this to radians.
ANGLES = {PEEK: np.deg2rad(168), REVERSE_1: np.deg2rad(0), REVERSE_2: np.deg2rad(118)}
BETA = np.deg2rad(175)
