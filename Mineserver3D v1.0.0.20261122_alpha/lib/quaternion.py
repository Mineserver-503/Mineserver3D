import math
import lib.tensor as tensor


def qua_judge(I: any) -> bool:
    if not tensor.ten_judge(I, 1):
        return False
    if not (len(I) == 4):
        return False
    return True


def qua_mod(I: list) -> float | None:
    if not qua_judge(I):
        return
    return tensor.vec_mod(I)


def qua_unit(I: list) -> list | None:
    # Extra Condition : qua_mod(I) != 0
    if not qua_judge(I):
        return
    if qua_mod(I) == 0:
        return
    return tensor.vec_unit(I)


def qua_arg(I: list) -> float | None:
    # Extra Condition : qua_mod(I) != 0
    if not qua_judge(I):
        return
    if qua_mod(I) == 0:
        return
    J = qua_unit(I)
    if J[0] > 1:
        i = 1
    elif J[0] < -1:
        i = -1
    else:
        i = J[0]
    return math.acos(i)


def qua_conj(I: list) -> list | None:
    if not qua_judge(I):
        return
    O = [I[0], -I[1], -I[2], -I[3]]
    return O


def qua_p(I1: list, I2: list) -> list | None:
    if not qua_judge(I1):
        return
    if not qua_judge(I2):
        return
    return tensor.ten_p(I1, I2, 1)


def qua_m(I1: list, I2: list) -> list | None:
    if not qua_judge(I1):
        return
    if not qua_judge(I2):
        return
    return tensor.ten_m(I1, I2, 1)


def sca_qua_mul(I1: int | float, I2: list) -> list | None:
    if not tensor.ten_judge(I1, 0):
        return
    if not qua_judge(I2):
        return
    return tensor.sca_ten_mul(I1, I2, 1)


def qua_opp(I1: list) -> list | None:
    if not qua_judge(I1):
        return
    return tensor.ten_opp(I1, 1)


def qua_mul(I1: list, I2: list) -> list | None:
    if not qua_judge(I1):
        return
    if not qua_judge(I2):
        return
    O = []
    O.append(I1[0] * I2[0] - I1[1] * I2[1] - I1[2] * I2[2] - I1[3] * I2[3])
    O.append(I1[0] * I2[1] + I1[1] * I2[0] + I1[2] * I2[3] - I1[3] * I2[2])
    O.append(I1[0] * I2[2] - I1[1] * I2[3] + I1[2] * I2[0] + I1[3] * I2[1])
    O.append(I1[0] * I2[3] + I1[1] * I2[2] - I1[2] * I2[1] + I1[3] * I2[0])
    return O


def qua_inv(I: list) -> list | None:
    # Extra Condition : qua_mod(I) != 0
    if not qua_judge(I):
        return
    if qua_mod(I) == 0:
        return
    O = sca_qua_mul(1 / (qua_mod(I) ** 2), qua_conj(I))
    return O


def rot(vec: list, axis: list, deg: int | float) -> list | None:
    # Extra Condition : qua_mod(axis) != 0
    if not qua_judge(vec):
        return
    if not math.isclose(vec[0], 0):
        return
    if not qua_judge(axis):
        return
    if not math.isclose(axis[0], 0):
        return
    if qua_mod(axis) == 0:
        return
    if not tensor.ten_judge(deg, 0):
        return
    unit = qua_unit(axis)
    exp = [
        math.cos(deg / 2),
        math.sin(deg / 2) * unit[1],
        math.sin(deg / 2) * unit[2],
        math.sin(deg / 2) * unit[3],
    ]
    result = qua_mul(qua_mul(exp, vec), qua_inv(exp))
    return result


def qua_vec(I: list) -> list | None:
    if not qua_judge(I):
        return
    O = [I[1], I[2], I[3]]
    return O
