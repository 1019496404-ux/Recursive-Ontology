import numpy as np
from zlib import compress
import math

np.random.seed(42)
N = 1500  # time steps
D = 10    # state dimension
alpha = 0.15
beta = 0.08

def lz_complexity(seq):
    s = ''.join(['1' if x > 0 else '0' for x in seq])
    return len(compress(s.encode(), 9))

# ==== Simulation A: logical-emergence window ====
S = np.zeros((N, D))
W = np.zeros((N, D))
P = np.zeros(D)

for n in range(N):
    if n < 400:
        W[n] = np.random.randn(D) * 0.05
    else:
        W[n] = np.random.randn(D) * 0.5

for n in range(1, N):
    err = W[n] - P
    grad = np.random.randn(D) * 0.1
    noise = np.random.randn(D) * 0.05
    S[n] = S[n-1] + alpha * err + beta * grad + noise
    P = 0.9 * P + 0.1 * S[n]

C = np.zeros(N)
for n in range(10, N):
    C[n] = lz_complexity(S[:n, 0])

seg1 = np.mean(C[50:399])
seg2 = np.mean(C[500:700])
seg3 = np.mean(C[800:1500])
print(f'[A] fetal C={seg1:.1f}, early C={seg2:.1f}, late C={seg3:.1f}')

threshold = 0.08
K = 10
diff_norm = np.linalg.norm(np.diff(S, axis=0), axis=1)
for n in range(K, N-1):
    if np.all(diff_norm[n-K:n] > threshold):
        print(f'[A] emergence @ step {n}')
        break

# ==== Simulation B: time perception vs difference density ====
def run_B(high, seed=7):
    np.random.seed(seed)
    S = np.zeros(D)
    P = np.zeros(D)
    diffs = np.zeros(500)
    std_val = 0.8 if high else 0.02
    for n in range(500):
        w = np.random.randn(D) * std_val
        if not high:
            w += 0.01 * math.sin(n / 30.0)
        err = w - P
        grad = np.random.randn(D) * 0.05
        noise = np.random.randn(D) * 0.02
        S_new = S + alpha * err + beta * grad + noise
        diffs[n] = np.linalg.norm(S_new - S)
        S = S_new
        P = 0.9 * P + 0.1 * S
    return diffs

diff_high = run_B(True)
diff_low = run_B(False)
print(f'[B] high={diff_high.sum():.2f}, low={diff_low.sum():.2f}, ratio={diff_high.sum()/diff_low.sum():.2f}x')

# ==== Simulation C: irrational residual ====
def cf_sqrt2(N):
    a = [1] + [2] * N
    def next_conv(m):
        p0, p1 = 1, a[0]
        q0, q1 = 0, 1
        for i in range(1, m+1):
            p0, p1 = p1, a[i]*p1 + p0
            q0, q1 = q1, a[i]*q1 + q0
        return p1 / q1
    return [abs(math.sqrt(2) - next_conv(i)) for i in range(1, N+1)]

def bisect_sqrt2(N):
    res = []
    lo, hi = 1.0, 2.0
    for _ in range(N):
        mid = (lo + hi) / 2
        res.append(abs(math.sqrt(2) - mid))
        if mid * mid < 2:
            lo = mid
        else:
            hi = mid
    return res

# ==== Simulation D: flow mode vs normal mode ====
np.random.seed(42)
S = np.zeros((N, D))
P = np.zeros(D)

for n in range(N):
    if n < 500:
        W = np.random.randn(D) * 0.5
    else:
        W = np.random.randn(D) * 0.3
    err = W - P
    grad = np.random.randn(D) * 0.1
    noise = np.random.randn(D) * 0.05
    S[n] = S[n-1] + alpha * err + beta * grad + noise
    P = 0.9 * P + 0.1 * S[n]

norm_ent = np.mean([np.std(S[100:500, i]) for i in range(D)])
flow_ent = np.mean([np.std(S[800:1400, i]) for i in range(D)])
print(f'[D] normal={norm_ent:.4f}, flow={flow_ent:.4f}, drop={(1-flow_ent/norm_ent)*100:.1f}%')
