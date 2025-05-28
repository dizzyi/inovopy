"""
# Joint Coord Module
This module provide joint space representation class for joint space

## Class
- `JointCoord` : 6D joint space representation
"""

import re
from inovopy.geometry import IntoRobotCommand
from inovopy.geometry.transform import rad_to_deg


class JointCoord(IntoRobotCommand):
    """
    # JointCoord
    A class representing 6D joint space of robot
    """

    def __init__(
        self,
        j1_deg: float = 0,
        j2_deg: float = 0,
        j3_deg: float = 0,
        j4_deg: float = 0,
        j5_deg: float = 0,
        j6_deg: float = 0,
    ):
        """
        Construct a new joint space representation from all joint angle
        """
        self.joint_coord_deg: list[float] = [
            float(j1_deg),
            float(j2_deg),
            float(j3_deg),
            float(j4_deg),
            float(j5_deg),
            float(j6_deg),
        ]

    def __str__(self) -> str:
        return str([str(q) for q in self.joint_coord_deg])

    def __add__(self, rhs: "JointCoord") -> "JointCoord":
        out = JointCoord()
        out.joint_coord_deg = [(self[i] + rhs[i]) for i in range(6)]
        return out

    def __neg__(self) -> "JointCoord":
        neg = []

        for j in self.joint_coord_deg:
            neg.append(-j)

        JointCoord.from_list(neg)

    def __getitem__(self, idx: int) -> float:
        return self.joint_coord_deg[idx]

    @classmethod
    def from_robot(cls, res: str) -> "JointCoord":
        """
        Parse Robot input to `JointCoord`

        example input:

        `{joints : [-1.545941, -0.087197, -0.111058, -2.998237, 1.762412, 3.399661, ],
        tcp : {rx : -1.793361, ry : 0.255386, rz : 1.682603,
        x : -0.073378, y : -0.014815, z : 0.929764, },
        tcpid : tool_plate, }`
        """
        res = re.findall(r"\[.*\]", res)[0]
        res = re.sub(r"[ \[\]]", "", res).split(",")
        joints: list[float] = []
        for i in range(6):
            try:
                joints.append(rad_to_deg(float(res[i])))
            except (ValueError, IndexError):
                joints.append(0)
        return JointCoord(
            joints[0],
            joints[1],
            joints[2],
            joints[3],
            joints[4],
            joints[5],
        )

    @classmethod
    def from_list(cls, coord: list[float]) -> "JointCoord":
        """Construst a new `JointCoord` with specified coord"""
        assert len(coord) >= 6
        for i in range(6):
            coord[i] = float(coord[i])
        return JointCoord(
            j1_deg=coord[0],
            j2_deg=coord[1],
            j3_deg=coord[2],
            j4_deg=coord[3],
            j5_deg=coord[4],
            j6_deg=coord[5],
        )

    @classmethod
    def from_j1(cls, deg: float = 0) -> "JointCoord":
        """Construct a new `JointCoord` with specified joint 1"""
        return JointCoord(j1_deg=deg)

    @classmethod
    def from_j2(cls, deg: float = 0) -> "JointCoord":
        """Construct a new `JointCoord` with specified joint 2"""
        return JointCoord(j1_deg=deg)

    @classmethod
    def from_j3(cls, deg: float = 0) -> "JointCoord":
        """Construct a new `JointCoord` with specified joint 3"""
        return JointCoord(j1_deg=deg)

    @classmethod
    def from_j4(cls, deg: float = 0) -> "JointCoord":
        """Construct a new `JointCoord` with specified joint 4"""
        return JointCoord(j1_deg=deg)

    @classmethod
    def from_j5(cls, deg: float = 0) -> "JointCoord":
        """Construct a new `JointCoord` with specified joint 5"""
        return JointCoord(j1_deg=deg)

    @classmethod
    def from_j6(cls, deg: float = 0) -> "JointCoord":
        """Construct a new `JointCoord` with specified joint 6"""
        return JointCoord(j1_deg=deg)

    def then_j1(self, deg: float = 0) -> "JointCoord":
        """Return a new `JointCoord` with a by roating joint 1"""
        return self + JointCoord.from_j1(deg)

    def then_j2(self, deg: float = 0) -> "JointCoord":
        """Return a new `JointCoord` with a by roating joint 2"""
        return self + JointCoord.from_j2(deg)

    def then_j3(self, deg: float = 0) -> "JointCoord":
        """Return a new `JointCoord` with a by roating joint 3"""
        return self + JointCoord.from_j3(deg)

    def then_j4(self, deg: float = 0) -> "JointCoord":
        """Return a new `JointCoord` with a by roating joint 4"""
        return self + JointCoord.from_j4(deg)

    def then_j5(self, deg: float = 0) -> "JointCoord":
        """Return a new `JointCoord` with a by roating joint 5"""
        return self + JointCoord.from_j5(deg)

    def then_j6(self, deg: float = 0) -> "JointCoord":
        """Return a new `JointCoord` with a by roating joint 6"""
        return self + JointCoord.from_j6(deg)

    def to_dict(self) -> dict[str, str | float]:
        """return a `dict[str,str|float]` representation of the `JointCoord`"""
        return {
            "target": "joint_coord",
            "j1": self.joint_coord_deg[0],
            "j2": self.joint_coord_deg[1],
            "j3": self.joint_coord_deg[2],
            "j4": self.joint_coord_deg[3],
            "j5": self.joint_coord_deg[4],
            "j6": self.joint_coord_deg[5],
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | float]) -> "JointCoord":
        """
        construct a new `JointCoord` from a dictionary

        ## Parameter
        - `data: dict[str, str|float]`: the data, if field is missing, 0 will be assumed
        """
        j1 = 0 if "j1" not in data else data["j1"]
        j2 = 0 if "j2" not in data else data["j2"]
        j3 = 0 if "j3" not in data else data["j3"]
        j4 = 0 if "j4" not in data else data["j4"]
        j5 = 0 if "j5" not in data else data["j5"]
        j6 = 0 if "j6" not in data else data["j6"]
        return JointCoord(j1, j2, j3, j4, j5, j6)
