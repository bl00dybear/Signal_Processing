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
        
        f_real = interp1d(t, real_part[ii, :], kind='cubic')
        f_imag = interp1d(t, imag_part[ii, :], kind='cubic')
        
        t_smooth = np.linspace(0, n-1, 200)
        
        axes[ii].plot(t_smooth, f_real(t_smooth))
        axes[ii].plot(t_smooth, f_imag(t_smooth))
        axes[ii].plot(t, real_part[ii, :], 'bo') 
        axes[ii].plot(t, imag_part[ii, :], 'ro')
        axes[ii].grid(True)
        
    plt.savefig("../plots/1.pdf")
    plt.show()
    plt.close()
        
    f_h_mat = np.real(cp_f_mat)-1j*np.imag(cp_f_mat)
    f_h_mat = f_h_mat/np.sqrt(n)
    
    prod_mat = np.dot(f_h_mat,f_mat)
    
    
    # print(prod_mat)
    
    print(np.allclose(prod_mat,np.identity(n)))
        
    
def _2():
    t=np.linspace(0,1,1000)
    sign=np.sin(2*np.pi*2*t)
    omegas = [2.0,3.0,4.0,5.0]
    
    fig,axes = plt.subplots(5,1,figsize=(7,50))
    i=1
    axes[0].plot(t,sign)
    axes[0].set_xlabel("Timp")
    axes[0].set_ylabel("Amplitudine")
    for omega in omegas:
        funct = sign * np.exp(-2j*np.pi*t*omega)
        distances = np.abs(funct)
        
        scatter=axes[i].scatter(np.real(funct), np.imag(funct),c=distances, cmap='viridis', s=3)
        axes[i].set_xlabel("Real")
        axes[i].set_ylabel("Imaginar")
        axes[i].set_aspect('equal')
        fig.colorbar(scatter, ax=axes[i], label='Distanta de la origine')
        i+=1

    plt.subplots_adjust(hspace=0.5)
    plt.savefig("../plots/2.pdf")
    plt.show()
    plt.close()
    
    
def _3():
    t=np.linspace(0,1,100)
    sig1=np.sin(2*np.pi*2*t)
    sig2=np.sin(2*np.pi*4*t)
    sig3=np.sin(2*np.pi*8*t)
    
    sig=sig1+sig2+sig3
    
    fig,axes = plt.subplots(2,1,figsize=(7,25))
    axes[0].plot(t,sig)
    axes[0].set_xlabel("Timp")
    axes[0].set_ylabel("Amplitudine")
    axes[0].grid(True)
    
    n=100
    F = np.zeros(shape=(n,n), dtype=complex)
    for ii in range (n):
        for jj in range (n):
            F[ii][jj] = math.e**(-2j*math.pi*ii*jj/n)
            
    F = F/np.sqrt(n)
    
    X=np.dot(F,sig)
    freq = np.arange(n)
    modul = np.abs(X)
    
    axes[1].stem(freq[:n//2], modul[:n//2])
    axes[1].set_xlabel("Frecventa")
    axes[1].set_ylabel("Modul")
    axes[1].set_title("DFT")
    axes[1].grid(True)
    
    plt.savefig("../plots/3.pdf")
    plt.show()
    plt.close()
    

def main():
    _3()
    


if __name__ == "__main__":
    main()