from typing import Union

def mod(n: Union[int, float], m: Union[int, float]) -> Union[int, float]:
    return ((n % m) + m) % m

def clamp(number, low, high):
    return max(low * 1.0, min(number * 1.0, high * 1.0))
