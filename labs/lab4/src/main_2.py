import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def main():
    fig, axes = plt.subplots(3, 1)
    
    fs = 6  
    t = np.arange(0,1,1/fs)
    
    frq = [7,13,19]  
    
    for idx, f in enumerate(frq):
        sig = np.sin(2*np.pi*f*t)
        
        axes[idx].scatter(t,sig,color='black',s=50)
        
        f_cubic = interp1d(t, sig, kind='cubic')
        t_smooth = np.linspace(t[0],t[-1],500)
        signal_cubic = f_cubic(t_smooth)
        axes[idx].plot(t_smooth, signal_cubic)
        
        axes[idx].grid(True)
        axes[idx].set_ylabel('Amplitudine')
        axes[idx].set_title(f'f = {f} Hz')
    
    axes[-1].set_xlabel('Timp (s)')
    
    plt.tight_layout()
    plt.savefig("../plots/2.pdf", dpi=150)
    plt.show()

if __name__ == "__main__":
    main()