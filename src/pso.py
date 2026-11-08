import numpy as np
from src.objectives import evaluate_objectives

CAPEX_BATTERY_PER_KWH = 500.0  # Costo reale installato [€/kWh]
BATTERY_LIFETIME_YEARS = 10.0  # Vita utile [anni]
OPEX_GRID_PER_KWH = 0.30  # Prezzo energia da rete [€/kWh]


def economic_cost_function(x):
  battery_capacity = x[0]
  f1, f2 = evaluate_objectives(battery_capacity)

  annual_capex = (CAPEX_BATTERY_PER_KWH * f1) / BATTERY_LIFETIME_YEARS
  annual_opex = OPEX_GRID_PER_KWH * f2

  return annual_capex + annual_opex


print("Avvio Particle Swarm Optimization (PSO)...")

np.random.seed(42)
n_particles = 30
dimensions = 1
max_iter = 30

positions = np.random.uniform(0.0, 50.0, (n_particles, dimensions))
velocities = np.random.uniform(-1.0, 1.0, (n_particles, dimensions))

personal_best_positions = positions.copy()
personal_best_scores = np.array([economic_cost_function(p) for p in positions])

global_best_idx = np.argmin(personal_best_scores)
global_best_position = personal_best_positions[global_best_idx].copy()
global_best_score = personal_best_scores[global_best_idx]

w = 0.5
c1 = 1.5
c2 = 1.5
history = [global_best_score]

for iteration in range(max_iter):
  r1 = np.random.rand(n_particles, dimensions)
  r2 = np.random.rand(n_particles, dimensions)

  velocities = (w * velocities+ c1 * r1 * (personal_best_positions - positions)+ c2 * r2 * (global_best_position - positions))
  positions += velocities
  positions = np.clip(positions, 0.0, 50.0)

  for i in range(n_particles):
    score = economic_cost_function(positions[i])
    if score < personal_best_scores[i]:
      personal_best_scores[i] = score
      personal_best_positions[i] = positions[i].copy()
      if score < global_best_score:
        global_best_score = score
        history.append(global_best_score)
        global_best_position = positions[i].copy()

pso_cap = global_best_position[0]
pso_cost = global_best_score
print("\n--- RISULTATI PARTICLE SWARM OPTIMIZATION (PSO) ---")
print(f"Capacità Batteria Ottimale: {pso_cap:.4f} kWh")
print(f"Costo Totale Annuo Minimo (J): € {pso_cost:,.4f}")