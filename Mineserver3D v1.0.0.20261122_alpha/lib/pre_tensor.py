import math


def ten_judge(I: any, dim: int) -> bool | None:
    if isinstance(I, (list, int, float)) == False:
        return False
    elif isinstance(I, (int, float)):
        if dim != 0:
            return False
    elif type(I) == list:
        if len(I) == 0:
            return False
        if dim == 0:
            return False
        for e in range(len(I)):
            if ten_judge(I[e], dim - 1) == False:
                return False
            else:
                continue


def ten_size(I: list, dim: int) -> int:
    if dim == 1:
        O = len(I)
    else:
        s = []
        for e in range(len(I)):
            s.append(ten_size(I[e], dim - 1))
        O = max(s)
    return O


def zero_ten(dim: int, size: int) -> int | list:
    if dim == 0:
        return 0
    else:
        O = []
        for e in range(size):
            O.append(zero_ten(dim - 1, size))
        return O


def ten_f(I: list, dim: int, size: int) -> list:
    comp = size - len(I)
    if dim == 1:
        O = I + [0] * comp
    else:
        O = []
        for e1 in range(len(I)):
            O.append(ten_f(I[e1], dim - 1, size))
        for e2 in range(comp):
            O.append(zero_ten(dim - 1, size))
    return O


def ten_p(
    I1: int | float | list, I2: int | float | list, dim: int
) -> int | float | list:
    if dim == 0:
        O = I1 + I2
    else:
        O = []
        for e in range(len(I1)):
            O.append(ten_p(I1[e], I2[e], dim - 1))
    return O


def ten_ele_sum(I: list, dim: int) -> float:
    if dim == 1:
        O = 0
        for e in range(len(I)):
            O = O + I[e]
    else:
        O = 0
        for e in range(len(I)):
            O = O + ten_ele_sum(I[e], dim - 1)
    return O


def sca_ten_mul(
    I1: int | float, I2: int | float | list, dim: int
) -> int | float | list:
    if dim == 0:
        O = I1 * I2
    else:
        O = []
        for e in range(len(I2)):
            O.append(sca_ten_mul(I1, I2[e], dim - 1))
    return O


def ten_isclose(
    I1: int | float | list, I2: int | float | list, dim: int
) -> bool | None:
    if dim == 0:
        if not math.isclose(I1, I2):
            return False
    else:
        for e in range(len(I1)):
            if ten_isclose(I1[e], I2[e], dim - 1) == False:
                return False
            else:
                continue
