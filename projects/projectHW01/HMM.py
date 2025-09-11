import numpy as np

def normalize(v, axis=None):
    """
    แบ่ง v ด้วยผลรวมตามแกน:
      - axis=None  ใช้กับเวกเตอร์ 1D
      - axis=1     ใช้กับเมทริกซ์ T×nS เพื่อ normalize รายแถว
    """
    if axis is None:
        s = v.sum()
        return v/s if s > 0 else np.ones_like(v)/v.size
    s = v.sum(axis=axis, keepdims=True)
    s = np.where(s == 0, 1.0, s)  # กันหาร 0
    return v / s

def forward_filter(pi0, A, B_emission, obs_seq):
    """
    alphas[t] = P(X_t | e_{1:t})  ขนาด (T, nS)
    """
    alphas = []
    # t = 0
    alpha = normalize(pi0 * B_emission[obs_seq[0]])
    alphas.append(alpha)
    # t = 1..T-1
    for o in obs_seq[1:]:
        alpha = normalize((alpha @ A) * B_emission[o])
        alphas.append(alpha)
    return np.vstack(alphas)  # shape (T, nS)

def backward_messages(A, B_emission, obs_seq):
    """
    betas[t, i] ≈ P(e_{t+1:T} | X_t=i)  (normalize ไว้เพื่อกัน underflow)
    ขนาด (T, nS)
    """
    T = len(obs_seq)
    nS = A.shape[0]
    betas = np.zeros((T, nS))
    betas[-1] = 1.0
    for t in range(T-2, -1, -1):
        o_next = obs_seq[t+1]
        betas[t] = A @ (B_emission[o_next] * betas[t+1])
        betas[t] = normalize(betas[t])  # normalize ต่อสเต็ป
    return betas

def smooth_posteriors(pi0, A, B_emission, obs_seq):
    """
    คืนค่า:
      alphas : filtering posteriors (T, nS)
      gammas : smoothed posteriors  (T, nS)
    """
    alphas = forward_filter(pi0, A, B_emission, obs_seq)  # (T, nS)
    betas  = backward_messages(A, B_emission, obs_seq)    # (T, nS)
    gammas_unnorm = alphas * betas                        # element-wise
    gammas = normalize(gammas_unnorm, axis=1)             # normalize รายแถว
    return alphas, gammas

# ตัวอย่างใช้งาน
if __name__ == "__main__":
    # สถานะ: [Rainy, Sunny]
    pi0 = np.array([0.5, 0.5])
    A   = np.array([[0.7, 0.3],
                    [0.3, 0.7]])
    # สังเกต: Umbrella (U) หรือ not (N)
    B = {
        'U': np.array([0.9, 0.2]),  # [P(U|Rainy), P(U|Sunny)]
        'N': np.array([0.1, 0.8]),
    }
    obs = ['U','U','N']   # e1..e3

    alphas = forward_filter(pi0, A, B, obs)               # filtering
    alphas2, gammas = smooth_posteriors(pi0, A, B, obs)   # smoothing
    print("Filtering P(X_t | e_1:t):\n", alphas)          # แต่ละแถวรวม≈1
    print("Smoothing  P(X_t | e_1:T):\n", gammas)         # แต่ละแถวรวม≈1
