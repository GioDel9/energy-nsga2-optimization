from src.simulator import EnergySimulator

def evaluate_objectives(battery_capacity):
    sim = EnergySimulator()
    result = sim.run_simulation(battery_capacity=battery_capacity)

    f1 = battery_capacity
    f2 = result["Total Grid Purchase"]

    return f1, f2
if __name__ == "__main__":
    cap,grid = evaluate_objectives(10.0)

    print("\n" + "="*40)
    print("  TEST FUNZIONE OBIETTIVO (NSGA-II)")
    print("="*40)
    print(f"🔹 Capacità testata (f1): {cap:.1f} kWh")
    print(f"🔹 Energia da rete (f2):  {grid:.2f} kWh")
    print("="*40 + "\n")