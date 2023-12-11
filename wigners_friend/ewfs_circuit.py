from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

from wigners_friend.observer import Observer
from wigners_friend.setting import Setting

from wigners_friend.config import (
    ALICE, BOB, ALICE_SIZE, BOB_SIZE,
    DEBBIE_QUBITS, DEBBIE_SIZE,
    CHARLIE_QUBITS, CHARLIE_SIZE,
    MEAS_SIZE, 
    PEEK, REVERSE_1, REVERSE_2,
    ANGLES, BETA,
)


def prepare_bipartite_system(qc: QuantumCircuit):
    """Generates the state: 1/sqrt(2) * (|01> - |10>)"""
    qc.x(ALICE)
    qc.x(BOB)
    qc.h(ALICE)
    qc.cx(ALICE, BOB)


def cnot_ladder(qc: QuantumCircuit, observer: Observer, friend_qubit: int, friend_size: int, reverse: bool, internal_copy: bool):
    """CNOT ladder circuit (GHZ without Hadamard)."""
    if internal_copy:
        if reverse:
            for i in range(friend_size-1):
                qc.cx(friend_qubit + friend_size-2-i, friend_qubit+friend_size-1-i)
            qc.cx(observer, friend_qubit)
        else:
            qc.cx(observer, friend_qubit)
            for i in range(friend_size-1):
                qc.cx(friend_qubit+i, friend_qubit + i + 1)
    else:
        if reverse:
            for i in range(friend_size):
                qc.cx(observer, friend_qubit+friend_size-1-i)
        else:
            for i in range(friend_size):
                qc.cx(observer, friend_qubit + i)


def ewfs_rotation(qc: QuantumCircuit, qubit: int, angle: float):
    qc.rz(-angle, qubit)
    qc.h(qubit)
    

def apply_setting(qc: QuantumCircuit, observer: Observer, setting: Setting, angle: float, observer_creg: list[int] | int):
    """Apply either the PEEK or REVERSE_1/REVERSE_2 settings."""
    
    # Alice is the friend of Charlie and Bob is the friend of Debbie.
    friend_qubits = CHARLIE_QUBITS if observer is ALICE else DEBBIE_QUBITS
    friend_size = CHARLIE_SIZE if observer is ALICE else DEBBIE_SIZE
    
    if setting is PEEK:
        qc.measure(friend_qubits, observer_creg)

    elif setting in [REVERSE_1, REVERSE_2]:
        cnot_ladder(qc, observer, friend_qubits[0], friend_size, reverse=True, internal_copy=True)

        # For either REVERSE_1 or REVERSE_2, apply the appropriate angle rotations.
        # Note that in this case, the rotation should occur on the observer's qubit.
        if observer is ALICE:
            qc.h(0)
            qc.rz(ANGLES[1], 0)        

        if observer is BOB:
            qc.h(1)        
            qc.rz((BETA - ANGLES[1]), 1)
        ewfs_rotation(qc, observer, angle)            
        qc.measure(observer, observer_creg)
        

def ewfs(alice_setting: Setting, bob_setting: Setting, angles: list[float], beta: float) -> QuantumCircuit:
    """Generate the circuit for extended Wigner's friend scenario."""    
    # Define quantum registers
    alice, bob, charlie, debbie = [
        QuantumRegister(size, name=name) 
        for size, name in zip([ALICE_SIZE, BOB_SIZE, CHARLIE_SIZE, DEBBIE_SIZE], 
                              ["Alice", "Bob", "Charlie", "Debbie"])
    ]
    if alice_setting == PEEK and bob_setting == PEEK:
        measurement = ClassicalRegister(CHARLIE_SIZE + DEBBIE_SIZE, name="Measurement")
        alice_creg = list(range(CHARLIE_SIZE))
        bob_creg = list(range(CHARLIE_SIZE, CHARLIE_SIZE + DEBBIE_SIZE))
    elif (alice_setting == PEEK and bob_setting != PEEK):
        measurement = ClassicalRegister(CHARLIE_SIZE + 1, name="Measurement")
        alice_creg = list(range(CHARLIE_SIZE))
        bob_creg = CHARLIE_SIZE
    elif (alice_setting != PEEK and bob_setting == PEEK):
        measurement = ClassicalRegister(DEBBIE_SIZE + 1, name="Measurement")
        alice_creg = 0
        bob_creg = list(range(1, CHARLIE_SIZE + 1))
    else:
        measurement = ClassicalRegister(MEAS_SIZE, name="Measurement")
        alice_creg = 0
        bob_creg = 1
        
    # Create the Quantum Circuit with the defined registers
    qc = QuantumCircuit(alice, bob, charlie, debbie, measurement)
    
    # Prepare the bipartite quantum system
    prepare_bipartite_system(qc)
    qc.rz(-angles[1], 0)
    qc.h(0)
    
    qc.rz(-(beta - angles[1]), 1)
    qc.h(1)

    # Apply the CNOT ladder for Alice-Charlie and Bob-Debbie
    cnot_ladder(qc, ALICE, CHARLIE_QUBITS[0], CHARLIE_SIZE, reverse=False, internal_copy=True)
    cnot_ladder(qc, BOB, DEBBIE_QUBITS[0], DEBBIE_SIZE, reverse=False, internal_copy=True)

    # Apply the settings for Alice/Charlie and Bob/Debbie
    apply_setting(qc, ALICE, alice_setting, angles[alice_setting], alice_creg)
    apply_setting(qc, BOB, bob_setting, (beta - angles[bob_setting]), bob_creg)

    return qc
