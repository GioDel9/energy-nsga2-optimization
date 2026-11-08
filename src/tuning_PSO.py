import numpy as np
from objectives import evaluate_objectives

# Parametri economici di riferimento
CAPEX_BATTERY_PER_KWH = 500.0
BATTERY_LIFETIME_YEARS = 10.0
OPEX_GRID_PER_KWH = 0.30


def economic_cost_function(x):
  battery_capacity = x[0]
  f1, f2 = evaluate_objectives(battery_capacity)
  return ((CAPEX_BATTERY_PER_KWH * f1) / BATTERY_LIFETIME_YEARS) + (OPEX_GRID_PER_KWH * f2)

swarm_sizes = [15, 30, 50]
inertia_weights = [0.4, 0.7, 0.9]
cognitive_social = [(1.5, 1.5), (2.0, 2.0)]

best_pso_cost = float("inf")
best_pso_params = {}

print("🧪 Avvio tuning iperparametri per Particle Swarm Optimization (PSO)...")

for n_p in swarm_sizes:
  for w in inertia_weights:
    for c1, c2 in cognitive_social:
      np.random.seed(42)
      dimensions = 1
      max_iter = 30

      positions = np.random.uniform(0.0, 50.0, (n_p, dimensions))
      velocities = np.random.uniform(-1.0, 1.0, (n_p, dimensions))

      pbest_pos = positions.copy()
      pbest_scores = np.array([economic_cost_function(p) for p in positions])

      gbest_idx = np.argmin(pbest_scores)
      gbest_pos = pbest_pos[gbest_idx].copy()
      gbest_score = pbest_scores[gbest_idx]

      for iteration in range(max_iter):
        r1 = np.random.rand(n_p, dimensions)
        r2 = np.random.rand(n_p, dimensions)

        velocities = (w * velocities+ c1 * r1 * (pbest_pos - positions)+ c2 * r2 * (gbest_pos - positions))
        positions = np.clip(positions + velocities, 0.0, 50.0)

        for i in range(n_p):
          score = economic_cost_function(positions[i])
          if score < pbest_scores[i]:
            pbest_scores[i] = score
            pbest_pos[i] = positions[i].copy()
            if score < gbest_score:
              gbest_score = score
              gbest_pos = positions[i].copy()

      print(f"Particles: {n_p:<2} | w: {w} | c1,c2: ({c1},{c2}) --> Capacità:"f" {gbest_pos[0]:.2f} kWh | Costo: € {gbest_score:,.2f}")

      if gbest_score < best_pso_cost:
        best_pso_cost = gbest_score
        best_pso_params = {"n_particles": n_p,"inertia": w,"c1": c1,"c2": c2,}

print("\n--- RISULTATI DEL TUNING PSO ---")
print(f"Migliori iperparametri trovati: {best_pso_params}")
print(f"Miglior costo registrato: € {best_pso_cost:,.2f}")