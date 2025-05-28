"""
# Transform Module
This module provide useful class and function for spatial calculation

## Class
- `Transform` : A spatial transform represented a translation and rotation

## Function
- `deg_to_rad` : translate degree to radian
- `rad_to_deg` : translate radian to degree
- `rx_mat` : compute rotation matrx of rotation along x axis
- `ry_mat` : compute rotation matrx of rotation along y axis
- `rz_mat` : compute rotation matrx of rotation along z axis
- `euler_to_mat` : translate euler angle to rotation matrix
- `mat_to_euler` : translate rotation matrix to euler angle
"""

from typing import Tuple
import re

import numpy
import numpy.typing as numpy_typing

from inovopy.geometry import IntoRobotCommand, deg_to_rad, rad_to_deg


def rx_mat(deg: float) -> numpy_typing.NDArray[numpy.float64]:
    """compute rotation matrx of rotation along x axis"""
    mat = numpy.eye(3)
    mat[1, 1] = numpy.cos(deg_to_rad(deg))
    mat[1, 2] = -numpy.sin(deg_to_rad(deg))
    mat[2, 2] = numpy.cos(deg_to_rad(deg))
    mat[2, 1] = numpy.sin(deg_to_rad(deg))
    return mat


def ry_mat(deg: float) -> numpy_typing.NDArray[numpy.float64]:
    """compute rotation matrx of rotation along y axis"""
    mat = numpy.eye(3)
    mat[0, 0] = numpy.cos(deg_to_rad(deg))
    mat[0, 2] = numpy.sin(deg_to_rad(deg))
    mat[2, 2] = numpy.cos(deg_to_rad(deg))
    mat[2, 0] = -numpy.sin(deg_to_rad(deg))
    return mat


def rz_mat(deg: float) -> numpy_typing.NDArray[numpy.float64]:
    """compute rotation matrx of rotation along z axis"""
    mat = numpy.eye(3)
    mat[0, 0] = numpy.cos(deg_to_rad(deg))
    mat[0, 1] = -numpy.sin(deg_to_rad(deg))
    mat[1, 1] = numpy.cos(deg_to_rad(deg))
    mat[1, 0] = numpy.sin(deg_to_rad(deg))
    return mat


def euler_to_mat(
    euler_deg: Tuple[float, float, float],
) -> numpy_typing.NDArray[numpy.float64]:
    """translate euler angle to rotation matrix"""
    rx = rx_mat(euler_deg[0])
    ry = ry_mat(euler_deg[1])
    rz = rz_mat(euler_deg[2])
    return numpy.matmul(rz, numpy.matmul(ry, rx))


def mat_to_euler(
    mat: numpy_typing.NDArray[numpy.float64],
) -> Tuple[float, float, float]:
    """translate rotation matrix to euler angle"""
    r31 = mat[2, 0]
    if numpy.abs(r31) != 1:
        ry = -numpy.arcsin(r31)
        rx = numpy.arctan2(mat[2, 1] / numpy.cos(ry), mat[2, 2] / numpy.cos(ry))
        rz = numpy.arctan2(mat[1, 0] / numpy.cos(ry), mat[0, 0] / numpy.cos(ry))
    else:
        rz = 0
        if r31 == -1:
            ry = numpy.pi / 2
            rx = numpy.arctan2(mat[0, 1], mat[0, 2])
        else:
            ry = -numpy.pi / 2
            rx = numpy.arctan2(-mat[0, 1], -mat[0, 2])
    return (rad_to_deg(rx), rad_to_deg(ry), rad_to_deg(rz))


