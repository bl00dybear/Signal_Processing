from scipy import datasets, ndimage
import numpy as np
import matplotlib.pyplot as plt


def main():
    X=datasets.face(gray=True)
    X = X.astype(float)
    m,n= X.shape
    spectru = np.fft.fft2(X)

    snr_target=20
    raza=0
    snr_curent = 0

    while snr_curent<snr_target:
        raza += 2 
        mask = np.zeros_like(spectru)
        
        mask[0:raza,0:raza] = 1
        mask[0:raza,n-raza:n] = 1
        mask[m-raza:m,0:raza] = 1
        mask[m-raza:m,n-raza:n] = 1
        
        spectru_filt = spectru * mask
        
        X_filt = np.abs(np.fft.ifft2(spectru_filt))
        
        noise=np.sum((X-X_filt)**2)
        sig=np.sum(X**2)
        snr_curent = 10*np.log10(sig/noise)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(X, cmap=plt.cm.gray)
    plt.title("Original")
    plt.subplot(1, 2, 2)
    plt.imshow(X_filt, cmap=plt.cm.gray)
    plt.title(f"Comprimat (SNR={snr_curent:.2f}dB)")
    plt.savefig("../plots/2.pdf")
    plt.show()

if __name__=="__main__":
    main()