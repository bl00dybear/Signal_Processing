import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import lstsq

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


def autocorelate(time_series):
    autocor = np.correlate(time_series, time_series, mode='full')
    autocor = autocor[autocor.size // 2:]
    autocor = autocor / autocor[0]

    plt.figure(figsize=(10, 5))
    plt.plot(autocor)
    plt.title('Vectorul de Autocorelatie')
    plt.savefig("../plots/2.pdf")
    plt.show()

    return autocor

def autoregresie(serie, p, plot=True):
    Y = []
    y = []

    for i in range(p, len(serie)):
        row = serie[i-p:i]
        Y.append(row[::-1])
        y.append(serie[i])

    Y = np.array(Y)
    y = np.array(y)



    Y_bias = np.hstack((np.ones((Y.shape[0], 1)), Y))

    coef, _,_,_ = np.linalg.lstsq(Y_bias, y)

    last_nums = serie[-p:]
    last_nums = last_nums[::-1]
    last_nums = np.r_[1, last_nums]

    predictii = Y_bias.dot(coef)

    new_pred=np.dot(last_nums,coef)

    if plot:
        plt.figure(figsize=(12, 6))
        plt.plot(np.arange(len(serie)), serie, label='Original')
        plt.plot(np.arange(p, len(serie)), predictii, color='red', linestyle='--', label='Predictie Scipy')
        plt.scatter(1001, new_pred, color='red', s=100, zorder=5)
        plt.title(f'Regresie Liniara cu Scipy (AR, p={p})')
        plt.grid(True)
        plt.savefig("../plots/3.pdf")
        plt.show()
        return None
    else:
        return new_pred


def grid_search(time_series):
    total_len = len(time_series)
    test_len = int(total_len * 0.1)
    train_len = total_len - test_len

    p_vals = [1, 2, 3, 4, 5, 10, 15]
    m_vals = [50, 100, 200, 300]

    best_rmse = float('inf')
    best_cfg = None

    print(f"Test size: {test_len} steps")

    for p in p_vals:
        for m in m_vals:
            if m <= p + 5:
                continue

            errors = []

            for i in range(train_len, total_len):
                history_start = max(0, i - m)
                history = time_series[history_start:i]

                actual = time_series[i]

                pred = autoregresie(history, p,False)
                errors.append((pred - actual) ** 2)

            if len(errors) > 0:
                rmse = np.sqrt(np.mean(errors))
                print(f"p={p}, m={m} -> RMSE={rmse:.4f}")

                if rmse < best_rmse:
                    best_rmse = rmse
                    best_cfg = (p, m)

    print(f"p={best_cfg[0]} m={best_cfg[1]} RMSE={best_rmse:.4f}")


def main():
    N = 1000

    time_series = generate_series(N)

    autocor = autocorelate(time_series)
    
    autoregresie(time_series, 50)

    grid_search(time_series)

if __name__ == "__main__":
    main()