import numpy as np
import matplotlib.pyplot as plt
from main import generate_series,mse
from statsmodels.tsa.arima.model import ARIMA

def ma_model(time_series, q):
    N = len(time_series)
    mu = np.mean(time_series)
    eps = time_series - mu

    X = []
    Y = []

    for t in range(q, N):
        row_errors = eps[t-q : t] 
        X.append(row_errors[::-1]) 
        Y.append(time_series[t] - mu)

    X = np.array(X)
    Y = np.array(Y)
    
    coef,_,_,_ = np.linalg.lstsq(X, Y, rcond=None)
    
    pred = np.full(N, mu)
    
    for t in range(q, N):
        past_errors = eps[t-q : t][::-1]
        errors = np.dot(coef, past_errors)
        pred[t] += errors
        
    return pred

def grid_search_arma(time_series, p_limit, q_limit):
    best_aic = float('inf')
    best_pair = (0, 0)
    best_model = None
        
    for p in range(1,p_limit + 1):
        for q in range(1,q_limit + 1):
            model = ARIMA(time_series, order=(p, 0, q))
            results = model.fit(method_kwargs={'warn_convergence': False})            
            
            if results.aic < best_aic:
                best_aic = results.aic
                best_pair = (p, q)
                best_model = results

                    
    return best_pair, best_model


def main():
    N = 1000
    time_series = generate_series(N)

    q_orizont = 5
    ma_pred = ma_model(time_series, q=q_orizont)
    
    plt.figure(figsize=(12, 6))
    plt.plot(time_series, label='Date Reale', color='gray', alpha=0.5)
    plt.plot(ma_pred, label=f'Model MA(q={q_orizont})', color='purple')
    plt.legend()
    plt.title(f"Model MA cu orizont {q_orizont}")
    plt.savefig("../plots/3.pdf")
    plt.show()


    limit = 10
    
    (opt_p, opt_q), model_final = grid_search_arma(time_series, limit, limit)

    print(f"\nBest pair: ({opt_p}, {opt_q})")

    predictii = model_final.predict(start=0, end=N-1)

    plt.figure(figsize=(12, 6))
    plt.plot(time_series, label='Date Reale', color='gray', alpha=0.5)
    plt.plot(predictii, label=f'ARMA({opt_p}, {opt_q})', color='red', linestyle='--')
    plt.legend()
    plt.title(f"Best pair: (p={opt_p}, q={opt_q})")
    plt.savefig("../plots/4.pdf")
    plt.show()
    

if __name__=="__main__":
    main()