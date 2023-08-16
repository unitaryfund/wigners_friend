"""Extended Wigner's friend scenario.

References:
    - arXiv:1907.05607
    - https://www.wignersfriends.com/
"""
import cirq
import numpy as np


def alice_projector(x: int) -> np.ndarray:
    """Alice's projective measurement as defined in Eq. (23) in
    arXiv:1907.05607"""
    angles = [168, 0, 118]
    e0 = np.array([1, 0]).reshape(-1, 1)
    e1 = np.array([0, 1]).reshape(-1, 1)
    phi = 1/np.sqrt(2) * (e0 + np.exp(1j * angles[x]) * e1)

    proj = phi @ phi.conj().T
    
    return 2 * proj - e0 @ e0.conj().T - e1 @ e1.conj().T


def bob_projector(y: int) -> np.ndarray:
    """Bob's projective measurement as defined in Eq. (24) in
    arXiv:1907.05607"""
    angles = [168, 0, 118]
    beta = 175
    e0 = np.array([1, 0]).reshape(-1, 1)
    e1 = np.array([0, 1]).reshape(-1, 1)
    phi = 1/np.sqrt(2) * (e0 + np.exp(1j * (beta - angles[y])) * e1)

    proj = phi @ phi.conj().T
    
    return 2 * proj - e0 @ e0.conj().T - e1 @ e1.conj().T


class SingleQubitUnitary(cirq.Gate):
    """Custom single-qubit Unitary gate."""
    def __init__(self, single_qubit_gate: cirq.Circuit) -> None:
        super(SingleQubitUnitary, self)
        self.single_qubit_gate = single_qubit_gate

    def _num_qubits_(self) -> int:
        return cirq.num_qubits(self.single_qubit_gate)

    def _unitary_(self) -> np.ndarray:
        return cirq.unitary(self.single_qubit_gate)

    def _circuit_diagram_info_(self, _) -> str:
        return "U_b"


class MultiQubitUnitary(cirq.Gate):
    """Custom multi-qubit Unitary gate."""
    def __init__(self, multi_qubit_gate: cirq.Circuit) -> None:
        super(MultiQubitUnitary, self)
        self.multi_qubit_gate = multi_qubit_gate

    def __pow__(self, _) -> cirq.Circuit:
        """Overloading this allows us to take the inverse (conjugate transpose) of our custom gate."""
        return cirq.MatrixGate(cirq.unitary(self.multi_qubit_gate).conj().T)

    def _num_qubits_(self) -> int:
        return cirq.num_qubits(self.multi_qubit_gate)

    def _unitary_(self) -> np.ndarray:
        return cirq.unitary(self.multi_qubit_gate)

    def _circuit_diagram_info_(self, _) -> tuple[str]:
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
        friend: list[cirq.GridQubit],
        friend_key: str,
        sys: cirq.GridQubit,
        u_obs: MultiQubitUnitary) -> cirq.Circuit:
    """Peek procedure for Wigner's friend scenario."""
    circuit = cirq.Circuit()
    if friend_key == "a":
        circuit.append(cirq.Circuit(u_obs.on(*(friend + [sys]))))
    elif friend_key == "b":
        circuit.append(cirq.Circuit(u_obs.on(*([sys] + friend))))

    circuit.append(cirq.measure(sys, key=friend_key))
    return circuit


def reverse_friend(
        friend: list[cirq.GridQubit], 
        friend_key: str,
        sys: cirq.GridQubit,
        u_obs: MultiQubitUnitary,
        u_b: SingleQubitUnitary
) -> cirq.Circuit:
    """Reverse procedure for Wigner's friend scenario."""
    circuit = cirq.Circuit()
    if friend_key == "a":
        circuit.append(u_obs.on(*(friend + [sys])))
        circuit.append(cirq.inverse(u_obs.on(*(friend + [sys]))))
    elif friend_key == "b":
        circuit.append(u_obs.on(*([sys] + friend)))
        circuit.append(cirq.inverse(u_obs.on(*([sys] + friend))))

    circuit.append(u_b.on(sys))
    circuit.append(cirq.measure(sys, key=friend_key))
    return circuit


