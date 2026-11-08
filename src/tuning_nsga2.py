import random
import numpy as np
from deap import tools
from nsga2 import run_optimization

n_iter = 100
best_hypervolume = -1.0
best_params = {}

ref_point = [20.0, 12000.0]

print("Avvio del tuning con popolazione ridotta per testare la pressione selettiva...")

for i in range(n_iter):
    cxpb = random.uniform(0.5, 0.95)
    max_mutpb = min(0.4,1.0 - cxpb)
    if max_mutpb < 0.05:
        max_mutpb = 0.05
    mutpb = random.uniform(0.05, max_mutpb)
    
    pareto_front = run_optimization(pop_size=6, n_gen=5, cxpb=cxpb, mutpb=mutpb)
    
    if len(pareto_front) > 0:
        try:
            hv = tools.hypervolume(pareto_front, ref_point)
        except Exception:
            fits = np.array([ind.fitness.values for ind in pareto_front])
            sorted_pts = sorted(fits, key=lambda x: x[0])
            hv = 0.0
            prev_f1 = ref_point[0]
            for pt in sorted_pts:
                f1, f2 = pt[0], pt[1]
                width = prev_f1 - f1
                height = ref_point[1] - f2
                if width > 0 and height > 0:
                    hv += width * height
                prev_f1 = f1
    else:
        hv = 0.0
        
    print(f"[{i+1}/{n_iter}] cxpb: {cxpb:.3f}, mutpb: {mutpb:.3f} -> Hypervolume: {hv:.4f}")
    
    if hv > best_hypervolume:
        best_hypervolume = hv
        best_params = {"cxpb": cxpb, "mutpb": mutpb}

print("\n--- RISULTATI DEL TUNING ---")
print(f"Migliori iperparametri trovati: {best_params}")
print(f"Miglior Hypervolume registrato: {best_hypervolume:.4f}")