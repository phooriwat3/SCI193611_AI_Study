import numpy as np

def stationary_via_linear(P: np.ndarray) -> np.ndarray:
    
    # หา stationary distribution π จากเงื่อนไข πP=π และ sum(π)=1
    # วิธี: แก้ (P^T - I)^T π^T = 0 โดยแทนข้อจำกัดด้วยการต่อสมการ sum(π)=1
    
    P = np.asarray(P, dtype=float)
    n = P.shape[0]
    A = (P.T - np.eye(n))
    # แทน nullspace ด้วยวิธี least squares โดยเพิ่มสมการ sum(π)=1
    A_aug = np.vstack([A, np.ones((1, n))])
    b_aug = np.zeros(n+1)
    b_aug[-1] = 1.0
    # แก้ least squares
    pi, *_ = np.linalg.lstsq(A_aug, b_aug, rcond=None)
    # อาจมีค่าลบเล็กน้อยจากเลขทศนิยม → clip
    pi = np.clip(pi, 0, None)
    return pi / pi.sum()

def stationary_via_power(P: np.ndarray, iters=10_000, tol=1e-12) -> np.ndarray:
    
    # Power iteration: เริ่มจากเวกเตอร์บวก อัปเดต π_{k+1}=π_k P จนคงตัว
    
    n = P.shape[0]
    pi = np.ones(n) / n
    for _ in range(iters):
        new = pi @ P
        if np.linalg.norm(new - pi, 1) < tol:
            return new / new.sum()
        pi = new
    return pi / pi.sum()

# ตัวอย่างใช้งาน
if __name__ == "__main__":
    P = np.array([[0.5, 0.5, 0.0],
                  [0.25, 0.5, 0.25],
                  [0.0, 0.5, 0.5]])
    pi_lin   = stationary_via_linear(P)
    pi_power = stationary_via_power(P)
    print("π (linear) =", pi_lin)     # ควรได้ [0.25, 0.5, 0.25]
    print("π (power)  =", pi_power)
