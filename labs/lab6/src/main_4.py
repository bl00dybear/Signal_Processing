import numpy as np

def main():
    d=10
    t=np.linspace(0,1,20)
    x=2*np.sin(2*np.pi*t+np.pi/2)+2*np.sin(2*np.pi*t)
    y=np.concatenate((x[d:],x[:d]))
    # print(x2)
    X = np.fft.fft(x)
    Y = np.fft.fft(y)

    corr = np.fft.ifft(Y * np.conj(X)).real
    d_rec = np.argmax(corr)

    print("deplasare reala:", d)
    print("deplasare recuperata:", d_rec)
    print("vector corelatie:", corr)


if __name__=="__main__":
    main()