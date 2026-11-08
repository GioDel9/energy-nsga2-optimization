import numpy as np
from objectives import evaluate_objectives
from scipy.optimize import differential_evolution

CAPEX_BATTERY_PER_KWH = 500.0
BATTERY_LIFETIME_YEARS = 10.0
OPEX_GRID_PER_KWH = 0.30


def economic_cost_function(x):
  battery_capacity = x[0]
  f1, f2 = evaluate_objectives(battery_capacity)
  return (
      (CAPEX_BATTERY_PER_KWH * f1) / BATTERY_LIFETIME_YEARS
  ) + (OPEX_GRID_PER_KWH * f2)


# Griglia di tuning per il Differential Evolution
strategies = ["best1bin", "rand1bin", "best2exp"]
pop_sizes = [10, 15, 50]

best_cost = float("inf")
best_params = {}

print("🧪 Avvio tuning iperparametri per Differential Evolution (DE)...")

for strat in strategies:
  for pop in pop_sizes:
    result_de = differential_evolution(economic_cost_function,bounds=[(0.0, 50.0)],strategy=strat,popsize=pop,maxiter=50,tol=1e-6,seed=42,)

    print(f"Strategy: {strat:<10} | PopSize: {pop:<3} --> Capacità:"f" {result_de.x[0]:.2f} kWh | Costo: € {result_de.fun:,.2f} | Iter:"f" {result_de.nit}")

    if result_de.fun < best_cost:
      best_cost = result_de.fun
      best_params = {"strategy": strat, "popsize": pop}

print("\n--- RISULTATI DEL TUNING DE ---")
print(f"Migliori iperparametri trovati: {best_params}")
print(f"Miglior costo registrato: € {best_cost:,.2f}")