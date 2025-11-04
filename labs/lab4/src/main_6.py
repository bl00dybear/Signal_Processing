import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

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

def main():
    fs, signal = wavfile.read("../plots/vocale.wav")

    n=len(signal)

    pow2 = 2 ** (int(np.log2(n))+1)
    pad=pow2-n

    # signal = np.hstack([signal, np.ones(pad) * np.mean(signal)])  
    # signal=signal[:-20]
    new_len = n//100
    if new_len%2 :
        new_len-=1
    new_len*=100
    signal=signal[:new_len]
    n=len(signal)
    window_len = int(n*0.01)
    stride = window_len//2
    
    print(window_len,stride)

    global x
    groups=[]
    index=0
    while (index+window_len)<=n:
        x=np.copy(signal[index:index+window_len])
        X=fast_fourier_transform(1,len(x),1)
        groups.append(np.abs(X))
        index+=stride
        
    groups = np.array(groups)

    print(groups.shape)
    print(n)
    spectrogram = groups.T[:len(groups.T)//2, :]
    
    
    freq = np.arange(window_len // 2) * fs / window_len
    
    time_frames = np.arange(spectrogram.shape[1])  
    time_seconds = time_frames * stride / fs  

    fig, ax = plt.subplots(figsize=(12, 6))

    spectrogram_db = 10 * np.log10(spectrogram + 0.00000000000000001)  

    im = ax.imshow(spectrogram_db, aspect='auto', origin='lower',
                cmap='viridis', vmin=-80, vmax=np.max(spectrogram_db),
                extent=[0, time_seconds[-1], 0, freq[-1]])   
    ax.set_xlabel('Timp')
    ax.set_ylabel('Frecvență')
    
    plt.colorbar(im, ax=ax, label='Magnitudine')
    plt.savefig("../plots/6.pdf")
    plt.show()
    
if __name__=="__main__":
    main()