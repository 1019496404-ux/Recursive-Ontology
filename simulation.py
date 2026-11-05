# ==========================================
# Recursive Ontology Simulation
# Author: Gangbei Niu
# Equation: S_n = f(S_{n-1}, W_n)
# ==========================================

import math
import random

def simulate_recursive_ontology(steps=10):
    """
    Simulates the state recursion equation S_n = f(S_{n-1}, W_n)
    and calculates the Triangle-Circle residual R(k) = 1 - cos(pi/k).
    """
    print("--- Initializing Recursive Ontology ---")
    
    # Initial State (S_0)
    S_prev = 0.0 
    
    for n in range(1, steps + 1):
        # Environmental Input (W_n) - simulated as random noise
        W_n = random.uniform(-1.0, 1.0)
        
        # Reaction Function (f) - simple linear combination with noise
        S_n = S_prev + (0.5 * W_n) 
        
        # Calculate the structural residual for the current depth n
        # Formula: R(k) = 1 - cos(pi/k)
        residual_R = 1 - math.cos(math.pi / n)
        
        print(f"Step {n}: S_n = {S_n:.4f} | Input W_n = {W_n:.4f} | Residual R({n}) = {residual_R:.4f}")
        
        # Update state for next recursion
        S_prev = S_n

if __name__ == "__main__":
    # Run the 72-hour Human-AI experiment simulation (abstracted to 10 steps for demo)
    simulate_recursive_ontology(steps=10)
