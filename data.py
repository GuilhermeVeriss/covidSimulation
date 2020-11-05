scale = 1  # pixel/metros (1 pixel vale quantos metros?)


def to_pixel(n):
    n *= scale
    n = n + 1 - (n % 1)
    return int(n)







