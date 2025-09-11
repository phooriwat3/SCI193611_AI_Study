import numpy as np

# (A) Beam model 1D (ฉบับย่อ) สำหรับระยะทาง z เทียบกับ z* ที่คาดจากแผนที่
def beam_model_likelihood(z, z_star, z_max,
                          w_hit=0.7, sigma_hit=0.5,
                          w_short=0.1, lam=2.0,
                          w_max=0.1, w_rand=0.1):
    """
    p(z | x,m) = w_hit*N(z; z*, sigma^2) + w_short*Exp(z;lam) (cut at z*)
               + w_max*delta(z=z_max) + w_rand*Uniform(0,z_max)
    """
    z = float(z); z_star = float(z_star)
    # hit (Gaussian)
    p_hit = (np.exp(-0.5*((z-z_star)/sigma_hit)**2) /
             (sigma_hit*np.sqrt(2*np.pi)))
    # short (exponential, support [0, z*])
    p_short = (lam*np.exp(-lam*z)) if (0 <= z <= z_star) else 0.0
    # max (spike ที่ z_max)
    p_max = 1.0 if abs(z - z_max) < 1e-9 else 0.0
    # random (uniform)
    p_rand = (1.0/z_max) if (0 <= z <= z_max) else 0.0
    # ผสม
    p = w_hit*p_hit + w_short*p_short + w_max*p_max + w_rand*p_rand
    # กัน NaN
    return max(p, 1e-12)

# (B) Landmark range-bearing Gaussian model
def landmark_likelihood(z_range, z_bearing, x, y, theta, xl, yl, R=None):
    """
    วัดระยะและมุมถึงหมุด (landmark) หนึ่งตัว
    z = h(x) + v, v ~ N(0, R) โดย R เป็น 2x2 covariance
    """
    if R is None:
        R = np.diag([0.5**2, (5.0*np.pi/180)**2])  # range 0.5m, bearing 5deg

    dx, dy = x - xl, y - yl
    r = np.hypot(dx, dy)
    b = np.arctan2(dy, dx) - theta
    # normalize bearing to [-pi, pi]
    b = (b + np.pi)%(2*np.pi) - np.pi
    z = np.array([z_range, z_bearing])
    h = np.array([r, b])
    e = z - h
    e[1] = (e[1] + np.pi)%(2*np.pi) - np.pi
    invR = np.linalg.inv(R)
    ll = np.exp(-0.5 * (e @ invR @ e)) / (2*np.pi*np.sqrt(np.linalg.det(R)))
    return float(ll)

# ตัวอย่างสั้น ๆ
if __name__ == "__main__":
    print("Beam like =", beam_model_likelihood(z=4.9, z_star=5.0, z_max=10.0))
    print("Landmark like =", landmark_likelihood(5.0, 0.1, x=1,y=2,theta=0.2, xl=4,yl=6))
