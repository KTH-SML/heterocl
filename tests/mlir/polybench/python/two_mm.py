import heterocl as hcl
import numpy as np


def top_2mm(
    P=16, Q=22, R=18, S=24, alpha=0.1, beta=0.1, dtype=hcl.Float(32), target=None
):

    hcl.init(dtype)
    A = hcl.placeholder((P, Q), "A")
    B = hcl.placeholder((Q, R), "B")
    C = hcl.placeholder((R, S), "C")
    D = hcl.placeholder((P, S), "D")

    def kernel_2mm(A, B, C, D):

        r = hcl.reduce_axis(0, Q, "r")
        out_AB = hcl.compute(
            (P, R),
            lambda x, y: hcl.sum(A[x, r] * B[r, y], axis=r, dtype=dtype),
            name="out_AB",
        )

        k = hcl.reduce_axis(0, R, "k")
        out_ABC = hcl.compute(
            (P, S),
            lambda x, y: hcl.sum(out_AB[x, k] * C[k, y], axis=k, dtype=dtype),
            name="out_ABC",
        )
        E = hcl.compute(
            D.shape,
            lambda x, y: (alpha * out_ABC[x, y] + beta * D[x, y]),
            dtype=dtype,
            name="E",
        )
        return E

    s1 = hcl.create_schedule([A, B, C, D], kernel_2mm)
    s2 = hcl.create_schedule([A, B, C, D], kernel_2mm)
    s3 = hcl.create_schedule([A, B, C, D], kernel_2mm)

    #### Applying customizations ####
    AB = kernel_2mm.out_AB
    ABC = kernel_2mm.out_ABC
    E = kernel_2mm.E

    s1[AB].compute_at(s1[ABC], ABC.axis[0])
    s1[ABC].compute_at(s1[E], E.axis[0])

    s2[AB].compute_at(s2[ABC], ABC.axis[0])
    s2[ABC].compute_at(s2[E], E.axis[1])

    s3[E].reorder(E.axis[1], E.axis[0])
    s3[AB].compute_at(s3[ABC], ABC.axis[0])

    return (
        hcl.build(s1, target=target),
        hcl.build(s2, target=target),
        hcl.build(s3, target=target),
    )


def main(P=16, Q=22, R=18, S=24, alpha=0.1, beta=0.1):
    f1, f2, f3 = top_2mm(P=P, Q=Q, R=R, S=S, alpha=alpha, beta=beta)
    A = np.random.randint(10, size=(P, Q)).astype(np.float32)
    B = np.random.randint(10, size=(Q, R)).astype(np.float32)
    C = np.random.randint(10, size=(R, S)).astype(np.float32)
    D = np.random.randint(10, size=(P, S)).astype(np.float32)
    res1 = np.zeros((P, S), dtype=np.float32)
    res2 = np.zeros((P, S), dtype=np.float32)
    res3 = np.zeros((P, S), dtype=np.float32)
    f1(A, B, C, D, res1)
    f2(A, B, C, D, res2)
    f3(A, B, C, D, res3)
    golden = alpha * np.matmul(np.matmul(A, B), C) + beta * D
    if (
        np.allclose(golden, res1)
        and np.allclose(res1, res2)
        and np.allclose(res2, res3)
    ):
        print("passed")
    else:
        print("failed")


if __name__ == "__main__":
    main()
