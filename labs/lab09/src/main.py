import numpy as np
import matplotlib.pyplot as plt

def generate_series(N):
    t = np.arange(N)

    trend = 0.00005 * t**2 + 0.01 * t + 5
    sezon = 10 * np.sin(2 * np.pi * t / 50) + 5 * np.sin(2 * np.pi * t / 20)
    variatii = np.random.normal(0, 2, N)

    serie = trend + sezon + variatii

    plt.figure(figsize=(10, 12))

    plt.subplot(4, 1, 1)
    plt.plot(t, serie)
    plt.title('Seria de Timp')

    plt.subplot(4, 1, 2)
    plt.plot(t, trend, color='red')
    plt.title('Trend')

    plt.subplot(4, 1, 3)
    plt.plot(t, sezon, color='green')
    plt.title('Sezon')

    plt.subplot(4, 1, 4)
    plt.plot(t, variatii, color='orange')
    plt.title('Variatii (Zgomot)')

    plt.tight_layout()
    plt.savefig("../plots/1.pdf")
    plt.show()

    return serie

def mediere_simpla(x, alpha, n):
    s = np.zeros(n)
    s[0]=x[0]

    for t in range(1, n):
        s[t] = alpha*x[t]+(1-alpha)*s[t-1]
        
    return s

def mediere_dubla(x, alpha, beta, n):
    s = np.zeros(n)
    s[0] = x[0]
    b = np.zeros(n)
    b[0] = x[1] - x[0]

    for t in range (1,n):
        s[t] = alpha*x[t]+(1-alpha)*(s[t-1]+b[t-1])
        b[t] = beta*(s[t]-s[t-1]) + (1-beta)*(b[t-1])

    return s,b

def mediere_tripla(x, alpha, beta, gamma, L):
    n = len(x)
    
    s = np.zeros(n)
    b = np.zeros(n)
    c = np.ones(n) 
    
    s[0] = x[0]
    b[0] =  x[1] - x[0]
    
    pred = np.zeros(n)
    pred[0] = x[0]
    
    for t in range(1, n):
        pred[t] = (s[t-1] + b[t-1]) * c[t - L]
            
        s[t] = alpha*(x[t]/c[t - L]) + (1-alpha)*(s[t-1]+b[t-1])
        b[t] = beta*(s[t]-s[t-1]) + (1-beta)*b[t-1]
        c[t] = gamma*(x[t]/s[t]) + (1-gamma)*c[t - L]
                
    return s,b,c,pred


def mse(serie,pred):
    sum=0
    for i in range (len(serie)):
        sum += abs(serie[i]-pred[i])

    return sum


def grid_search_simpla(time_series):
    best_alpha = 0
    min_error = float('inf')
    N = len(time_series)
    vals = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]   
    for a in vals:
        s = mediere_simpla(time_series, a, N)
        eroare = mse(time_series, s)
        if eroare < min_error:
            min_error = eroare
            best_alpha = a
    return best_alpha

def grid_search_dubla(time_series):
    best_alpha = 0
    best_beta = 0
    min_error = float('inf')
    N = len(time_series)
    vals = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    for a in vals:
        for b in vals:
            s, _ = mediere_dubla(time_series, a, b, N)
            eroare = mse(time_series, s)
            if eroare < min_error:
                min_error = eroare
                best_alpha = a
                best_beta = b
    return best_alpha, best_beta

def grid_search_tripla(time_series, L):
    best_alpha = 0
    best_beta = 0
    best_gamma = 0
    min_error = float('inf')
    N = len(time_series)
    vals = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    for a in vals:
        for b in vals:
            for g in vals:
                _, _, _, pred = mediere_tripla(time_series, a, b, g, L)
                eroare = mse(time_series, pred)
                if eroare < min_error:
                    min_error = eroare
                    best_alpha = a
                    best_beta = b
                    best_gamma = g
    return best_alpha, best_beta, best_gamma




def main():
    N = 1000
    time_series = generate_series(N)

    opt_a_1 = grid_search_simpla(time_series)
    s1 = mediere_simpla(time_series, opt_a_1, N)
    print(f"Simpla Alpha: {opt_a_1}")

    opt_a_2, opt_b_2 = grid_search_dubla(time_series)
    s2, _ = mediere_dubla(time_series, opt_a_2, opt_b_2, N)
    print(f"Dubla Alpha: {opt_a_2}, Beta: {opt_b_2}")

    L_optim = 50
    opt_a_3, opt_b_3, opt_g_3 = grid_search_tripla(time_series, L=L_optim)
    _, _, _, pred3 = mediere_tripla(time_series, opt_a_3, opt_b_3, opt_g_3, L=L_optim)
    print(f"Tripla Alpha: {opt_a_3}, Beta: {opt_b_3}, Gamma: {opt_g_3}")

    plt.figure(figsize=(12, 6))
    plt.plot(time_series, label='Date Reale', color='gray', alpha=0.5)
    plt.plot(s1, label='Simpla Optim', color='blue')
    plt.plot(s2, label='Dubla Optim', color='orange')
    plt.plot(pred3, label='Tripla Optim', color='red')
    plt.legend()
    plt.savefig("../plots/2.pdf")
    plt.show()


# Simpla Alpha: 0.95
# Dubla Alpha: 0.95, Beta: 0.05
# Tripla Alpha: 0.95, Beta: 0.05, Gamma: 0.05

if __name__ == "__main__":
    main()