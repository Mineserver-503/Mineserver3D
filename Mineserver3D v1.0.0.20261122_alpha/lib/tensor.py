import lib.pre_tensor as pre_tensor
import math


def int_rng_judge(I: any, l: int | float) -> bool:
    if not (type(I) == int and isinstance(l, (int, float))):
        return False
    if I < l:
        return False
    return True


def ten_judge(I: any, dim: int) -> bool:
    if not (isinstance(I, (int, float, list)) and int_rng_judge(dim, 0)):
        return False
    result = pre_tensor.ten_judge(I, dim)
    if result == False:
        return False
    if result == None:
        return True


def sca_rng_judge(I: any, l: int | float) -> bool:
    if not ten_judge(I, 0):
        return False
    if not ten_judge(l, 0):
        return False
    if I < l:
        return False
    return True


def ten_size(I: list, dim: int) -> int | None:
    if not int_rng_judge(dim, 1):
        return
    if not ten_judge(I, dim):
        return
    return pre_tensor.ten_size(I, dim)


def zero_ten(dim: int, size: int) -> int | list | None:
    if not (int_rng_judge(dim, 0) and int_rng_judge(size, 1)):
        return
    return pre_tensor.zero_ten(dim, size)


def ten_f(I: list, dim: int, size: int) -> list | None:
    if not int_rng_judge(dim, 1):
        return
    if not ten_judge(I, dim):
        return
    if not int_rng_judge(size, ten_size(I, dim)):
        return
    return pre_tensor.ten_f(I, dim, size)


def ten_f_sgl(I: list, dim: int) -> list | None:
    if not int_rng_judge(dim, 1):
        return
    if not ten_judge(I, dim):
        return
    return ten_f(I, dim, ten_size(I, dim))


def ten_f_dbl(I1: list, dim1: int, I2: list, dim2: int) -> tuple | None:
    if not int_rng_judge(dim1, 1):
        return
    if not int_rng_judge(dim2, 1):
        return
    if not ten_judge(I1, dim1):
        return
    if not ten_judge(I2, dim2):
        return
    size = max([ten_size(I1, dim1), ten_size(I2, dim2)])
    O1, O2 = ten_f(I1, dim1, size), ten_f(I2, dim2, size)
    return (O1, O2)


def ten_p(
    I1: int | float | list, I2: int | float | list, dim: int
) -> int | float | list | None:
    if not int_rng_judge(dim, 0):
        return
    if not ten_judge(I1, dim):
        return
    if not ten_judge(I2, dim):
        return
    if dim != 0:
        J1, J2 = ten_f_dbl(I1, dim, I2, dim)[0], ten_f_dbl(I1, dim, I2, dim)[1]
        return pre_tensor.ten_p(J1, J2, dim)
    else:
        return I1 + I2


def ten_ele_sum(I: list, dim: int) -> float | None:
    if not int_rng_judge(dim, 1):
        return
    if not ten_judge(I, dim):
        return
    return pre_tensor.ten_ele_sum(I, dim)


def sca_ten_mul(
    I1: float, I2: int | float | list, dim: int
) -> int | float | list | None:
    if not ten_judge(I1, 0):
        return
    if not int_rng_judge(dim, 0):
        return
    if not ten_judge(I2, dim):
        return
    return pre_tensor.sca_ten_mul(I1, I2, dim)


def ten_opp(I: int | float | list, dim: int) -> int | float | list | None:
    if not int_rng_judge(dim, 0):
        return
    if not ten_judge(I, dim):
        return
    return sca_ten_mul(-1, I, dim)


def ten_m(
    I1: int | float | list, I2: int | float | list, dim: int
) -> int | float | list | None:
    if not int_rng_judge(dim, 0):
        return
    if not ten_judge(I1, dim):
        return
    if not ten_judge(I2, dim):
        return
    J2 = ten_opp(I2, dim)
    return ten_p(I1, J2, dim)


def vec_mod(I: list) -> float | None:
    if not ten_judge(I, 1):
        return
    sq_sum = 0
    for e in range(len(I)):
        sq_sum = sq_sum + I[e] ** 2
    O = math.sqrt(sq_sum)
    return O


def vec_dist(I1: list, I2: list) -> float | None:
    if not ten_judge(I1, 1):
        return
    if not ten_judge(I2, 1):
        return
    J1, J2 = ten_f_dbl(I1, 1, I2, 1)[0], ten_f_dbl(I1, 1, I2, 1)[1]
    K = ten_m(J1, J2, 1)
    O = vec_mod(K)
    return O


def vec_unit(I: list) -> list | None:
    # Extra Condition : vec_mod(I) != 0
    if not ten_judge(I, 1):
        return
    if vec_mod(I) == 0:
        return
    O = sca_ten_mul(1 / vec_mod(I), I, 1)
    return O


