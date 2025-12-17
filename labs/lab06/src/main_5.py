import numpy as np
import matplotlib.pyplot as plt

def rectang_window(n):
    w=np.ones(n)
    return w


def hanning_window(n):
    w=np.zeros_like(n)
    for i in range (n):
        w=0.5*(1-np.cos(2*np.pi*i/n))

    return w


def main():
    t=np.linspace(0,1,200)
    sig=1*np.sin(2*np.pi*t*100+0)

    rect_w=rectang_window(200)
    hann_w=hanning_window(200)

    fin_sig=rect_w*sig
    fin_sig=fin_sig*hann_w

    plt.plot(t,fin_sig)
    plt.ylabel("Amplitudine")
    plt.xlabel("Timp")
    plt.savefig("../plots/5.pdf")
    plt.show()

if __name__=="__main__":
    main()