def extended_wigner_circuit(
        observer_circuit: cirq.Circuit,
        friend_setting_1: str,
        friend_setting_2: str,
    ) -> cirq.Circuit:
    """Generate the circuit for the extended Wigner's friend scenario with
    choice of either "peek" or "reverse" friend settings."""

    friend_settings = ["peek", "reverse_1", "reverse_2"]
    if not set([friend_setting_1, friend_setting_2]).issubset(set(friend_settings)):
        raise ValueError(f"Friend setting {friend_setting_1} or {friend_setting_2} not recognized.")

    num_qubits = cirq.num_qubits(observer_circuit)

    # TODO: These need to be calculate based on the settings passed in.
    reverse_1_circuit = SingleQubitUnitary(rotation(168))
    reverse_2_circuit = SingleQubitUnitary(rotation(118))

    # Charlie and first part of bipartite system.
    charlie = [cirq.GridQubit(0, i) for i in range(num_qubits-1)]
    sys_1 = cirq.GridQubit(0, num_qubits-1)

    # Debbie and second part of bipartite system.
    sys_2 = cirq.GridQubit(1, 0)
    debbie = [cirq.GridQubit(1, i) for i in range(1, num_qubits)]

    # Define the experiment based on friend settings.
    circuit = state_prep(sys_1, sys_2)

    # Top portion of circuit (first friend setting).
    match friend_setting_1:
        case "peek":
            circuit.append(peek_friend(charlie, "a", sys_1, observer_circuit))
        case "reverse_1":
            circuit.append(reverse_friend(charlie, "a", sys_1, observer_circuit, reverse_1_circuit))
        case "reverse_2":
            circuit.append(reverse_friend(charlie, "a", sys_1, observer_circuit, reverse_2_circuit))

    # Bottom portion of circuit (second friend setting).
    match friend_setting_2:
        case "peek":
            circuit.append(peek_friend(debbie, "b", sys_2, observer_circuit))
        case "reverse_1":
            circuit.append(reverse_friend(debbie, "b", sys_2, observer_circuit, reverse_1_circuit))
        case "reverse_2":
            circuit.append(reverse_friend(debbie, "b", sys_2, observer_circuit, reverse_2_circuit))

    return circuit


def expectation_value(circuit: cirq.Circuit, repetitions: int = 75) -> tuple[float, float]:
    """Run the circuit `repetitions` times and calculate the resulting expectation value."""
    result = cirq.Simulator().run(program=circuit, repetitions=repetitions)

    alice_expectation_value = sum(np.array(result.measurements["a"][:, 0])) / repetitions
    bob_expectation_value = sum(np.array(result.measurements["b"][:, 0])) / repetitions

    return alice_expectation_value, bob_expectation_value


def lf_facet_1(expectation_values: dict[str, float]) -> float:
    """Genuine LF facet 1 as defined in Equation (13) from arXiv:1907.05607.
    
    The inequality for this facet is defined in terms of expectation values:
        -<A_1> - <A_2> - <B_1> - <B_2> - <A_1 B_1> 
        - 2 <A_1 B_2> - 2 <A_2 B_1> + 2 <A_2 B_2>
        - <A_2 B_3> - <A_3 B_2> - <A_3 B_3> - 6 <= 0
    """
    a_1, a_2, a_3 = expectation_values["a_1"], expectation_values["a_2"], expectation_values["a_3"]
    b_1, b_2, b_3 = expectation_values["b_1"], expectation_values["b_2"], expectation_values["b_3"]
    return -a_1 - a_2 - b_1 - b_2 - a_1 * b_1 \
        - 2 * a_1 * b_2 - 2 * a_2 * b_1 + 2 * a_2 * b_2 \
        - a_2 * b_3 - a_3 * b_2 - a_3 * b_3 - 6


def lf_facet_2(expectation_values: dict[str, float]) -> float:
    """Genuine LF facet 2 as defined in Equation (14) from arXiv:1907.05607.
    
    The inequality for this facet is defined in terms of expectation values:
        -<A_1> - <A_2> - <A_3> - <B_1> 
        -<A_1 B_1> - <A_2 B_1> - <A_3 B_1> - 2 <A_1 B_2>
        +<A_2 B_2> + <A_3 B_2> - <A_2 B_3> + <A_3 B_3> - 5 <= 0
    """
    a_1, a_2, a_3 = expectation_values["a_1"], expectation_values["a_2"], expectation_values["a_3"]
    b_1, b_2, b_3 = expectation_values["b_1"], expectation_values["b_2"], expectation_values["b_3"]
    return -a_1 - a_2 - a_3 - b_1 \
        -a_1 * b_1 - a_2 * b_1 - a_3 * b_1 - 2 * a_1 * b_2 \
        + a_1 * b_2 + a_3 * b_2 - a_2 * b_3 + a_3 * b_3 - 5


def positivity_facet_1_1(expectation_values: dict[str, float]) -> float:
    """Positivity facet from Eq (19)."""
    a_1, b_1 = expectation_values["a_1"], expectation_values["b_1"]
    return 1 + a_1 + b_1 + a_1 * b_1


if __name__ == "__main__":
    # Define observer circuit for protocol.
    observer_circuit = MultiQubitUnitary(cnot_ladder(2))

    # Calculate expectation values:
    a_1, b_1 = expectation_value(extended_wigner_circuit(observer_circuit, "peek", "peek"))
    a_2, b_2 = expectation_value(extended_wigner_circuit(observer_circuit, "reverse_1", "reverse_1"))
    a_3, b_3 = expectation_value(extended_wigner_circuit(observer_circuit, "reverse_2", "reverse_2"))

    # Sub-indices define the friend settings used, namely:
    #   1: Peek
    #   2: Reverse 1
    #   3: Reverse 2
    expectation_values = {
        "a_1": a_1, "a_2": a_2, "a_3": a_3,
        "b_1": b_1, "b_2": b_2, "b_3": b_3,
    }

    # Check LF facet violations:
    #print(f"Is LF-1 inequality violated: {lf_facet_1(expectation_values)}")
    #print(f"Is LF-2 inequality violated: {lf_facet_2(expectation_values)}")

    print(1 + a_1 + b_1 + a_1 * b_1)
    