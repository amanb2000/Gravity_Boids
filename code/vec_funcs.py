import math

def get_unit_a_to_b(a, b):
    """"""
    dist = get_dist(a, b)
    vec = get_a_to_b(a, b)

    for i in range(len(vec)):
        vec[i] /= dist

    return vec



def get_dist(a, b):
    """Computes the distance between a and b    """
    dx = a[0] - b[0]
    dy = a[1] - b[1]

    d = math.sqrt(dx**2 + dy**2)

    return d


def get_a_to_b(a, b):
    """Computes the vector that connects a -> b"""
    c = []

    for i in range(len(a)):
        c += [b[i] - a[i]]
    
    return c