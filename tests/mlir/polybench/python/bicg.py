import heterocl as hcl
import numpy as np

def top_bicg(M, N, dtype=hcl.Int(), target=None):

    hcl.init(dtype)
    A = hcl.placeholder((N, M), "A")
    p = hcl.placeholder((M, ), "p")
    r = hcl.placeholder((N, ), "r")
    q = hcl.placeholder((N, ), "q")
    s = hcl.placeholder((M, ), "s")

    def kernel_bicg(A, p, r, q, s):
    
        i = hcl.reduce_axis(0, N, "i")
        hcl.update(s,
                   lambda n: hcl.sum(r[i] * A[i, n], axis=i, dtype=dtype),
                   name="s"
                   )

        j = hcl.reduce_axis(0, M, "j")
        hcl.update(q,
                   lambda m: hcl.sum(A[m, j] * p[j], axis=j, dtype=dtype),
                   name="q"
                   )

    sch = hcl.create_schedule([A, p, r, q, s], kernel_bicg)

    #### Applying customizations ####

    s = kernel_bicg.s
    q = kernel_bicg.q

    sch[s].compute_at(sch[q], q.axis[0])

    #### Applying customizations ####

    return hcl.build(sch, target=target)

def bicg_golden(M, N, A, p, r, q, s):

    dtype = np.float32

    for i in range(M):
        s[i] = (dtype)(0)
    for i in range(N):
        q[i] = (dtype)(0)
        for j in range(M):
            s[j] = s[j] + r[i] * A[i][j]
            q[i] = q[i] + A[i][j] * p[j]
    return s, q

def main(M=32, N=32, dtype=hcl.Float(32), target=None):
    A = np.random.randint(10, size=(N, M)).astype(np.float32)
    p = np.random.randint(10, size=(M, )).astype(np.float32)
    r = np.random.randint(10, size=(N, )).astype(np.float32)
    q = np.random.randint(10, size=(N, )).astype(np.float32)
    s = np.random.randint(10, size=(M, )).astype(np.float32)
    f = top_bicg(M, N, dtype, target)
    f(A, p, r, q, s)
    s_golden, q_golden = bicg_golden(M, N, A, p, r, q, s)
    if np.allclose(s, s_golden) and np.allclose(q, q_golden):
        print("pass")
    else:
        print("fail")

if __name__ == "__main__":
    main()