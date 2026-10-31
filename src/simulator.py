import pandas as pd
import numpy as np
import os

class EnergySimulator:
    def __init__(self, load_file="data/load_profile_sample.csv", solar_file="data/solar_generation_profile.csv"):
        #Inizializza il simulatore caricando i profili energetici dai file CSV.
        if not os.path.exists(load_file) or not os.path.exists(solar_file):
            raise FileNotFoundError("I file di dati non sono stati trovati nella cartella 'data/'. Esegui prima generate_data.py o inserisci il tuo valore di dati nella cartella!")

        self.load_df = pd.read_csv(load_file)
        self.solar_df = pd.read_csv(solar_file)

    def run_simulation(self, battery_capacity=10.0):
        load = self.load_df['load_demand_kW'].values
        solar = self.solar_df['solar_generation_kW'].values
        hours = len(load)

        soc = 0.0 #State of Charge, ricarica della batteria
        grid_purchas_total = 0.0 #energia prelevata dalla batteria
        energy_deficit_total = 0.0 #energia in deficit
        surrendered_energy = 0.0 #energia immessa in rete (sprecata)

        for i in range(hours):
            net_power = solar[i] - load[i] #Positivo = surplus, Negativo = Deficit

            if net_power >= 0:
                space_battery = battery_capacity - soc
                abs_battery = min(net_power, space_battery)
                soc += abs_battery

                surrendered_energy += abs_battery
            else:
                deficit = abs(net_power)
                drawn_battery = min(deficit,soc)
                soc -= drawn_battery

                unmet_load = deficit - drawn_battery

                if unmet_load > 0:
                    grid_purchas_total += unmet_load
                    energy_deficit_total += unmet_load

        results = {
            "Total Grid Purchase": grid_purchas_total,
            "Total Deficit": energy_deficit_total,
            "Total Surplus": surrendered_energy,
            "Final Battery": soc
        

        }

        return results
if __name__ == "__main__":

    sim = EnergySimulator()
    res = sim.run_simulation(battery_capacity = 10.0)

    print("\n" + "="*40)
    print("  RISULTATI SIMULAZIONE ENERGETICA (1 Anno)")
    print("="*40)
    print(f"🔸 Deficit energetico non coperto: {res['Total Deficit']:.2f} kWh")
    print(f"☀️ Surplus immesso in rete:       {res['Total Surplus']:.2f} kWh")
    print(f"🔋 Stato carica finale batteria: {res['Final Battery']:.2f} kWh")
    print("="*40 + "\n")