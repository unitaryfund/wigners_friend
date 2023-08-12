"""Extended Wigner's friend scenario."""
import cirq
import numpy as np


def bitstring(bits: str) -> str:
    return "".join("1" if e else "_" for e in bits)


class SingleQubitUnitary(cirq.Gate):
    """Custom single-qubit Unitary gate."""
    def __init__(self, single_qubit_gate):
        super(SingleQubitUnitary, self)
        self.single_qubit_gate = single_qubit_gate

    def _num_qubits_(self):
        return 1

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


def rotation_basis() -> cirq.Circuit:
    """Rotation to pick some basis to measure."""
    pass


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


if __name__ == "__main__":
    sim = cirq.Simulator()
    num_qubits = 2

    # For the sake of example, use a CNOT ladder circuit for U.
    u_obs = MultiQubitUnitary(cnot_ladder(num_qubits))
    u_b = SingleQubitUnitary(cirq.H)

    print("Simulate the circuit:")

    # Charlie and first part of bipartite system.
    charlie = [cirq.GridQubit(0, i) for i in range(num_qubits-1)]
    sys_1 = cirq.GridQubit(0, num_qubits-1)

    # Debbie and second part of bipartite system.
    sys_2 = cirq.GridQubit(1, 0)
    debbie = [cirq.GridQubit(1, i) for i in range(1, num_qubits)]

    circuit = state_prep(sys_1, sys_2)

    circuit.append(peek_friend(charlie, sys_1, u_obs))
    circuit.append(reverse_friend(debbie, sys_2, u_obs, u_b))

    print(circuit)

    results = sim.simulate(circuit)
    print(results)

    exit()

    # Run simulations.
    repetitions = 75
    print(f"Simulating {repetitions} repetitions...")
    result = cirq.Simulator().run(program=circuit, repetitions=repetitions)

    a = np.array(result.measurements["a"][:, 0])
    b = np.array(result.measurements["b"][:, 0])

    # Print data.
    print()
    print('Results')
    print('a:', bitstring(a))
    print('b:', bitstring(b))

    #circuit = cirq.Circuit(
    #    # State prep: generates the 1/sqrt(3) * (|00> + |01> + |10>) state.
    #    cirq.Ry(rads=2 * np.arccos(np.sqrt(2/3))).on(sys_1),
    #    cirq.Ry(rads=np.pi/4).on(sys_2),
    #    cirq.X(sys_1),
    #    cirq.CX(sys_1, sys_2),
    #    cirq.X(sys_1),
    #    cirq.Ry(rads=-np.pi/4).on(sys_2),

    #    # Peek friend:
    #    u_obs.on(*(charlie + [sys_1])),
    #    cirq.measure(sys_1, key="a"),

    #    # Reverse friend:
    #    u_obs.on(*([sys_2] + debbie)),
    #    cirq.inverse(u_obs.on(*([sys_2] + debbie))),
    #    u_b.on(sys_2),
    #    cirq.measure(sys_2, key="b"),
    #)