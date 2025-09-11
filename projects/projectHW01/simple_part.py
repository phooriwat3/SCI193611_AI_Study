import numpy as np

class ParticleFilter1D:
    def __init__(self, N=1000, init_mean=0.0, init_std=5.0, seed=0):
        self.rng = np.random.default_rng(seed)
        self.N = N
        self.particles = self.rng.normal(init_mean, init_std, N)
        self.weights = np.ones(N) / N

    def predict(self, u, sigma_proc):
        self.particles += u + self.rng.normal(0.0, sigma_proc, self.N)

    def update(self, z, sigma_meas):
        # likelihood ∝ N(z | x, sigma_meas^2)
        w = np.exp(-0.5*((z - self.particles)/sigma_meas)**2) / (sigma_meas*np.sqrt(2*np.pi))
        w += 1e-300
        self.weights = w / w.sum()

    def resample_systematic(self):
        c = np.cumsum(self.weights)
        r0 = self.rng.random() / self.N
        r = r0 + np.arange(self.N) / self.N
        idx = np.searchsorted(c, r)
        self.particles = self.particles[idx]
        self.weights[:] = 1.0 / self.N

    def estimate(self):
        return np.average(self.particles, weights=self.weights)

# ตัวอย่างจำลองสั้น ๆ
if __name__ == "__main__":
    pf = ParticleFilter1D(N=2000, init_mean=0, init_std=10, seed=42)
    true_x, est = 0.0, []
    sigma_proc, sigma_meas = 0.5, 2.0
    for t in range(30):
        u = 1.0                         # ความเร็วคงที่ 1 หน่วย/สเต็ป
        true_x = true_x + u + np.random.normal(0, sigma_proc)
        z = true_x + np.random.normal(0, sigma_meas)

        pf.predict(u, sigma_proc)       # ขั้น predict
        pf.update(z, sigma_meas)        # ขั้น update (คำนวณน้ำหนัก)
        pf.resample_systematic()        # ขั้น resample
        est.append(pf.estimate())

    print("estimate last =", est[-1])