def vec_col_judge(I1: list, I2: list) -> bool | None:
    # Extra Condition : vec_mod(I1) != 0
    # Extra Condition : vec_mod(I2) != 0
    if not ten_judge(I1, 1):
        return
    if vec_mod(I1) == 0:
        return
    if not ten_judge(I2, 1):
        return
    if vec_mod(I2) == 0:
        return
    J1, J2 = ten_f_dbl(I1, 1, I2, 1)[0], ten_f_dbl(I1, 1, I2, 1)[1]
    K1, K2 = vec_unit(J1), vec_unit(J2)
    L1 = ten_opp(K1, 1)
    C1 = True
    C2 = True
    for e1 in range(len(L1)):
        if not math.isclose(K1[e1], K2[e1]):
            C1 = False
    for e2 in range(len(L1)):
        if not math.isclose(L1[e2], K2[e2]):
            C2 = False
    if C1 or C2:
        return True
    else:
        return False


def vec_dot(I1: list, I2: list) -> float | None:
    if not ten_judge(I1, 1):
        return
    if not ten_judge(I2, 1):
        return
    J1, J2 = ten_f_dbl(I1, 1, I2, 1)[0], ten_f_dbl(I1, 1, I2, 1)[1]
    O = 0
    for e in range(len(J1)):
        O = O + J1[e] * J2[e]
    return O


def vec_cross(I1: list, I2: list) -> list | None:
    if not ten_judge(I1, 1):
        return
    if len(I1) > 3:
        return
    if not ten_judge(I2, 1):
        return
    if len(I2) > 3:
        return
    J1, J2 = ten_f(I1, 1, 3), ten_f(I2, 1, 3)
    O = [
        I1[1] * I2[2] - I1[2] * I2[1],
        I1[2] * I2[0] - I1[0] * I2[2],
        I1[0] * I2[1] - I1[1] * I2[0],
    ]
    return O


def mat_vec_mul(I1: list, I2: list) -> list | None:
    if not ten_judge(I1, 2):
        return
    if not ten_judge(I2, 1):
        return
    J1, J2 = ten_f_dbl(I1, 2, I2, 1)[0], ten_f_dbl(I1, 2, I2, 1)[1]
    pre_O1 = []
    for e1 in range(len(J1)):
        pre_O1.append(sca_ten_mul(J2[e1], J1[e1], 1))
    pre_O2 = []
    for e2 in range(len(pre_O1)):
        sub_pre_O2 = []
        for e3 in range(len(pre_O1)):
            sub_pre_O2.append(pre_O1[e3][e2])
        pre_O2.append(sub_pre_O2)
    O = []
    for e4 in range(len(pre_O2)):
        O.append(ten_ele_sum(pre_O2[e4], 1))
    return O


def mat_mul(I1: list, I2: list) -> list | None:
    if not ten_judge(I1, 2):
        return
    if not ten_judge(I2, 2):
        return
    J1, J2 = ten_f_dbl(I1, 2, I2, 2)[0], ten_f_dbl(I1, 2, I2, 2)[1]
    O = []
    for e in range(len(J1)):
        O.append(mat_vec_mul(I1, I2[e]))
    return O


def ten_isclose(
    I1: int | float | list, I2: int | float | list, dim: int
) -> bool | None:
    if not int_rng_judge(dim, 0):
        return
    if not ten_judge(I1, dim):
        return
    if not ten_judge(I2, dim):
        return
    J1, J2 = ten_f_dbl(I1, dim, I2, dim)[0], ten_f_dbl(I1, dim, I2, dim)[1]
    O = pre_tensor.ten_isclose(J1, J2, dim)
    if O == False:
        return False
    else:
        return True


def vec_ang(I1: list, I2: list) -> float | None:
    # Extra Condition : vec_mod(I1) != 0
    # Extra Condition : vec_mod(I2) != 0
    if not ten_judge(I1, 1):
        return
    if not ten_judge(I2, 1):
        return
    if vec_mod(I1) == 0:
        return
    if vec_mod(I2) == 0:
        return
    i1 = vec_dot(I1, I2) / (vec_mod(I1) * vec_mod(I2))
    if i1 > 1:
        i2 = 1
    elif i1 < -1:
        i2 = -1
    else:
        i2 = i1
    O = math.acos(i2)
    return O


def vec_cut(I1: list, I2) -> list|None:
    # Extra Condition : vec_mod(I1) != 0
    if not ten_judge(I1, 1):
        return
    if vec_mod(I1) == 0:
        return
    if not ten_judge(I2, 0):
        return
    O = sca_ten_mul(I2 / vec_mod(I1), I1, 1)
    return O
