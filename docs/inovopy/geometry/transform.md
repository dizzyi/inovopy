Module inovopy.geometry.transform
=================================
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

Functions
---------

`euler_to_mat(euler_deg: Tuple[float, float, float]) ‑> numpy.ndarray[tuple[int, ...], numpy.dtype[numpy.float64]]`
:   translate euler angle to rotation matrix

`mat_to_euler(mat: numpy.ndarray[tuple[int, ...], numpy.dtype[numpy.float64]]) ‑> Tuple[float, float, float]`
:   translate rotation matrix to euler angle

`rx_mat(deg: float) ‑> numpy.ndarray[tuple[int, ...], numpy.dtype[numpy.float64]]`
:   compute rotation matrx of rotation along x axis

`ry_mat(deg: float) ‑> numpy.ndarray[tuple[int, ...], numpy.dtype[numpy.float64]]`
:   compute rotation matrx of rotation along y axis

`rz_mat(deg: float) ‑> numpy.ndarray[tuple[int, ...], numpy.dtype[numpy.float64]]`
:   compute rotation matrx of rotation along z axis

Classes
-------

`Transform(vec_mm: Tuple[float, float, float] = (0, 0, 0), euler_deg: Tuple[float, float, float] = (0, 0, 0))`
:   # Transform
    A class representing spatial transform,
    compose of a translation and a rotation
    
    ## Representation
    - `vec_mm` : a 3D vector with unit in mm
    - `euler_deg` : a set of euler angle wiht unit in degree
    
    initalize a transform
    
    ## Parameter
    - `vec_mm` : a 3D vector with unit in mm
    - `euler_deg` : a set of euler angle wiht unit in degree

    ### Ancestors (in MRO)

    * inovopy.geometry.IntoRobotCommand
    * abc.ABC

    ### Static methods

    `from_dict(data: dict[str, str | float]) ‑> inovopy.geometry.transform.Transform`
    :   construct a new `Transform` from a dictionary
        
        ## Parameter
        - `data: dict[str, str|float]`: the data, if field is missing, 0 will be assumed

    `from_euler(rx_deg: float = 0, ry_deg: float = 0, rz_deg: float = 0) ‑> inovopy.geometry.transform.Transform`
    :   Construct a new `Transform` from euler angle set

    `from_homogenous(mat: numpy.ndarray[tuple[int, ...], numpy.dtype[numpy.float64]]) ‑> inovopy.geometry.transform.Transform`
    :   construct a transform from a `np.array` 4x4 homogenous matrix
        
        ## Parameter:
        - `mat : np.array` : 4x4 homogenous matrix representation of the transform
        
        ## Return:
        - `Transform`

    `from_robot(res: str) ‑> inovopy.geometry.transform.Transform`
    :   Parse robot transform response into `Transform`

    `from_rx(rx_deg: float) ‑> inovopy.geometry.transform.Transform`
    :   Construct a new `Transform` with specified rx

    `from_ry(ry_deg: float) ‑> inovopy.geometry.transform.Transform`
    :   Construct a new `Transform` with specified ry

    `from_rz(rz_deg: float) ‑> inovopy.geometry.transform.Transform`
    :   Construct a new `Transform` with specified rz

    `from_vec(x_mm: float = 0, y_mm: float = 0, z_mm: float = 0) ‑> inovopy.geometry.transform.Transform`
    :   Construct a new `Transform` from vector componment

    `from_x(x_mm: float) ‑> inovopy.geometry.transform.Transform`
    :   Construct a new `Transform` with specified x

    `from_y(y_mm: float) ‑> inovopy.geometry.transform.Transform`
    :   Construct a new `Transform` with specified y

    `from_z(z_mm: float) ‑> inovopy.geometry.transform.Transform`
    :   Construct a new `Transform` with specified z

    ### Methods

    `clone(self) ‑> inovopy.geometry.transform.Transform`
    :   clone the transform

    `euler_only(self) ‑> inovopy.geometry.transform.Transform`
    :   Extract rotation from `self` and construct a new transfrom

    `inv(self) ‑> inovopy.geometry.transform.Transform`
    :   return the inverse transform of `self`

    `set_euler(self, rx_deg: float, ry_deg: float, rz_deg: float) ‑> inovopy.geometry.transform.Transform`
    :   set the euler angle

    `set_rx(self, deg: float) ‑> inovopy.geometry.transform.Transform`
    :   set the rx component to a specified value

    `set_ry(self, deg: float) ‑> inovopy.geometry.transform.Transform`
    :   set the ry component to a specified value

    `set_rz(self, deg: float) ‑> inovopy.geometry.transform.Transform`
    :   set the rz component to a specified value

    `set_vec(self, x_mm: float, y_mm: float, z_mm: float) ‑> inovopy.geometry.transform.Transform`
    :   set the vector

    `set_x(self, mm: float) ‑> inovopy.geometry.transform.Transform`
    :   set the x component to a specified value

    `set_y(self, mm: float) ‑> inovopy.geometry.transform.Transform`
    :   set the y component to a specified value

    `set_z(self, mm: float) ‑> inovopy.geometry.transform.Transform`
    :   set the z component to a specified value

    `then(self, transform: Transform) ‑> inovopy.geometry.transform.Transform`
    :   return a new transform that is apply a transform to `self`
        
        ## Parameter
        - `transform` : the transform to apply to `self`
        
        ## Return
        - `transform` : resulted transform

    `then_relative(self, transform: Transform) ‑> inovopy.geometry.transform.Transform`
    :   return a new transform that apply a transform relative `self`'s position

    `then_relative_rx(self, deg: float) ‑> inovopy.geometry.transform.Transform`
    :   return a new transform that apply relative rotaion along axis x

    `then_relative_ry(self, deg: float) ‑> inovopy.geometry.transform.Transform`
    :   return a new transform that apply relative rotaion along axis y

    `then_relative_rz(self, deg: float) ‑> inovopy.geometry.transform.Transform`
    :   return a new transform that apply relative rotaion along axis z

    `then_relative_to(self, transform: Transform, reference: Transform) ‑> inovopy.geometry.transform.Transform`
    :   return a new transform that,
        apply a transform to `self` relative to a reference
        
        ## Parameter
        - `transform` : the transform to apply
        - `reference` : the reference of the transfrom

    `then_rx(self, deg: float) ‑> inovopy.geometry.transform.Transform`
    :   return a new transform that apply rotation along x axis to `self`

    `then_ry(self, deg: float) ‑> inovopy.geometry.transform.Transform`
    :   return a new transform that apply rotation along y axis to `self`

    `then_rz(self, deg: float) ‑> inovopy.geometry.transform.Transform`
    :   return a new transform that apply rotation along z axis to `self`

    `then_x(self, cm: float) ‑> inovopy.geometry.transform.Transform`
    :   return a new transform that apply translation along x axis to `self`

    `then_y(self, cm: float) ‑> inovopy.geometry.transform.Transform`
    :   return a new transform that apply translation along y axis to `self`

    `then_z(self, cm: float) ‑> inovopy.geometry.transform.Transform`
    :   return a new transform that apply translation along z axis to `self`

    `to_dict(self) ‑> dict[str, str | float]`
    :   return a `dict[str,str|float]` representation of the transform

    `to_homogenous(self) ‑> numpy.ndarray[tuple[int, ...], numpy.dtype[numpy.float64]]`
    :   return a homogenous matrix representation of the `self`
        
        ## Return:
        - `np.array` : 4x4 homogenous matrix representation of the transform

    `vec_only(self) ‑> inovopy.geometry.transform.Transform`
    :   Extract translation from `self` and construct a new transfrom