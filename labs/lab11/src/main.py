import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import hankel, svd, eigh

def generate_series(N):
    t = np.arange(N)
    trend = 0.00005 * t**2 + 0.01*t + 5
    sezon = 10 * np.sin(2*np.pi*t/50) + 5*np.sin(2*np.pi*t/20)
    variatii = np.random.normal(0, 2, N)
    serie = trend + sezon + variatii
    return serie

def diagonal_averaging(X):
    L, K = X.shape
    N = L + K - 1
    result = np.zeros(N)
    
    for k in range(N):
        elements = []
        for i in range(L):
            j = k - i
            if 0 <= j < K:
                elements.append(X[i, j])
        result[k] = np.mean(elements)
    
    return result

def main():
    N = 200
    time_series = generate_series(N)
    
    L = 100
    K = N - L + 1
    
    c = time_series[0:L]
    r = time_series[L-1:N]
    X = hankel(c, r)
    
    XXt = np.dot(X, X.T)
    XtX = np.dot(X.T, X)
    
    eig_vals_XXt, eig_vecs_XXt = eigh(XXt)
    idx = eig_vals_XXt.argsort()[::-1]
    eig_vals_XXt = eig_vals_XXt[idx]
    eig_vecs_XXt = eig_vecs_XXt[:, idx]
    
    U, S, Vt = svd(X)
    
    
    num_components = 3
    X_reconstructed = np.zeros_like(X)
    
    for i in range(num_components):
        component = S[i] * np.outer(U[:, i], Vt[i, :])
        X_reconstructed += component
        
    trend_extracted = diagonal_averaging(X_reconstructed)
    
    plt.figure(figsize=(10, 5))
    plt.plot(time_series, label='Original Series')
    plt.plot(trend_extracted, label=f'SSA Reconstruction (r={num_components})', linewidth=2)
    plt.legend()
    plt.title('SSA: Original vs Reconstructed Trend')
    plt.tight_layout()
    plt.savefig("../plots/1.pdf")
    plt.show()

if __name__ == "__main__":
    main()