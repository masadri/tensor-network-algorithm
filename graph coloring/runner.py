import sys
import numpy as np
from subprocess import call

def generate_graph(n):
    indices = np.arange(n * n)
    edgeCount = np.random.randint(0, n * (n - 1) // 2)
    print(edgeCount)
    np.random.shuffle(indices)
    G = np.zeros((n, n))
    print(G.shape)
    ptr = 0
    while edgeCount > 0 and ptr < n * n:
        u, v = indices[ptr] // n, indices[ptr] % n
        if u == v or G[u, v] == 1:
            ptr += 1
            continue
        ptr += 1
        edgeCount -= 1
        G[u][v] = G[v, u] = 1
    return G.astype(int)

def generate_graph_to_file(n, file_name = "./data/rng_graph.txt"):
    indices = np.arange(n * n)
    edgeCount = np.random.randint(0, n * (n - 1) // 2)
    np.random.shuffle(indices)
    G = np.zeros((n, n))
    f = open(file_name, "w")
    f.write(str(n) + " " + str(edgeCount) + "\n")
    ptr = 0
    E = edgeCount
    while edgeCount > 0 and ptr < n * n:
        u, v = indices[ptr] // n, indices[ptr] % n
        if u == v or G[u, v] == 1:
            ptr += 1
            continue
        ptr += 1
        edgeCount -= 1
        G[u][v] = G[v, u] = 1
        f.write(str(u) + " " + str(v) + "\n")
    G = G.astype(int)
    f.close()
    return G, E

def work(file):
    #print("python main function")
    cmd = "deterministic_solver"
    #file_name = str(sys.argv).split()[1][1:-2]
    file_name = file
    call(["make", cmd]) # compilation
    output = call(["./" + cmd, file_name])

    f = open("output.txt", "r")
    data = f.read()
    return data
    
def prepare(file):
    data = work(file)
    items = data.split("\n")[2:-1]
    colors = []
    for line in items:
        value = int(line.split()[-1])
        colors.append(value)
    return colors

def get_max_clique(file):
    #print("python main function")
    cmd = "max_clique"
    #file_name = str(sys.argv).split()[1][1:-2]
    file_name = file
    call(["make", cmd]) # compilation
    output = call(["./" + cmd, file_name])

    f = open("clique_output.txt", "r")
    data = f.read()
    lines = data.split("\n")
    #print(lines)
    return int(lines[0].split()[-1]), int(lines[1].split()[-1])

def bound_quantum_chromatic_number(file):
    coloring = prepare(file)
    clique = get_max_clique(file)[0]
    return clique, max(coloring) + 1

def generate_and_bound(n):
    file = "./data/rng_graph.txt"
    G, E = generate_graph_to_file(n)
    coloring = prepare(file)
    clique = get_max_clique(file)[0]
    return clique, max(coloring) + 1, E, G

def get_laplacian(graph_file):
    f = open(graph_file)
    graph_data = f.read()
    f.close()
    original = graph_data.split("\n")
    n, m = map(int, original[0].split(' '))
    G = np.zeros((n, n))
    for i in range(1, len(original) - 1):
        chunk = original[i]
        u, v = map(int, chunk.split(' '))
        G[u, v] = G[v, u] = 1
    L = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                L[i, j] = np.sum(G[i], axis=0)
            elif G[i, j] == 1:
                L[i, j] = -1
            else:
                L[i, j] = 1
    return L.astype(int)

    