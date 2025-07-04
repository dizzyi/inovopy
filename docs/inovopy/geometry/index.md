Module inovopy.geometry
=======================
# Geometry Module
This module provide geometric data structure class for robot control

## Modules
- `transform` : Functions and Class for 3D spatial transform
- `jointcoord` : 6D joint space representation

Sub-modules
-----------
* inovopy.geometry.jointcoord
* inovopy.geometry.transform

Functions
---------

`deg_to_rad(deg: float) ‑> float`
:   translate degree to radian

`rad_to_deg(rad: float) ‑> float`
:   translate radion to degree

Classes
-------

`IntoRobotCommand()`
:   # IntoRobotCommand
    An interface for all class that can be turn into robot command
    
    ## Method
    - `as_motion`
    - `as_linear`
    - `as_linear_relative`
    - `as_joint`
    - `as_joint_relative`

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * inovopy.geometry.jointcoord.JointCoord
    * inovopy.geometry.transform.Transform

    ### Methods

    `as_joint(self) ‑> inovopy.iva.RobotCommand`
    :   construct a new joint motion command from the `self`

    `as_joint_relative(self) ‑> inovopy.iva.RobotCommand`
    :   construct a new joint relative motion command from the `self`

    `as_linear(self) ‑> inovopy.iva.RobotCommand`
    :   construct a new linear motion command from the `self`

    `as_linear_relative(self) ‑> inovopy.iva.RobotCommand`
    :   construct a new linear relative motion command from the `self`

    `as_motion(self, motion_mode: inovopy.iva.MotionMode) ‑> inovopy.iva.RobotCommand`
    :   construct a new motion command from the `self`