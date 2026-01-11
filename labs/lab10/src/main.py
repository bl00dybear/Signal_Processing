import numpy as np
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from cvxopt import matrix, solvers


def generate_series(N):
    t = np.arange(N)

    trend = 0.00005 * t**2 + 0.01*t + 5
    sezon = 10 * np.sin(2*np.pi*t/50) + 5*np.sin(2*np.pi*t/20)
    variatii = np.random.normal(0, 2, N)

    serie = trend + sezon + variatii

    return serie



def autoregresie(serie, p):
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

    return coef



def build_regressor_matrix(serie,p):
    Y=[]
    y=[]

    for i in range (p,len(serie)):
        row = serie[i-p:i]
        Y.append(row[::-1])
        y.append(serie[i])

    return np.array(Y), np.array(y)


def greedy_forward_selection(Y, y, k_features):
    _,n_total_features = Y.shape
    selected_indices = []
    remaining_indices = list(range(n_total_features))
    
    for _ in range(k_features):
        best_mse = float('inf')
        best_feature = -1
        
        for feature_idx in remaining_indices:
            current_indices = selected_indices + [feature_idx]
            Y_subset = Y[:, current_indices]
            
            model = LinearRegression()
            model.fit(Y_subset, y)
            preds = model.predict(Y_subset)
            mse = mean_squared_error(y, preds)
            
            if mse < best_mse:
                best_mse = mse
                best_feature = feature_idx
        
        if best_feature != -1:
            selected_indices.append(best_feature)
            remaining_indices.remove(best_feature)
            
    final_model = LinearRegression()
    final_model.fit(Y[:, selected_indices], y)

    final_coeffs = np.zeros(n_total_features)
    for idx, coef in zip(selected_indices, final_model.coef_):
        final_coeffs[idx] = coef
        
    return final_coeffs,selected_indices
    

def lasso_regression(X, y, alpha_lasso):
    X = X.astype(float)
    y = y.astype(float)

    y_mean = np.mean(y)
    X_mean = np.mean(X, axis=0)

    X = X - X_mean
    y = y - y_mean

    # min (1/2) z^T P z + q^T z cu z = concat[x,v]
    # z sunt regresorii si v limite pt modul

    m,n=X.shape

    XTX=np.dot(X.T,X)
    P = matrix(
        np.block([
            [2*XTX, np.zeros((n,n))],
            [np.zeros((n,n)), np.zeros((n,n))]
        ])
    )

    XTy = np.dot(X.T,y)
    q = matrix(
        np.concatenate([
            -2*XTy,
            alpha_lasso*np.ones(n)
        ])
    )

    eye = np.eye(n)
    G = matrix(
        np.block([
            [eye, -eye],
            [-eye, -eye]
        ])
    )

    h = matrix(np.zeros(2*n))

    solvers.options['show_progress'] = False
    sol = solvers.qp(P,q,G,h)

    z = np.array(sol['x']).flatten()
    x_sol = z[:n]
    
    return x_sol


def roots(coeffs):
    n = len(coeffs)

    comp = np.zeros((n,n))

    if n > 1:
        comp[1:, :-1] = np.eye(n-1)

    comp[:,-1]=coeffs[::-1]

    var_prop = np.linalg.eigvals(comp)

    return var_prop

def is_stationary(model_coeffs):
    pol_coeffs = [1]+[-val for val in model_coeffs]

    pol_roots = roots(pol_coeffs)

    if np.all(np.abs(pol_roots))>1:
        return True
    else:
        return False

def main():
    N = 1000
    p = 30
    k_greedy = 5
    alpha_lasso = 5000
    # am ajustat parametrul de penalizare incat sa am tot o solutie cu 5 coeficienti
    # pentru seria de timp generata de mine
    #Greedy: [0, 1, 4, 26, 29]
    # Lasso: [ 0  1  7 24 29]

    time_series = generate_series(N)
    X, y = build_regressor_matrix(time_series, p)

    greedy_coeffs, greedy_indices = greedy_forward_selection(X, y, k_greedy)
    
    lasso_coeffs = lasso_regression(X, y, alpha_lasso)

    print(f"Greedy: {sorted(greedy_indices)}")
    print(f"Lasso: {np.where(np.abs(lasso_coeffs) > 0.001)[0]}")

    polinom = [2, 1.5, 8, 12, 0.25]

    print(f"\nRadacini: {roots(polinom)}")
    print(f"\nModel AR Greedy stationar: {is_stationary(greedy_coeffs)}")
    print(f"Model AR Lasso stationar: {is_stationary(lasso_coeffs)}")


if __name__ == "__main__":
    main()