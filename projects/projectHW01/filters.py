import numpy as np

def simulate_cv(T=50, dt=1.0, a_std=0.2, meas_std=1.0, outlier_prob=0.05, outlier_std=10.0, seed=0):
    rng = np.random.default_rng(seed)
    x = np.array([0.0, 1.0])  # pos, vel
    F = np.array([[1, dt],
                  [0, 1 ]])
    G = np.array([0.5*dt**2, dt])
    Q = (a_std**2) * np.outer(G, G)  # process noise from accel
    H = np.array([[1.0, 0.0]])
    R = np.array([[meas_std**2]])
    xs, zs = [], []
    for t in range(T):
        # evolve
        a = rng.normal(0, a_std)
        x = F @ x + G * a
        # measurement with occasional outliers
        z = H @ x + rng.normal(0, meas_std)
        if rng.random() < outlier_prob:
            z += rng.normal(0, outlier_std)
        xs.append(x.copy()); zs.append(float(z))
    return np.array(xs), np.array(zs), F, Q, H, R

def run_kf(zs, F, Q, H, R, x0=None, P0=None):
    n = F.shape[0]
    if x0 is None: x0 = np.zeros(n)
    if P0 is None: P0 = np.eye(n)*10.0
    x, P = x0.copy(), P0.copy()
    xs_f = []
    for z in zs:
        # predict
        x = F @ x
        P = F @ P @ F.T + Q
        # update
        y = z - H @ x
        S = H @ P @ H.T + R
        K = P @ H.T @ np.linalg.inv(S)
        x = x + (K @ y)
        P = (np.eye(n) - K @ H) @ P
        xs_f.append(x.copy())
    return np.array(xs_f)

class PF1D_CV:
    def __init__(self, N=2000, seed=0):
        self.rng = np.random.default_rng(seed)
        self.N = N
        # state = [pos, vel]
        self.X = np.column_stack([
            self.rng.normal(0, 10, N),
            self.rng.normal(0, 5, N)
        ])
        self.W = np.ones(N)/N

    def predict(self, F, a_std):
        dt = F[0,1]
        a = self.rng.normal(0, a_std, self.N)
        self.X[:,0] = self.X[:,0] + dt*self.X[:,1] + 0.5*(dt**2)*a
        self.X[:,1] = self.X[:,1] + dt*a

    def update(self, z, meas_std):
        # likelihood of position-only measurement
        err = z - self.X[:,0]
        w = np.exp(-0.5*(err/meas_std)**2)/(meas_std*np.sqrt(2*np.pi))
        w += 1e-300
        self.W = w / w.sum()

    def resample(self):
        c = np.cumsum(self.W)
        r0 = self.rng.random()/self.N
        r = r0 + np.arange(self.N)/self.N
        idx = np.searchsorted(c, r)
        self.X = self.X[idx].copy()
        self.W[:] = 1.0/self.N

    def estimate(self):
        return np.average(self.X, axis=0, weights=self.W)

def rmse(a, b):
    return np.sqrt(((a-b)**2).mean())

if __name__ == "__main__":
    xs_true, zs, F, Q, H, R = simulate_cv(T=60, dt=1.0, a_std=0.2, meas_std=1.0,
                                          outlier_prob=0.05, outlier_std=10.0, seed=1)
    # KF
    xs_kf = run_kf(zs, F, Q, H, R, x0=np.array([0,1]), P0=np.eye(2)*10)
    # PF
    pf = PF1D_CV(N=3000, seed=2)
    est_pf = []
    for z in zs:
        pf.predict(F, a_std=0.2)
        pf.update(z, meas_std=1.0)
        pf.resample()
        est_pf.append(pf.estimate())
    xs_pf = np.array(est_pf)

    # เปรียบเทียบเฉพาะตำแหน่ง
    kf_rmse = rmse(xs_kf[:,0], xs_true[:,0])
    pf_rmse = rmse(xs_pf[:,0], xs_true[:,0])
    print(f"RMSE position  KF={kf_rmse:.3f}  PF={pf_rmse:.3f}")

