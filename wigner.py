"""Extended Wigner's friend scenario.

References:
    - arXiv:1907.05607
    - https://www.wignersfriends.com/
"""
from typing import Optional
import cirq
import numpy as np


class SingleQubitUnitary(cirq.Gate):
    """Custom single-qubit Unitary gate."""
    def __init__(self, single_qubit_gate):
        super(SingleQubitUnitary, self)
        self.single_qubit_gate = single_qubit_gate

    def _num_qubits_(self):
        return cirq.num_qubits(self.single_qubit_gate)

    def _unitary_(self):
        return cirq.unitary(self.single_qubit_gate)

    def _circuit_diagram_info_(self, _):
        return "U_b"


class MultiQubitUnitary(cirq.Gate):
    """Custom two-qubit Unitary gate."""
    def __init__(self, multi_qubit_gate):
        super(MultiQubitUnitary, self)
        self.multi_qubit_gate = multi_qubit_gate

    def __pow__(self, other):
        """Overloading this allows us to take the inverse (conjugate transpose) of our custom gate."""
        return cirq.MatrixGate(cirq.unitary(self.multi_qubit_gate).conj().T)

    def _num_qubits_(self):
        return cirq.num_qubits(self.multi_qubit_gate)

    def _unitary_(self):
        return cirq.unitary(self.multi_qubit_gate)

    def _circuit_diagram_info_(self, _):
        return tuple(["@"] * (self._num_qubits_() - 1)) + tuple("U")


def cnot_ladder(num_qubits: int) -> cirq.Circuit: 
    """N-qubit CNOT ladder observer circuit."""
    qubits = cirq.LineQubit.range(num_qubits) 

    circuit = cirq.Circuit()
    for i in range(num_qubits - 1):
        layer = cirq.Circuit(cirq.CX(qubits[i], qubits[i+1]))
        circuit += layer
    return circuit


def rotation(angle: float) -> cirq.Circuit:
    """Rotation to pick some basis to measure.
    
    Distilled from Equations (23) and (24) from arXiv:1907.05607.
    """
    radians = 2 * np.deg2rad(angle)
    qubit = cirq.LineQubit(0)

    return cirq.Circuit(
        cirq.Rz(rads=radians).on(qubit),
    )


def state_prep(sys_1: cirq.GridQubit, sys_2: cirq.GridQubit) -> cirq.Circuit:
    """Generates the initial state of 1/sqrt(3) * (|00> + |01> + |10>)"""
    return cirq.Circuit(
        cirq.Ry(rads=2 * np.arccos(np.sqrt(2/3))).on(sys_1),
        cirq.Ry(rads=np.pi/4).on(sys_2),
        cirq.X(sys_1),
        cirq.CX(sys_1, sys_2),
        cirq.X(sys_1),
        cirq.Ry(rads=-np.pi/4).on(sys_2),
    )


def peek_friend(
        charlie: cirq.GridQubit,
        sys_1: cirq.GridQubit,
        u_obs: MultiQubitUnitary) -> cirq.Circuit:
    """Peek procedure for Wigner's friend between first part of bipartite system and Charlie."""
    return cirq.Circuit(
        u_obs.on(*(charlie + [sys_1])),
        cirq.measure(sys_1, key="a")
    )


def reverse_friend(
        debbie: cirq.GridQubit, 
        sys_2: cirq.GridQubit,
        u_obs: MultiQubitUnitary,
        u_b: SingleQubitUnitary
) -> cirq.Circuit:
    """Reverse procedure for Wigner's friend between second part of bipartite system and Debbie."""
    return cirq.Circuit(
        u_obs.on(*([sys_2] + debbie)),
        cirq.inverse(u_obs.on(*([sys_2] + debbie))),
        u_b.on(sys_2),
        cirq.measure(sys_2, key="b"),
    )


def extended_wigner_circuit(
        friend_setting_1: str,
        friend_setting_2: str,
        observer_circuit: cirq.Circuit,
        rotation_circuit: Optional[cirq.Circuit] = None
    ) -> cirq.Circuit:
    """Generate the circuit for the extended Wigner's friend scenario with
    choice of either "peek" or "reverse" friend settings."""

    friend_settings = ["peek", "reverse"]
    if not set([friend_setting_1, friend_setting_2]).issubset(set(friend_settings)):
        raise ValueError(f"Friend setting {friend_setting_1} or {friend_setting_2} not recognized.")

    num_qubits = cirq.num_qubits(observer_circuit)

    # Charlie and first part of bipartite system.
    charlie = [cirq.GridQubit(0, i) for i in range(num_qubits-1)]
    sys_1 = cirq.GridQubit(0, num_qubits-1)

    # Debbie and second part of bipartite system.
    sys_2 = cirq.GridQubit(1, 0)
    debbie = [cirq.GridQubit(1, i) for i in range(1, num_qubits)]

    # Define the experiment based on friend settings.
    circuit = state_prep(sys_1, sys_2)

    # Top portion of circuit (first friend setting).
    if friend_setting_1 == "peek":
        circuit.append(peek_friend(charlie, sys_1, observer_circuit))
    else:
        circuit.append(reverse_friend(debbie, sys_2, observer_circuit, rotation_circuit))

    # Bottom portion of circuit (second friend setting).
    if friend_setting_2 == "peek":
        circuit.append(peek_friend(charlie, sys_1, observer_circuit))
    else:
        circuit.append(reverse_friend(debbie, sys_2, observer_circuit, rotation_circuit))

    return circuit


def run():
    """Run simulation."""
    pass


if __name__ == "__main__":
    sim = cirq.Simulator()
    observer_circuit = MultiQubitUnitary(cnot_ladder(2))
    rotation_circuit = SingleQubitUnitary(rotation(168))

    circuit = extended_wigner_circuit("peek", "reverse", observer_circuit, rotation_circuit)
    num_qubits = observer_circuit._num_qubits_()

    print(f"Extended Wigner's friend circuit on {2 + num_qubits} qubits: \n")
    print(circuit)

    # Run simulations.
    repetitions = 75
    print(f"Simulating {repetitions} repetitions...")
    result = cirq.Simulator().run(program=circuit, repetitions=repetitions)

    print(f"Alice outcomes: {result.histogram(key='a')}")
    print(f"Bob outcomes: {result.histogram(key='b')}")
