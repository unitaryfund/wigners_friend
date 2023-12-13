import matplotlib.pyplot as plt


def plot_friend_size_vs_violation(friend_sizes: list[int], violations: dict[str, float], shots: int):
    keys_values = {}
    for d in violations:
        for key, value in d.items():
            keys_values.setdefault(key, []).append(value)

    plt.plot(friend_sizes, keys_values["lf"], marker="o", label="LF")
    plt.plot(friend_sizes, keys_values["I3322"], marker="s", label="I3322")
    plt.plot(friend_sizes, keys_values["brukner"], marker="^", label="Brukner")
    plt.plot(friend_sizes, keys_values["semi_brukner"], marker="*", label="Semi-brukner")
    plt.plot(friend_sizes, keys_values["bell_non_lf"], marker="H", label="Bell non-LF")

    plt.axhline(y=0.0, color="r", linestyle="--", label="Violation threshold")

    plt.xlabel("Friend size (qubits)")
    plt.ylabel("LHS inequality value")
    plt.title(f"Friend size vs. inequality value (IBM (Fake) Kolkata) w/{shots} shots")
    plt.xticks(friend_sizes)
    plt.legend()
    plt.show()


def plot_noise_levels_vs_violation(
    noise_levels: list[float],
    violations: dict[str, float],
    shots: int,
    friend_size: int
):
    keys_values = {}
    for d in violations:
        for key, value in d.items():
            keys_values.setdefault(key, []).append(value)

    plt.plot(noise_levels, keys_values["lf"], marker="o", label="LF")
    plt.plot(noise_levels, keys_values["I3322"], marker="s", label="I3322")
    plt.plot(noise_levels, keys_values["brukner"], marker="^", label="Brukner")
    plt.plot(noise_levels, keys_values["semi_brukner"], marker="*", label="Semi-brukner")
    plt.plot(noise_levels, keys_values["bell_non_lf"], marker="H", label="Bell non-LF")

    plt.axhline(y=0.0, color="r", linestyle="--", label="Violation threshold")

    plt.xlabel("Depolarizing noise level")
    plt.ylabel("LHS inequality value")
    plt.title(f"Noise level vs. inequality value (shots={shots} / friend_size={friend_size})")
    plt.xticks(noise_levels)
    plt.legend()
    plt.show()