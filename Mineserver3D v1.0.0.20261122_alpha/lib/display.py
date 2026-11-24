import math
import lib.quaternion as quaternion
import lib.tensor as tensor
import lib.geometry as geometry


class Camera:
    def __init__(
        self,
        mode: str,
        fov: float,
        aspect: float,
        near: float,
        far: float,
        eye: geometry.Vector,
    ):
        if (
            (mode == "persp")
            and tensor.sca_rng_judge(fov, math.pi / 6)
            and tensor.sca_rng_judge(-fov, -2 * math.pi / 3)
            and tensor.sca_rng_judge(aspect, 1 / 3)
            and tensor.sca_rng_judge(-aspect, -3)
            and tensor.sca_rng_judge(near, 1 / 20)
            and tensor.sca_rng_judge(far, near + 10)
            and geometry.V_judge(eye)
        ):
            if eye.d[0] == 0 and eye.d[1] == 0:
                self.mode = None
                self.fov = None
                self.aspect = None
                self.near = None
                self.far = None
                self.eye = None
                self.P_top = None
                self.P_left = None
                self.P_bottom = None
                self.P_right = None
                self.P_near = None
                self.P_far = None
            else:
                self.mode = mode
                self.fov = fov
                self.aspect = aspect
                self.near = near
                self.far = far
                self.eye = eye
                """""" """""" """"""
                rel_x = self.near
                rel_y = math.tan(self.fov / 2) * self.aspect * self.near
                rel_z = math.tan(self.fov / 2) * self.near
                near_V = geometry.Vector(tensor.vec_cut(self.eye.d, rel_x), self.eye.p)
                far_V = geometry.Vector(
                    tensor.vec_cut(self.eye.d, self.far), self.eye.p
                )
                self.near_orig = tensor.ten_p(near_V.d, near_V.p, 1)
                self.far_orig = tensor.ten_p(far_V.d, far_V.p, 1)
                self.near_Vx = geometry.Vector(
                    tensor.vec_cut(
                        tensor.vec_cross([near_V.d[0], near_V.d[1], 0], [0, 0, 1]),
                        rel_y,
                    ),
                    self.near_orig,
                )
                self.near_Vy = geometry.Vector(
                    tensor.vec_cut(
                        tensor.vec_cross(self.near_Vx.d, near_V.d),
                        rel_z,
                    ),
                    self.near_orig,
                )
                edge1 = geometry.Vector(
                    tensor.ten_p(
                        tensor.ten_p(self.near_Vx.d, self.near_Vy.d, 1), near_V.d, 1
                    ),
                    self.eye.p,
                )
                edge2 = geometry.Vector(
                    tensor.ten_p(
                        tensor.ten_p(
                            tensor.ten_opp(self.near_Vx.d, 1), self.near_Vy.d, 1
                        ),
                        near_V.d,
                        1,
                    ),
                    self.eye.p,
                )
                edge3 = geometry.Vector(
                    tensor.ten_p(
                        tensor.ten_p(
                            tensor.ten_opp(self.near_Vx.d, 1),
                            tensor.ten_opp(self.near_Vy.d, 1),
                            1,
                        ),
                        near_V.d,
                        1,
                    ),
                    self.eye.p,
                )
                edge4 = geometry.Vector(
                    tensor.ten_p(
                        tensor.ten_p(
                            self.near_Vx.d, tensor.ten_opp(self.near_Vy.d, 1), 1
                        ),
                        near_V.d,
                        1,
                    ),
                    self.eye.p,
                )
                self.P_top = geometry.Plane(edge1.d, edge2.d, self.eye.p)
                self.P_left = geometry.Plane(edge2.d, edge3.d, self.eye.p)
                self.P_bottom = geometry.Plane(edge3.d, edge4.d, self.eye.p)
                self.P_right = geometry.Plane(edge4.d, edge1.d, self.eye.p)
                self.P_near = geometry.Plane(
                    self.near_Vx.d, self.near_Vy.d, self.near_orig
                )
                self.P_far = geometry.Plane(
                    self.near_Vx.d, self.near_Vy.d, self.far_orig
                )
        elif (
            (mode == "ortho")
            and tensor.sca_rng_judge(-fov, -1000)
            and tensor.sca_rng_judge(fov, 1)
            and tensor.sca_rng_judge(aspect, 1 / 3)
            and tensor.sca_rng_judge(-aspect, -3)
            and tensor.sca_rng_judge(near, 1 / 20)
            and tensor.sca_rng_judge(far, near + 10)
            and geometry.V_judge(eye)
        ):
            if eye.d[0] == 0 and eye.d[1] == 0:
                self.mode = None
                self.fov = None
                self.aspect = None
                self.near = None
                self.far = None
                self.eye = None
                self.P_top = None
                self.P_left = None
                self.P_bottom = None
                self.P_right = None
                self.P_near = None
                self.P_far = None
            else:
                self.mode = mode
                self.fov = fov
                self.aspect = aspect
                self.near = near
                self.far = far
                self.eye = eye
                """""" """""" """"""
                near_V = geometry.Vector(
                    tensor.vec_cut(self.eye.d, self.near), self.eye.p
                )
                far_V = geometry.Vector(
                    tensor.vec_cut(self.eye.d, self.far), self.eye.p
                )
                self.near_orig = tensor.ten_p(near_V.d, near_V.p, 1)
                self.far_orig = tensor.ten_p(far_V.d, far_V.p, 1)
                self.near_Vx = geometry.Vector(
                    tensor.vec_cut(
                        tensor.vec_cross([near_V.d[0], near_V.d[1], 0], [0, 0, 1]),
                        self.aspect * self.fov / 2,
                    ),
                    self.near_orig,
                )
                self.near_Vy = geometry.Vector(
                    tensor.vec_cut(
                        tensor.vec_cross(self.near_Vx.d, near_V.d),
                        self.fov / 2,
                    ),
                    self.near_orig,
                )
                near_Pt1 = tensor.ten_p(
                    tensor.ten_p(self.near_Vx.d, self.near_Vy.d, 1), self.near_orig, 1
                )
                near_Pt2 = tensor.ten_p(
                    tensor.ten_p(tensor.ten_opp(self.near_Vx.d, 1), self.near_Vy.d, 1),
                    self.near_orig,
                    1,
                )
                near_Pt3 = tensor.ten_p(
                    tensor.ten_p(
                        tensor.ten_opp(self.near_Vx.d, 1),
                        tensor.ten_opp(self.near_Vy.d, 1),
                        1,
                    ),
                    self.near_orig,
                    1,
                )
                near_Pt4 = tensor.ten_p(
                    tensor.ten_p(self.near_Vx.d, tensor.ten_opp(self.near_Vy.d, 1), 1),
                    self.near_orig,
                    1,
                )
                near_V_top = geometry.Vector(
                    tensor.sca_ten_mul(2, self.near_Vx.d, 1), near_Pt2
                )
                near_V_left = geometry.Vector(
                    tensor.sca_ten_mul(2, self.near_Vy.d, 1), near_Pt3
                )
                near_V_bottom = geometry.Vector(
                    tensor.sca_ten_mul(-2, self.near_Vx.d, 1), near_Pt4
                )
                near_V_right = geometry.Vector(
                    tensor.sca_ten_mul(-2, self.near_Vy.d, 1), near_Pt1
                )
                edge1 = geometry.Vector(far_V.d, near_Pt1)
                edge2 = geometry.Vector(far_V.d, near_Pt2)
                edge3 = geometry.Vector(far_V.d, near_Pt3)
                edge4 = geometry.Vector(far_V.d, near_Pt4)
                self.P_top = geometry.Plane(near_V_top.d, edge2.d, near_Pt2)
                self.P_left = geometry.Plane(near_V_left.d, edge3.d, near_Pt3)
                self.P_bottom = geometry.Plane(near_V_bottom.d, edge4.d, near_Pt4)
                self.P_right = geometry.Plane(near_V_right.d, edge1.d, near_Pt1)
                self.P_near = geometry.Plane(
                    self.near_Vx.d, self.near_Vy.d, self.near_orig
                )
                self.P_far = geometry.Plane(
                    self.near_Vx.d, self.near_Vy.d, self.far_orig
                )
        else:
            self.mode = None
            self.fov = None
            self.aspect = None
            self.near = None
            self.far = None
            self.eye = None
            self.P_top = None
            self.P_left = None
            self.P_bottom = None
            self.P_right = None
            self.P_near = None
            self.P_far = None


