"""EWFS circuit."""
import random
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

from wigners_friend.observer import Observer
from wigners_friend.setting import Setting

from wigners_friend.config import (
    ALICE, BOB, ALICE_SIZE, BOB_SIZE,
    MEAS_SIZE, 
    PEEK, REVERSE_1, REVERSE_2,
    ANGLES, BETA,
    SYS_SIZE,
)


def prepare_bipartite_system(qc: QuantumCircuit):
    """Generates the state: 1/sqrt(2) * (|01> - |10>)"""
    qc.x(ALICE)
    qc.x(BOB)
    qc.h(ALICE)
    qc.cx(ALICE, BOB)


def cnot_ladder(qc: QuantumCircuit, observer: Observer, friend_qubit: int, friend_size: int):
    """CNOT ladder circuit (GHZ without Hadamard)."""
    for i in range(friend_size):
        qc.cx(observer, friend_qubit + i)


def ewfs_rotation(qc: QuantumCircuit, qubit: int, angle: float):
    qc.rz(-angle, qubit)
    qc.h(qubit)
    

def apply_setting(
    qc: QuantumCircuit,
    observer: Observer,
    setting: Setting,
    angle: float,
    charlie_size: int,
    debbie_size: int
):
    """Apply either the PEEK or REVERSE_1/REVERSE_2 settings."""
    charlie_qubits = range(SYS_SIZE, (SYS_SIZE + charlie_size))
    debbie_qubits = range(SYS_SIZE + charlie_size, SYS_SIZE + (charlie_size + debbie_size))

    # Alice is the friend of Charlie and Bob is the friend of Debbie.
    friend_qubits = charlie_qubits if observer is ALICE else debbie_qubits
    friend_size = charlie_size if observer is ALICE else debbie_size
    
    if setting is PEEK:
        # Ask friend for the outcome. We pick a random qubit from friend's register.
        random_offset = random.randint(0, friend_size - 1)
        qc.measure(friend_qubits[0] + random_offset, observer)

    elif setting in [REVERSE_1, REVERSE_2]:
        cnot_ladder(qc, observer, friend_qubits[0], friend_size)

        # For either REVERSE_1 or REVERSE_2, apply the appropriate angle rotations.
        # Note that in this case, the rotation should occur on the observer's qubit.
        if observer is ALICE:
            qc.h(0)
            qc.rz(ANGLES[1], 0)        

        if observer is BOB:
            qc.h(1)        
            qc.rz((BETA - ANGLES[1]), 1)
        ewfs_rotation(qc, observer, angle)            
        qc.measure(observer, observer)
        

def ewfs(
    alice_setting: Setting,
    bob_setting: Setting,
    angles: list[float],
    beta: float,
    charlie_size: int,
    debbie_size: int
) -> QuantumCircuit:
    """Generate the circuit for extended Wigner's friend scenario."""    
    # Define quantum registers
    alice, bob, charlie, debbie = [
        QuantumRegister(size, name=name) 
        for size, name in zip([ALICE_SIZE, BOB_SIZE, charlie_size, debbie_size], 
                              ["Alice", "Bob", "Charlie", "Debbie"])
    ]
    measurement = ClassicalRegister(MEAS_SIZE, name="Measurement")
    
    # Create the Quantum Circuit with the defined registers
    qc = QuantumCircuit(alice, bob, charlie, debbie, measurement)
    
    # Prepare the bipartite quantum system
    prepare_bipartite_system(qc)
    qc.rz(-angles[1], 0)
    qc.h(0)
    
    qc.rz(-(beta - angles[1]), 1)
    qc.h(1)

    charlie_qubits = range(SYS_SIZE, (SYS_SIZE + charlie_size))
    debbie_qubits = range(SYS_SIZE + charlie_size, SYS_SIZE + (charlie_size + debbie_size))

    # Apply the CNOT ladder for Alice-Charlie and Bob-Debbie
    cnot_ladder(qc, ALICE, charlie_qubits[0], charlie_size)
    cnot_ladder(qc, BOB, debbie_qubits[0], debbie_size)

    # Apply the settings for Alice/Charlie and Bob/Debbie
    apply_setting(qc, ALICE, alice_setting, angles[alice_setting], charlie_size, debbie_size)
    apply_setting(qc, BOB, bob_setting, (beta - angles[bob_setting]), charlie_size, debbie_size)

    return qc
