import os
import numpy as np
import pandas as pd

os.makedirs("data", exist_ok=True)

np.random.seed(42)

# 8760 ore in un anno (2026)
hours = 8760
time_index = pd.date_range(start="2026-01-01", periods=hours, freq="h")

# 1. Generazione del profilo di carico (Consumo energetico in kW)
# Andamento ciclico giornaliero + rumore casuale
daily_cycle = np.sin(np.linspace(0, 2 * np.pi, 24)) * 1.0 + 2.0
base_load = np.tile(daily_cycle, hours // 24)
noise = np.random.normal(0, 0.5, hours)
load_profile = np.clip(base_load + noise, 0.5, 5.5)  # Valori tra 1 e 10 kW

df_load = pd.DataFrame({
    "timestamp": time_index, 
    "load_demand_kW": load_profile
})
df_load.to_csv("data/load_profile_sample.csv", index=False)

# 2. Generazione del profilo solare (Generazione FV in kW)
# Campana diurna dalle 6:00 alle 18:00
solar_profile = np.zeros(hours)
for i in range(hours):
    hour_of_day = i % 24
    if 6 <= hour_of_day <= 18:
        solar_profile[i] = 4.0 * np.sin(np.pi * (hour_of_day - 6) / 12) + np.random.normal(0, 0.2)
solar_profile = np.clip(solar_profile, 0.0, 5.0)  # Valori tra 0 e 5 kW

df_solar = pd.DataFrame({
    "timestamp": time_index, 
    "solar_generation_kW": solar_profile
})
df_solar.to_csv("data/solar_generation_profile.csv", index=False)

print("File CSV generati e ottimizzati con successo nella cartella 'data/'!")