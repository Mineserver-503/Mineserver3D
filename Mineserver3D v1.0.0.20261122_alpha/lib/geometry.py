import math
import lib.tensor as tensor
import lib.quaternion as quaternion


class Vector:
    def __init__(self, d: list, p: list):
        self.d = d
        self.p = p
        self.dispmode = 1


class Plane:
    def __init__(self, d1: list, d2: list, p: list):
        self.d1 = d1
        self.d2 = d2
        self.p = p


def Pt_judge(I: any) -> bool:
    if not tensor.ten_judge(I, 1):
        return False
    if len(I) != 3:
        return False
    return True


def V_judge(I: any) -> bool:
    if type(I) != Vector:
        return False
    if not tensor.ten_judge(I.d, 1):
        return False
    if len(I.d) != 3:
        return False
    if not tensor.ten_judge(I.p, 1):
        return False
    if len(I.p) != 3:
        return False
    if tensor.vec_mod(I.d) == 0:
        return False
    return True


def P_judge(I: any) -> bool:
    if type(I) != Plane:
        return False
    if not tensor.ten_judge(I.d1, 1):
        return False
    if len(I.d1) != 3:
        return False
    if not tensor.ten_judge(I.d2, 1):
        return False
    if len(I.d2) != 3:
        return False
    if not tensor.ten_judge(I.p, 1):
        return False
    if len(I.p) != 3:
        return False
    if tensor.vec_mod(I.d1) == 0:
        return False
    if tensor.vec_mod(I.d2) == 0:
        return False
    if tensor.vec_col_judge(I.d1, I.d2):
        return False
    return True


def V_mod(I: Vector) -> float | None:
    if not V_judge(I):
        return
    return tensor.vec_mod(I.d)


def Pt_V_judge(I1: list, I2: Vector) -> bool | None:
    if not Pt_judge(I1):
        return
    if not V_judge(I2):
        return
    if I1 == I2.p:
        return True
    else:
        J = tensor.ten_m(I1, I2.p, 1)
        return tensor.vec_col_judge(J, I2.d)


def P_V(I: Plane) -> Vector | None:
    if not P_judge(I):
        return
    return Vector(tensor.vec_cross(I.d1, I.d2), I.p)


def Pt_P_judge(I1: list, I2: Plane) -> bool | str | None:
    if not Pt_judge(I1):
        return
    if not P_judge(I2):
        return
    if I1 == I2.p:
        return True
    else:
        J = tensor.ten_m(I1, I2.p, 1)
        if J == I2.d1 or J == I2.d2:
            return True
        else:
            if tensor.vec_col_judge(
                P_V(I2).d,
                tensor.vec_cross(tensor.ten_m(J, I2.d1, 1), tensor.ten_m(J, I2.d2, 1)),
            ) or Pt_V_judge(J, Vector(tensor.ten_m(I2.d2, I2.d1, 1), I2.d1)):
                return True
            else:
                det = tensor.vec_dot(J, tensor.vec_cross(I2.d1, I2.d2))
                if det < 0:
                    return "Left"
                if det > 0:
                    return "Right"


def V_P_judge(I1: Vector, I2: Plane) -> str | None:
    if not V_judge(I1):
        return
    if not P_judge(I2):
        return
    if V_mod(I1) == 0:
        return
    J1 = Vector(I1.d, [0, 0, 0])
    J2 = Plane(I2.d1, I2.d2, [0, 0, 0])
    if (
        Pt_P_judge(J1.p, J2) == True
        and Pt_P_judge(tensor.ten_p(J1.p, J1.d, 1), J2) == True
    ):
        if (
            Pt_P_judge(I1.p, I2) == True
            and Pt_P_judge(tensor.ten_p(I1.p, I1.d, 1), I2) == True
        ):
            return "Coincident"
        else:
            return "Parallel"
    else:
        return "Intersecting"


def V_P_int(I1: Vector, I2: Plane) -> list | None:
    if not V_judge(I1):
        return
    if not P_judge(I2):
        return
    if V_P_judge(I1, I2) == "Coincident" or V_P_judge(I1, I2) == "Parallel":
        return
    J1 = Vector(I1.d, [0, 0, 0])
    J2 = Plane(I2.d1, I2.d2, tensor.ten_m(I2.p, I1.p, 1))
    x1, y1, z1 = J2.d1[0], J2.d1[1], J2.d1[2]
    x2, y2, z2 = J2.d2[0], J2.d2[1], J2.d2[2]
    x3, y3, z3 = J1.d[0], J1.d[1], J1.d[2]
    x4, y4, z4 = J2.p[0], J2.p[1], J2.p[2]
    p1, p2, p3, p4, p5, p6, p7 = (
        (x3 == 0 and y3 == 0 and z3 != 0),
        (x3 == 0 and y3 != 0 and z3 == 0),
        (x3 == 0 and y3 != 0 and z3 != 0),
        (x3 != 0 and y3 == 0 and z3 == 0),
        (x3 != 0 and y3 == 0 and z3 != 0),
        (x3 != 0 and y3 != 0 and z3 == 0),
        (x3 != 0 and y3 != 0 and z3 != 0),
    )
    k1, k2, k3, k4, k5, k6, k7, k8, k9 = (
        x3 * y1 - x1 * y3,
        x2 * y3 - x3 * y2,
        x3 * y4 - x4 * y3,
        y2 * z3 - y3 * z2,
        y3 * z1 - y1 * z3,
        y3 * z4 - y4 * z3,
        z2 * x3 - z3 * x2,
        z3 * x1 - z1 * x3,
        z3 * x4 - z4 * x3,
    )
    if p4 or p5 or p6 or p7:
        a = (k3 * k7 - k2 * k9) / (k2 * k8 - k1 * k7)
        b = (k3 * k8 - k1 * k9) / (k2 * k8 - k1 * k7)
    if p2 or p3 or p6 or p7:
        a = (k2 * k6 - k3 * k4) / (k1 * k4 - k2 * k5)
        b = (k1 * k6 - k3 * k5) / (k1 * k4 - k2 * k5)
    if p1 or p3 or p5 or p7:
        a = (k4 * k9 - k6 * k7) / (k5 * k7 - k4 * k8)
        b = (k5 * k9 - k6 * k8) / (k5 * k7 - k4 * k8)
    O = [
        a * x1 + b * x2 + x4 + I1.p[0],
        a * y1 + b * y2 + y4 + I1.p[1],
        a * z1 + b * z2 + z4 + I1.p[2],
    ]
    return O


def Pt_P_dist(I1: list, I2: Plane) -> float | None:
    if not Pt_judge(I1):
        return
    if not P_judge(I2):
        return
    J1 = Vector(P_V(I2).d, I1)
    O = V_P_int(J1, I2)
    return O