class Transform(IntoRobotCommand):
    """
    # Transform
    A class representing spatial transform,
    compose of a translation and a rotation

    ## Representation
    - `vec_mm` : a 3D vector with unit in mm
    - `euler_deg` : a set of euler angle wiht unit in degree
    """

    def __init__(
        self,
        vec_mm: Tuple[float, float, float] = (0, 0, 0),
        euler_deg: Tuple[float, float, float] = (0, 0, 0),
    ):
        """
        initalize a transform

        ## Parameter
        - `vec_mm` : a 3D vector with unit in mm
        - `euler_deg` : a set of euler angle wiht unit in degree
        """
        self.vec_mm: Tuple[float, float, float] = vec_mm
        self.euler_deg: Tuple[float, float, float] = euler_deg

    def clone(self) -> "Transform":
        """clone the transform"""
        return Transform(vec_mm=self.vec_mm, euler_deg=self.euler_deg)

    def __repr__(self) -> str:
        return f"vec_mm : {self.vec_mm}, euler_deg : {self.euler_deg}"

    @classmethod
    def from_vec(cls, x_mm: float = 0, y_mm: float = 0, z_mm: float = 0) -> "Transform":
        """Construct a new `Transform` from vector componment"""
        return Transform(vec_mm=(x_mm, y_mm, z_mm))

    @classmethod
    def from_euler(
        cls, rx_deg: float = 0, ry_deg: float = 0, rz_deg: float = 0
    ) -> "Transform":
        """Construct a new `Transform` from euler angle set"""
        return Transform(euler_deg=(rx_deg, ry_deg, rz_deg))

    @classmethod
    def from_robot(cls, res: str) -> "Transform":
        """Parse robot transform response into `Transform`"""
        res = re.sub(r"[ {}]", "", res).split(",")
        t = Transform()
        for i in range(6):
            tokens = res[i].split(":")
            q = float(tokens[1])

            match tokens[0]:
                case "x":
                    t.set_x(q * 1000)
                case "y":
                    t.set_y(q * 1000)
                case "z":
                    t.set_z(q * 1000)
                case "rx":
                    t.set_rx(rad_to_deg(q))
                case "ry":
                    t.set_ry(rad_to_deg(q))
                case "rz":
                    t.set_rz(rad_to_deg(q))
                case _:
                    continue
        return t

    def vec_only(self) -> "Transform":
        """Extract translation from `self` and construct a new transfrom"""
        return Transform(vec_mm=self.vec_mm)

    def euler_only(self) -> "Transform":
        """Extract rotation from `self` and construct a new transfrom"""
        return Transform(euler_deg=self.euler_deg)

    @classmethod
    def from_x(cls, x_mm: float) -> "Transform":
        """Construct a new `Transform` with specified x"""
        return Transform.from_vec(x_mm=x_mm)

    @classmethod
    def from_y(cls, y_mm: float) -> "Transform":
        """Construct a new `Transform` with specified y"""
        return Transform.from_vec(y_mm=y_mm)

    @classmethod
    def from_z(cls, z_mm: float) -> "Transform":
        """Construct a new `Transform` with specified z"""
        return Transform.from_vec(z_mm=z_mm)

    @classmethod
    def from_rx(cls, rx_deg: float) -> "Transform":
        """Construct a new `Transform` with specified rx"""
        return Transform.from_euler(rx_deg=rx_deg)

    @classmethod
    def from_ry(cls, ry_deg: float) -> "Transform":
        """Construct a new `Transform` with specified ry"""
        return Transform.from_euler(ry_deg=ry_deg)

    @classmethod
    def from_rz(cls, rz_deg: float) -> "Transform":
        """Construct a new `Transform` with specified rz"""
        return Transform.from_euler(rz_deg=rz_deg)

    def set_vec(self, x_mm: float, y_mm: float, z_mm: float) -> "Transform":
        """set the vector"""
        self.vec_mm = (x_mm, y_mm, z_mm)
        return self

    def set_x(self, mm: float) -> "Transform":
        """set the x component to a specified value"""
        self.vec_mm = (mm, self.vec_mm[1], self.vec_mm[2])
        return self

    def set_y(self, mm: float) -> "Transform":
        """set the y component to a specified value"""
        self.vec_mm = (self.vec_mm[0], mm, self.vec_mm[2])
        return self

    def set_z(self, mm: float) -> "Transform":
        """set the z component to a specified value"""
        self.vec_mm = (self.vec_mm[0], self.vec_mm[1], mm)
        return self

    def set_euler(self, rx_deg: float, ry_deg: float, rz_deg: float) -> "Transform":
        """set the euler angle"""
        self.euler_deg = (rx_deg, ry_deg, rz_deg)
        return self

    def set_rx(self, deg: float) -> "Transform":
        """set the rx component to a specified value"""
        self.euler_deg = (deg, self.euler_deg[1], self.euler_deg[2])
        return self

    def set_ry(self, deg: float) -> "Transform":
        """set the ry component to a specified value"""
        self.euler_deg = (self.euler_deg[0], deg, self.euler_deg[2])
        return self

    def set_rz(self, deg: float) -> "Transform":
        """set the rz component to a specified value"""
        self.euler_deg = (self.euler_deg[0], self.euler_deg[1], deg)
        return self

    def to_homogenous(self) -> numpy_typing.NDArray[numpy.float64]:
        """
        return a homogenous matrix representation of the `self`

        ## Return:
        - `np.array` : 4x4 homogenous matrix representation of the transform
        """
        mat = numpy.eye(4)
        mat[0:3, 0:3] = euler_to_mat(self.euler_deg)
        mat[0:3, 3] = numpy.asarray(self.vec_mm)
        return mat

    @classmethod
    def from_homogenous(cls, mat: numpy_typing.NDArray[numpy.float64]) -> "Transform":
        """
        construct a transform from a `np.array` 4x4 homogenous matrix

        ## Parameter:
        - `mat : np.array` : 4x4 homogenous matrix representation of the transform

        ## Return:
        - `Transform`
        """
        return Transform(
            vec_mm=(
                mat[0, 3],
                mat[1, 3],
                mat[2, 3],
            ),
            euler_deg=mat_to_euler(mat),
        )

    def inv(self) -> "Transform":
        """return the inverse transform of `self`"""
        return Transform.from_homogenous(numpy.linalg.inv(self.to_homogenous()))

    def __mul__(self, rhs: "Transform") -> "Transform":
        return Transform.from_homogenous(
            numpy.matmul(self.to_homogenous(), rhs.to_homogenous())
        )

    def then(self, transform: "Transform") -> "Transform":
        """
        return a new transform that is apply a transform to `self`

        ## Parameter
        - `transform` : the transform to apply to `self`

        ## Return
        - `transform` : resulted transform
        """
        new = transform * self
        self.vec_mm = new.vec_mm
        self.euler_deg = new.euler_deg
        return self

    def then_x(self, cm: float) -> "Transform":
        """return a new transform that apply translation along x axis to `self`"""
        return self.then(Transform.from_x(cm))

    def then_y(self, cm: float) -> "Transform":
        """return a new transform that apply translation along y axis to `self`"""
        return self.then(Transform.from_y(cm))

    def then_z(self, cm: float) -> "Transform":
        """return a new transform that apply translation along z axis to `self`"""
        return self.then(Transform.from_z(cm))

    def then_rx(self, deg: float) -> "Transform":
        """return a new transform that apply rotation along x axis to `self`"""
        return self.then(Transform.from_rx(deg))

    def then_ry(self, deg: float) -> "Transform":
        """return a new transform that apply rotation along y axis to `self`"""
        return self.then(Transform.from_ry(deg))

    def then_rz(self, deg: float) -> "Transform":
        """return a new transform that apply rotation along z axis to `self`"""
        return self.then(Transform.from_rz(deg))

    def then_relative_to(
        self, transform: "Transform", reference: "Transform"
    ) -> "Transform":
        """
        return a new transform that,
        apply a transform to `self` relative to a reference

        ## Parameter
        - `transform` : the transform to apply
        - `reference` : the reference of the transfrom
        """
        return reference * transform * reference.inv() * self

    def then_relative(self, transform: "Transform") -> "Transform":
        """return a new transform that apply a transform relative `self`'s position"""
        return self.then_relative_to(transform=transform, reference=self.vec_only())

    def then_relative_rx(self, deg: float) -> "Transform":
        """return a new transform that apply relative rotaion along axis x"""
        return self.then_relative(Transform.from_rx(deg))

    def then_relative_ry(self, deg: float) -> "Transform":
        """return a new transform that apply relative rotaion along axis y"""
        return self.then_relative(Transform.from_ry(deg))

    def then_relative_rz(self, deg: float) -> "Transform":
        """return a new transform that apply relative rotaion along axis z"""
        return self.then_relative(Transform.from_rz(deg))

    def to_dict(self) -> dict[str, str | float]:
        """return a `dict[str,str|float]` representation of the transform"""
        return {
            "target": "transform",
            "x": self.vec_mm[0],
            "y": self.vec_mm[1],
            "z": self.vec_mm[2],
            "rx": self.euler_deg[0],
            "ry": self.euler_deg[1],
            "rz": self.euler_deg[2],
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | float]) -> "Transform":
        """
        construct a new `Transform` from a dictionary

        ## Parameter
        - `data: dict[str, str|float]`: the data, if field is missing, 0 will be assumed
        """
        x = 0 if "x" not in data else data["x"]
        y = 0 if "y" not in data else data["y"]
        z = 0 if "z" not in data else data["z"]
        rx = 0 if "rx" not in data else data["rx"]
        ry = 0 if "ry" not in data else data["ry"]
        rz = 0 if "rz" not in data else data["rz"]

        return Transform((x, y, z), (rx, ry, rz))
