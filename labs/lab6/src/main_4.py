import numpy as np

def main():
    d=10
    t=np.linspace(0,1,20)
    x=2*np.sin(2*np.pi*t+np.pi/2)+2*np.sin(2*np.pi*t)
    y=np.concatenate((x[d:],x[:d]))
    # print(x2)
    X = np.fft.fft(x)
    Y = np.fft.fft(y)

    corr = np.fft.ifft(np.conj(X)*Y).real
    d_rec = np.argmax(corr)

    print("Deplasare recuperata cu inmultire:", d_rec)

    corr = np.fft.ifft(X/Y).real
    d_rec = np.argmax(corr)

    print("Deplasare recuperata cu impartire:", d_rec)


if __name__=="__main__":
    main()