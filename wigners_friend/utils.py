import itertools
import qiskit
from qiskit.providers import Backend
from qiskit_aer.noise import NoiseModel

from wigners_friend.observer import Observer
from wigners_friend.ewfs_circuit import ewfs
from wigners_friend.config import SETTINGS
from wigners_friend.config import (
    ALICE, BOB,
    PEEK, REVERSE_1, REVERSE_2,
    SETTINGS,
)


def decode_results(results: dict[str, float], charlie_size: int, debbie_size: int) -> dict[str, float]:
    """Take majority vote of measurement bit-strings."""
    decoded_results = {}
    # For each setting, there is a dictionary of measurement results.
    for setting in results:
        if setting == (PEEK, PEEK) or setting == (PEEK, REVERSE_1) or setting == (PEEK, REVERSE_2):
            setting_results = {}
            # Decode the keys for each measurement result of the setting.
            for k, v in results[setting].items():
                alice_friend, bob_friend = k[:charlie_size], k[debbie_size:]

                alice_zero_count, bob_zero_count = alice_friend.count("0"), bob_friend.count("0")
                if setting[1] == PEEK:
                    alice_decoding = "0" if alice_zero_count >= charlie_size // 2 + 1 else "1"
                    bob_decoding = "0" if bob_zero_count >= debbie_size // 2 + 1 else "1"
                else:
                    alice_decoding = "0" if alice_zero_count >= charlie_size // 2 + 1 else "1"
                    bob_decoding = "0" if bob_zero_count >= 1 else "1"

                if alice_decoding + bob_decoding in setting_results.keys():
                    setting_results[alice_decoding + bob_decoding] += v
                else:
                    setting_results[alice_decoding + bob_decoding] = v
            decoded_results[setting] = setting_results


        elif setting == (REVERSE_1, PEEK) or setting == (REVERSE_2, PEEK):
            setting_results = {}
            # Decode the keys for each measurement result of the setting.
            for k, v in results[setting].items():
                alice_friend, bob_friend = k[:1], k[1:]

                alice_zero_count, bob_zero_count = alice_friend.count("0"), bob_friend.count("0")

                alice_decoding = "0" if alice_zero_count >= 1 else "1"
                bob_decoding = "0" if bob_zero_count >= debbie_size // 2 + 1 else "1"

 
                if alice_decoding + bob_decoding in setting_results.keys():
                    setting_results[alice_decoding + bob_decoding] += v
                else:
                    setting_results[alice_decoding + bob_decoding] = v
            decoded_results[setting] = setting_results

        else:
            decoded_results[setting] = results[setting]
            
    return decoded_results


def generate_all_experiments(
    backend: Backend,
    noise_model: NoiseModel,
    shots: float,
    angles: list[float],
    beta: float,
    charlie_size: int,
    debbie_size: int,
) -> dict[tuple[Observer, Observer], list[float]]:
    """Generate probabilities for all combinations of experimental settings."""
    all_experiment_combos = list(itertools.product(SETTINGS, repeat=2))
    
    results = {}
    for alice_setting, bob_setting in all_experiment_combos:
        ewfs_circuit = ewfs(
            alice_setting=alice_setting,
            bob_setting=bob_setting, 
            angles=angles,
            beta=beta,
            charlie_size=charlie_size,
            debbie_size=debbie_size
        )

        job = qiskit.execute(
            experiments=ewfs_circuit,
            backend=backend,
            noise_model=noise_model,
            basis_gates=noise_model.basis_gates if noise_model is not None else None,
            shots=shots,
        )
        counts = job.result().get_counts()
        
        # Convert counts to probabilities.
        probabilities = {key[::-1]: value / shots for key, value in counts.items()}

        results[(alice_setting, bob_setting)] = probabilities
    return results
