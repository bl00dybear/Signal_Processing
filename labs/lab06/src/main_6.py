import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def main():

    #(a)
    df = pd.read_csv("Train.csv")    
    x=np.array(df['Count'])
    x=x[:3*24]
    # print(x)
    t=np.linspace(0,3*24,3*24)

    plt.plot(t,x)
    plt.savefig("../plots/6.1.pdf")
    plt.show()

    #(b)
    w=17
    x=np.convolve(x,np.ones(w), 'valid')/w
    # print(x)

    t=np.linspace(0,3*24,len(x))
    plt.plot(t,x)
    plt.savefig("../plots/6.2.pdf")
    plt.show()

    #(c)
    x=np.array(df['Count'])[:3*24]
    n=len(x)

    X = np.fft.fft(x)
    freqs = np.fft.fftfreq(n) 
    
    indices = np.abs(freqs)>1/6 
    # Am ales 6 ore pentru ca am citit ca este a 4-a "sinusoida" a zilei, practic a 4 a perioada,
    # celelalte fiind la 8,12 si 24 de ore. Daca as alege mai mic de atat as putea pastra evenimentele 
    # neimportante, de exemplu cele de 3 ore care in sine ar fi atenuarile de trafic.
    X[indices] = 0

    x_filtered = np.real(np.fft.ifft(X))

    t=np.linspace(0,3*24,len(x))
    plt.figure()
    plt.plot(t, x, color='gray', alpha=0.5, label='Original')
    plt.plot(t, x_filtered, color='red', linewidth=2, label='Semnal filtrat low pass')
    plt.legend()
    plt.title("Filtrare Frecvente Inalte")
    plt.savefig("../plots/6.3.pdf")
    plt.show()


    fs_hz = 1.0/3600
    nyquist_hz=fs_hz/2
    
    fc_hz=1/6*fs_hz 

    norm_freq=1/6/0.5

    print(f"Frecventa taiere (hz): {fc_hz}")
    print(f"Frecventa Niquist (hz): {nyquist_hz}")
    print(f"Frecventa normalizata: {norm_freq}")

    #(d) (e)
    order=5
    rp=5

    b_butt, a_butt = signal.butter(N=order, Wn=norm_freq, btype='low')
    b_cheby, a_cheby = signal.cheby1(N=order, rp=rp, Wn=norm_freq, btype='low')

    x_butt = signal.filtfilt(b_butt,a_butt,x)
    x_cheby = signal.filtfilt(b_cheby,a_cheby,x)

    t=np.linspace(0,3*24,len(x))
    
    plt.figure(figsize=(12, 6))
    plt.plot(t, x, 'gray', alpha=0.4, label='Original Zgomotos')
    plt.plot(t, x_butt, 'b', linewidth=2, label=f'Butterworth (Ord={order})')
    plt.plot(t, x_cheby, 'r--', linewidth=2, label=f'Chebyshev (Ord={order})')
    
    plt.title(f"Comparatie Filtre: Butterworth vs Chebyshev")
    plt.xlabel("Ore")
    plt.ylabel("Trafic")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f"../plots/6.4.pdf")
    plt.show()

    # aleg Butterworth intrucat copiaza semnalul cat mai fidel, dar mult mai rotunjit
    # in sensul in care nu se pierde sau aduga informatie, cum se observa la Cebysev in zonele low ale graficului

    #(f)
    ordine_de_testat = [2, 5, 10]
    
    plt.figure(figsize=(12, 6))
    plt.plot(t, x, 'gray', alpha=0.3, label='Original')
    
    for ordin in ordine_de_testat:
        b_temp, a_temp = signal.butter(N=ordin, Wn=norm_freq, btype='low')
        x_temp = signal.filtfilt(b_temp, a_temp, x)
        plt.plot(t, x_temp, linewidth=2, label=f'Butterworth Ordin {ordin}')

    plt.title("Experiment 1: Influenta Ordinului (Butterworth)")
    plt.legend()
    plt.savefig("../plots/6.5.pdf")
    plt.show()

    valori_rp = [0.1, 5, 10]

    plt.figure(figsize=(12, 6))
    plt.plot(t, x, 'gray', alpha=0.3, label='Original')

    for val_rp in valori_rp:
        b_temp, a_temp = signal.cheby1(N=5, rp=val_rp, Wn=norm_freq, btype='low')
        x_temp = signal.filtfilt(b_temp, a_temp, x)
        plt.plot(t, x_temp, linewidth=1.5, label=f'Chebyshev rp={val_rp}dB')

    plt.title("Experiment 2: Influenta Ondulatiilor (Chebyshev Ordin 5)")
    plt.legend()
    plt.savefig("../plots/6.6.pdf")
    plt.show()

    # La Butterworth, daca pun ordin mic (2) pare ca capteaza mai multa informatiem deci mai mult zgomot. 
    # daca pun 10 e prea mai neted, dar nu imi da foarte multa incredere in sensul in care nu pierde mai 
    # multa informatie (mai mult decat zgomotul). 
    # pare ca 5 e bun la nivel de compromis din ambele directii (zgomot si informatie adevarata)

    # La al doilea cu Chebyshev, rp mare (5 sau 10) graficul se face mult mai smooth si pare ca pierde informatie 
    # un fel de combinatie de filtru low pass si high pass, dar noi nu cred ca vrem sa filtram in sensul de high pass
    # la 0.1 are niste puncte dubioase de low mai mici decat sunt pe graficul raw


if __name__=="__main__":
    main()