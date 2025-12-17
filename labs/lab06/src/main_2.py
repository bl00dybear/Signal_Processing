import numpy as np
import matplotlib.pyplot as plt


def main():

    n=100
    t=np.linspace(0,100,n)
    sig=np.random.rand(n)

    fig, axs = plt.subplots(3, 1, figsize=(10, 10))

    for i in range (3):
        sig=np.convolve(sig,sig)
        t=np.linspace(0,100,len(sig))

        axs[i].plot(t,sig)
        axs[i].set_xlabel("Timp")
        axs[i].set_ylabel("Amplitudine")
        axs[i].grid()


    axs[0].set_title("Convolutii pe vector random")
    plt.savefig("../plots/2.1.pdf")
    plt.show()

    # Observatii: datele de aduna spre centru, si se fac mai smooth inspre margini, conform legii numerelor mari,
    # se aduna sub forma unei distributii normale

    A=2
    t=np.linspace(0,1,100)
    sig=A*(t>0.4)*(t<0.6)
    fig, axes = plt.subplots(4,1,figsize=(8, 20))

    axes[0].plot(t,sig)

    sig=np.convolve(sig,sig)
    t=np.linspace(0,1,len(sig))
    axes[1].plot(t,sig)

    sig=np.convolve(sig,sig)
    t=np.linspace(0,1,len(sig))    
    axes[2].plot(t,sig)

    sig=np.convolve(sig,sig)
    t=np.linspace(0,1,len(sig))
    axes[3].plot(t,sig)
    
    axes[0].set_title("Convolutii pe semnal rectangular")
    axes[-1].set_xlabel('Timp')
    fig.text(0.04, 0.5, 'Amplitudine',rotation='vertical')
    plt.savefig("../plots/2.2.pdf")
    plt.show()

    


if __name__=="__main__":
    main()