def C_judge(I: any) -> bool:
    if type(I) != Camera:
        return False
    if I.mode == None:
        return False
    return True


def Pt_disp_judge(I1: list, I2: Camera) -> str | None:
    if not geometry.Pt_judge(I1):
        return
    if not C_judge(I2):
        return
    if geometry.Pt_P_judge(I1, I2.P_near) == "Right":
        return "OutNear"
    if geometry.Pt_P_judge(I1, I2.P_near) == True:
        return "Near"
    if (
        geometry.Pt_P_judge(I1, I2.P_near) == "Left"
        and geometry.Pt_P_judge(I1, I2.P_far) == "Right"
    ):
        return "In"
    if geometry.Pt_P_judge(I1, I2.P_far) == True:
        return "Far"
    if geometry.Pt_P_judge(I1, I2.P_far) == "Left":
        return "OutFar"


def V_disp_cut(I1: geometry.Vector, I2: Camera) -> geometry.Vector | None:
    if not geometry.V_judge(I1):
        return
    if not C_judge(I2):
        return
    J1 = Pt_disp_judge(tensor.ten_p(I1.d, I1.p, 1), I2)
    J2 = Pt_disp_judge(I1.p, I2)
    if (J1 == "Near" or J1 == "In" or J1 == "F") and (
        J2 == "Near" or J2 == "In" or J2 == "F"
    ):
        return I1
    if (
        (J1 == "OutNear" and J2 == "OutNear")
        or (J1 == "Near" and J2 == "OutNear")
        or (J1 == "OutNear" and J2 == "Near")
        or (J1 == "OutFar" and J2 == "OutFar")
        or (J1 == "Far" and J2 == "OutFar")
        or (J1 == "OutFar" and J2 == "Far")
    ):
        return
    if (J1 == "In" or J1 == "Far") and J2 == "OutNear":
        Pt = geometry.V_P_int(I1, I2.P_near)
        O = geometry.Vector(
            tensor.vec_cut(I1.d, tensor.vec_dist(tensor.ten_p(I1.d, I1.p, 1), Pt)), Pt
        )
    if J1 == "OutFar" and J2 == "OutNear":
        Pt1 = geometry.V_P_int(I1, I2.P_near)
        Pt2 = geometry.V_P_int(I1, I2.P_far)
        O = geometry.Vector(tensor.vec_cut(I1.d, tensor.vec_dist(Pt1, Pt2)), Pt1)
    if (J1 == "In" or J1 == "Near") and J1 == "OutFar":
        Pt = geometry.V_P_int(I1, I2.P_far)
        O = geometry.Vector(tensor.vec_cut(I1.d, tensor.vec_dist(I1.p, Pt)), I1.p)
    if (J2 == "In" or J2 == "Far") and J1 == "OutNear":
        Pt = geometry.V_P_int(I1, I2.P_near)
        O = geometry.Vector(tensor.vec_cut(I1.d, tensor.vec_dist(I1.p, Pt)), I1.p)
    if J2 == "OutFar" and J1 == "OutNear":
        Pt1 = geometry.V_P_int(I1, I2.P_far)
        Pt2 = geometry.V_P_int(I1, I2.P_near)
        O = geometry.Vector(tensor.vec_cut(I1.d, tensor.vec_dist(Pt1, Pt2)), Pt1)
    if (J1 == "In" or J1 == "Near") and J2 == "OutFar":
        Pt = geometry.V_P_int(I1, I2.P_far)
        O = geometry.Vector(
            tensor.vec_cut(I1.d, tensor.vec_dist(tensor.ten_p(I1.d, I1.p, 1), Pt)), Pt
        )
    return O


