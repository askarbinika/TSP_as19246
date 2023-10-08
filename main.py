# -----------------------------------------------------------------------------
# Program: TSP ar SA algoritmu, as19246
# Author:  OpenAI ChatGPT 3
# Date: 08.10.2023
#
# Description:
# Programma risina TSP problēmu:
#   Dotas n mašīnas, kur katrai ir noteikts darba laiks.
#   Doti m klienti, laiks kad viņi ir pieejami, kā arī nepieciešamais laiks, lai nokļūtu no viena klienta līdz otram un līdz mašīnu depo.
#   Sastādīt maršrutu, kas apmeklē visus klientus un minimizē paterēto laiku.
#
# References:
# 1. Praktiskā kombinatoriālā optimizācija, 3.Lekcijā dotais SA algoritms
# 2. ChatGPT3
# -----------------------------------------------------------------------------
import random
import time

def read_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    machines, clients, paths = {}, {}, {}

    current_section = None
    for line in lines:
        if line.startswith("#"):
            if "Mašīnas" in line:
                current_section = "machines"
            elif "Klienti" in line:
                current_section = "clients"
            elif "Ceļš" in line:
                current_section = "paths"
        else:
            if current_section == "machines":
                machine_id, time_range = line.strip().split(": ")
                start_time, end_time = map(int, time_range.split("-"))
                machines[machine_id] = (start_time, end_time)
            elif current_section == "clients":
                client_id, time_range = line.strip().split(": ")
                start_time, end_time = map(int, time_range.split("-"))
                clients[client_id] = (start_time, end_time)
            elif current_section == "paths":
                path, time = line.strip().split("=")
                paths[path] = float(time)

    return machines, clients, paths

def cost(route, paths):
    total_cost = 0
    prev = 'A'
    for client in route:
        total_cost += paths.get(prev + client, float('inf'))
        prev = client
    total_cost += paths.get(route[-1] + 'A', float('inf'))
    return total_cost

def generate_neighbor(route):
    new_route = route[:]
    i, j = random.sample(range(len(route)), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

def simulated_annealing(initial_route, paths, max_iterations=10000, start_temperature=100, alpha=0.995):
    current_route = initial_route
    current_cost = cost(current_route, paths)
    best_route = current_route
    best_cost = current_cost
    temperature = start_temperature

    for iteration in range(max_iterations):
        neighbor = generate_neighbor(current_route)
        neighbor_cost = cost(neighbor, paths)
        cost_difference = neighbor_cost - current_cost

        if cost_difference < 0 or random.random() < (temperature / start_temperature):
            current_route = neighbor
            current_cost = neighbor_cost

            if current_cost < best_cost:
                best_route = current_route
                best_cost = current_cost

        temperature *= alpha

    return best_route, best_cost

if __name__ == "__main__":
    machines, clients, paths = read_data('data.txt')
    initial_route = list(clients.keys())
    
    start_time = time.time()
    best_route, best_cost = simulated_annealing(initial_route, paths)
    execution_time = time.time() - start_time

    print(f"Best route: {best_route}")
    print(f"Cost (or quality of solution): {best_cost}")
    print(f"Execution time: {execution_time} seconds")
