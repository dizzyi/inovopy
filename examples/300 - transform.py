from inovopy.geometry.transform import Transform

if __name__ == "__main__":

    # constructor
    print(Transform())
    print(Transform(vec_mm=(0, 1, 0), euler_deg=(0, 0, 0)))

    # constrution functions
    print(Transform.from_x(1))
    print(Transform.from_dict({"rz": 90}))

    # chained construction
    print(Transform.from_x(10).then_rz(90))

    # inverse
    print(Transform.from_rx(45).inv())

    # multiplication
    a = Transform.from_x(10)
    b = Transform.from_rz(90)
    c = b * a
    print(c)
