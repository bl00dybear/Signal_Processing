import numpy as np
import time
import matplotlib.pyplot as plt

def fast_fourier_transform(l,r,s):
    if l == r:
        return [x[l]]
    else:
        n=(r-l)+1
        mid = l+n// 2
        even=fast_fourier_transform(l,mid-1,s*2)
        odd=fast_fourier_transform(l+s,mid+s-1,s*2)
        
        X=[0]*n
        for i in range(n//2):
            p=even[i]
            q=np.exp(-2j*np.pi*i/n)*odd[i]
            X[i]=p+q
            X[i+n//2]=p-q
            
        return X


def discrete_fourier_transform(n):
    F = np.zeros(shape=(n,n), dtype=complex)
    for ii in range (n):
        for jj in range (n):
            F[ii][jj] = np.exp(-2j*np.pi*ii*jj/n)
            
    F = F/np.sqrt(n)
    X=np.dot(F,x)
    
    return X


def main():
    global x

    
    sizes=[128, 256, 512, 1024, 2048, 4096, 8192]
    fft=[]
    dft=[]
    npfft=[]
    
    for size in sizes: 
        t=np.linspace(0,1,size)
        x=np.sin(2*np.pi*5*t)+np.sin(2*np.pi*6*t+np.pi/2)
        
        start=time.time()
        X=discrete_fourier_transform(size)
        dft.append(time.time()-start)
        
        start=time.time()
        X=fast_fourier_transform(0,size-1,1)
        fft.append(time.time()-start)
        
        start=time.time()
        X=np.fft.fft(x)
        npfft.append(time.time()-start)
        
        
    plt.plot(sizes, dft, label='DFT', marker='o')
    plt.plot(sizes, fft, label='FFT', marker='s')
    plt.plot(sizes, npfft, label='NumPy FFT', marker='^')
    plt.xlabel('Dimensiune')
    plt.ylabel('Timp')
    plt.legend()
    plt.yscale('log')
    plt.grid(True)
    plt.savefig("../plots/1.pdf")
    plt.show()



if __name__=="__main__":
    main()