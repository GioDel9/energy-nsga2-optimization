import random
import numpy as np
from deap import base, creator, tools, algorithms

from src.objectives import evaluate_objectives

if not hasattr(creator, "FitnessMin"):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("attr_capacity", random.uniform, 0.0, 50.0)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_capacity, n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    battery_capacity = max(0.0, individual[0])
    individual[0] = battery_capacity 
    
    f1, f2 = evaluate_objectives(battery_capacity)
    return f1, f2

toolbox.register("evaluate", evaluate)

toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0.0, sigma=2.0, indpb=0.2)
toolbox.register("select", tools.selNSGA2)

def run_optimization(pop_size=40, n_gen=25, cxpb=0.638, mutpb=0.161):
    population = toolbox.population(n=pop_size)
    
    final_pop, logbook = algorithms.eaMuPlusLambda(population, toolbox, mu=pop_size, lambda_=pop_size, cxpb=cxpb, mutpb=mutpb, ngen=n_gen, verbose=False)
    
    pareto_front = tools.sortNondominated(final_pop, len(final_pop), first_front_only=True)[0]
    return pareto_front

if __name__ == "__main__":
    print("Avvio della run definitiva di ottimizzazione NSGA-II...")
    
    optimal_front = run_optimization(pop_size=40, n_gen=25, cxpb=0.638, mutpb=0.161)
    
    print(f"\nOttimizzazione completata!")
    print(f"Individui sul Fronte di Pareto: {len(optimal_front)}")
    
    print("\n--- SOLUZIONI DEL FRONTE DI PARETO ---")
    for i, ind in enumerate(optimal_front):
        print(f"Soluzione {i+1}: Capacità Batteria = {ind.fitness.values[0]:.2f} kWh | Energia da Rete = {ind.fitness.values[1]:.2f} kWh")