def pro(I1, I2: Camera):
    if not C_judge(I2):
        return
    try:
        test = I1.dispmode
    except:
        return
    if I1.dispmode == 1:
        if V_disp_cut(I1, I2) == None:
            return
        else:
            J1 = V_disp_cut(I1, I2)
        if I2.mode == "persp":
            light1 = geometry.Vector(tensor.ten_m(J1.p, I2.eye.p, 1), I2.eye.p)
            light2 = geometry.Vector(
                tensor.ten_m(tensor.ten_p(J1.d, J1.p, 1), I2.eye.p, 1), I2.eye.p
            )
        else:
            light1 = geometry.Vector(geometry.P_V(I2.P_near).d, J1.p)
            light2 = geometry.Vector(
                geometry.P_V(I2.P_near).d, tensor.ten_p(J1.d, J1.p, 1)
            )
        I1_pro = geometry.Vector(
            tensor.ten_m(
                geometry.V_P_int(light2, I2.P_near),
                geometry.V_P_int(light1, I2.P_near),
                1,
            ),
            geometry.V_P_int(light1, I2.P_near),
        )
        rel_x = I2.near_Vx.d
        rel_y = I2.near_Vy.d
        rel_p1 = tensor.ten_m(I1_pro.p, I2.near_orig, 1)
        rel_p2 = tensor.ten_m(geometry.V_P_int(light2, I2.P_near), I2.near_orig, 1)
        O = (
            (
                tensor.vec_dot(rel_p1, rel_x) / tensor.vec_mod(rel_x) ** 2,
                tensor.vec_dot(rel_p1, rel_y) / tensor.vec_mod(rel_y) ** 2,
            ),
            (
                tensor.vec_dot(rel_p2, rel_x) / tensor.vec_mod(rel_x) ** 2,
                tensor.vec_dot(rel_p2, rel_y) / tensor.vec_mod(rel_y) ** 2,
            ),
        )
        return O
