import random
from deap import base, creator, tools, algorithms
from src.objectives import evaluate_objectives

def run_optimization(pop_size=40, n_gen=25):
    # Configurazione fitness e individuo
    if not hasattr(creator, "FitnessMin"):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
    if not hasattr(creator, "Individual"):
        creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_battery", random.uniform, 1.0, 30.0)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_battery, n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def eval_wrapper(individual):
        individual[0] = max(1.0, min(30.0, individual[0]))
        return evaluate_objectives(individual[0])

    toolbox.register("evaluate", eval_wrapper)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0.0, sigma=2.0, indpb=0.5)
    toolbox.register("select", tools.selNSGA2)

    population = toolbox.population(n=pop_size)
    
    for ind in population:
        ind.fitness.values = toolbox.evaluate(ind)

    for gen in range(1, n_gen + 1):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.9, mutpb=0.2)
        for ind in offspring:
            if not ind.fitness.valid:
                ind.fitness.values = toolbox.evaluate(ind)
        population = toolbox.select(population + offspring, pop_size)

    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
    return pareto_front

if __name__ == "__main__":
    front = run_optimization()
    for i, ind in enumerate(front):
        print(f"Soluzione {i+1}: Batteria={ind[0]:.2f} kWh, Rete={ind.fitness.values[1]:.2f} kWh")