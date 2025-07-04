Module inovopy.geometry.jointcoord
==================================
# Joint Coord Module
This module provide joint space representation class for joint space

## Class
- `JointCoord` : 6D joint space representation

Classes
-------

`JointCoord(j1_deg: float = 0, j2_deg: float = 0, j3_deg: float = 0, j4_deg: float = 0, j5_deg: float = 0, j6_deg: float = 0)`
:   # JointCoord
    A class representing 6D joint space of robot
    
    Construct a new joint space representation from all joint angle

    ### Ancestors (in MRO)

    * inovopy.geometry.IntoRobotCommand
    * abc.ABC

    ### Static methods

    `from_dict(data: dict[str, str | float]) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   construct a new `JointCoord` from a dictionary
        
        ## Parameter
        - `data: dict[str, str|float]`: the data, if field is missing, 0 will be assumed

    `from_j1(deg: float = 0) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Construct a new `JointCoord` with specified joint 1

    `from_j2(deg: float = 0) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Construct a new `JointCoord` with specified joint 2

    `from_j3(deg: float = 0) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Construct a new `JointCoord` with specified joint 3

    `from_j4(deg: float = 0) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Construct a new `JointCoord` with specified joint 4

    `from_j5(deg: float = 0) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Construct a new `JointCoord` with specified joint 5

    `from_j6(deg: float = 0) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Construct a new `JointCoord` with specified joint 6

    `from_list(coord: list[float]) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Construst a new `JointCoord` with specified coord

    `from_robot(res: str) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Parse Robot input to `JointCoord`
        
        example input:
        
        `{joints : [-1.545941, -0.087197, -0.111058, -2.998237, 1.762412, 3.399661, ],
        tcp : {rx : -1.793361, ry : 0.255386, rz : 1.682603,
        x : -0.073378, y : -0.014815, z : 0.929764, },
        tcpid : tool_plate, }`

    ### Methods

    `then_j1(self, deg: float = 0) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Return a new `JointCoord` with a by roating joint 1

    `then_j2(self, deg: float = 0) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Return a new `JointCoord` with a by roating joint 2

    `then_j3(self, deg: float = 0) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Return a new `JointCoord` with a by roating joint 3

    `then_j4(self, deg: float = 0) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Return a new `JointCoord` with a by roating joint 4

    `then_j5(self, deg: float = 0) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Return a new `JointCoord` with a by roating joint 5

    `then_j6(self, deg: float = 0) ‑> inovopy.geometry.jointcoord.JointCoord`
    :   Return a new `JointCoord` with a by roating joint 6

    `to_dict(self) ‑> dict[str, str | float]`
    :   return a `dict[str,str|float]` representation of the `JointCoord`