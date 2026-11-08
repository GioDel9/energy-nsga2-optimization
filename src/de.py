import numpy as np
from scipy.optimize import differential_evolution

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

bounds = [(0.0, 50.0)]

print("Avvio dell'ottimizzazione con Differential Evolution (DE)...")

result_de = differential_evolution(economic_cost_function,bounds=bounds,strategy="best1bin",maxiter=50,popsize=15,tol=1e-6,seed=42,)

print("\n--- RISULTATI DIFFERENTIAL EVOLUTION (DE) ---")
print(f"Capacità Batteria Ottimale: {result_de.x[0]:.4f} kWh")
print(f"Costo Totale Minimo (J): € {result_de.fun:,.4f}")
print(f"Numero di iterazioni eseguite: {result_de.nit}")

f1_base, f2_base = evaluate_objectives(0.0)
annual_opex_base = OPEX_GRID_PER_KWH * f2_base
costo_totale_base = annual_opex_base  # CapEx = 0

costo_totale_de = result_de.fun
risparmio_annuo = costo_totale_base - costo_totale_de
percentuale_risparmio = (risparmio_annuo / costo_totale_base) * 100

print("\n" + "=" * 50)
print("📊 CONFRONTO ECONOMICO: BASELINE VS DIFFERENTIAL EVOLUTION")
print("=" * 50)
print(f"🔸 Scenario Senza Batteria (Baseline): € {costo_totale_base:,.2f} /anno")
print(f"🔹 Scenario Ottimizzato (DE - {result_de.x[0]:.2f} kWh): € {costo_totale_de:,.2f} /anno")
print("-" * 50)
print(f"💰 Risparmio Economico Netto: € {risparmio_annuo:,.4f} all'anno")
print(f"📉 Riduzione della spesa energetica: {percentuale_risparmio:.2f}%")
print("=" * 50)