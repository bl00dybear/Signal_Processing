import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def _1():
    n=8
    
    f_mat = np.zeros(shape=(n,n), dtype=complex)
    
    # print(np.imag(f_mat))
    
    for ii in range (n):
        for jj in range (n):
            f_mat[ii][jj] = math.e**(-2j*math.pi*ii*jj/n)
            
            
    cp_f_mat = f_mat.copy()
    f_mat = f_mat/np.sqrt(n)
            
            
    real_part = np.real(f_mat)
    imag_part = np.imag(f_mat)
    
    fig,axes = plt.subplots(n,1)
    
    for ii in range(n):
        t = np.arange(n)
        
        # Interpolare spline cubică
        f_real = interp1d(t, real_part[ii, :], kind='cubic')
        f_imag = interp1d(t, imag_part[ii, :], kind='cubic')
        
        # Vector de timp mai dens pentru curbă netedă
        t_smooth = np.linspace(0, n-1, 200)
        
        axes[ii].plot(t_smooth, f_real(t_smooth))
        axes[ii].plot(t_smooth, f_imag(t_smooth))
        axes[ii].plot(t, real_part[ii, :], 'bo') 
        axes[ii].plot(t, imag_part[ii, :], 'ro')
        axes[ii].grid(True)
        
    plt.show()
    plt.savefig("../plots/1.png")
    plt.close()
        
    f_h_mat = np.real(cp_f_mat)-1j*np.imag(cp_f_mat)
    f_h_mat = f_h_mat/np.sqrt(n)
    
    prod_mat = np.dot(f_h_mat,f_mat)
    
    
    # print(prod_mat)
    
    print(np.allclose(prod_mat,np.identity(n)))
        
        

        
def _2():
    pass


def main():
    _1()


if __name__ == "__main__":
    main()