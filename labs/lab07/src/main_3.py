from scipy import datasets, ndimage
import numpy as np
import matplotlib.pyplot as plt



def main():
    pixel_noise = 200

    X_orig = datasets.face(gray=True).astype(float)
    noise = np.random.randint(-pixel_noise, high=pixel_noise+1, size=X_orig.shape)
    X_noisy = X_orig + noise

    X = X_noisy.astype(float)

    m, n = X.shape
    spectru = np.fft.fft2(X)

    zgomot_init = np.sum((X_orig - X)**2)
    semnal_init = np.sum(X_orig**2)
    snr_start = 10 * np.log10(semnal_init / zgomot_init)

    print(f"SNR Initial (Zgomotos): {snr_start:.2f} dB") 

    snr_target = 20 
    raza = 0
    snr_curent = snr_start 

    while snr_curent < snr_target:
        raza += 2
        mask = np.zeros_like(spectru)
        
        mask[0:raza, 0:raza] = 1
        mask[0:raza, n-raza:n] = 1
        mask[m-raza:m, 0:raza] = 1
        mask[m-raza:m, n-raza:n] = 1
        
        spectru_filt = spectru * mask
        X_filt = np.abs(np.fft.ifft2(spectru_filt))

        noise = np.sum((X_orig - X_filt)**2)
        sig = np.sum(X_orig**2)
        snr_curent = 10 * np.log10(sig / noise)
        
        if raza > min(m,n)//2: break

    print(f"SNR Final: {snr_curent:.2f} dB")

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(X, cmap=plt.cm.gray)
    plt.title(f"Original Zgomotos (SNR={snr_start:.2f}dB)")
    plt.subplot(1, 2, 2)
    plt.imshow(X_filt, cmap=plt.cm.gray)
    plt.title(f"Filtrat (SNR={snr_curent:.2f}dB)")
    plt.savefig("../plots/3.pdf") 
    plt.show()

if __name__=="__main__":
    main()