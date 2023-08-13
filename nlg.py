from toqito.nonlocal_games.nonlocal_game import NonlocalGame

import numpy as np
num_a_in, num_a_out = 3, 2
num_b_in, num_b_out = 3, 2

prob_mat = np.array([[1/6, 0, 1/6],
                     [1/6, 1/6, 0],
                     [1/3, 0, 0]])
pred_mat = np.zeros(
    (num_a_out, num_b_out, num_a_in, num_b_in)
)

for a_alice in range(num_a_out):
    for b_bob in range(num_b_out):
        for x_alice in range(num_a_in):
            for y_bob in range(num_b_in):
                if a_alice ^ b_bob == x_alice * y_bob:
                    pred_mat[a_alice, b_bob, x_alice, y_bob] = 1

print(pred_mat)

chsh = NonlocalGame(prob_mat, pred_mat)
print(chsh.quantum_value_lower_bound())
print(chsh.commuting_measurement_value_upper_bound())
print(chsh.nonsignaling_value())
