def imsl_generator(N, seed):
    """
    Generador congruencial multiplicativo IMSL.

    """

    a = 16807
    m = 2**31 - 1

    if not isinstance(seed, int) or not (1 <= seed < m):
        raise ValueError("non valid seed.")

    X = seed
    random_numbers = []

    for _ in range(N):

        X = (a * X) % m

        U = X / m

        random_numbers.append(U)

    return random_numbers