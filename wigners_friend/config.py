"""Configuration file for EWFS circuit."""
import numpy as np

from wigners_friend.observer import Observer
from wigners_friend.setting import Setting


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
