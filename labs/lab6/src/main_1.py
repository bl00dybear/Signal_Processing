import numpy as np
import matplotlib.pyplot as plt


def main():
    B=2
    t_cont = np.linspace(-3, 3, 5000)
    x_cont = np.sinc(B*t_cont)**2
    Fss = [1,1.5,2,20]

    fig, axes = plt.subplots(4,1,figsize=(8, 20))

    i=0
    for Fs in Fss:
        Ts =1/Fs
        tn = np.arange(-3,3,Ts)
        x_stem = np.sinc(tn)**2
        
        x_hat = np.zeros_like(t_cont) 

        ii=0
        for t in t_cont:
            sinc_terms = np.sinc((t-tn)/Ts)
            x_hat[ii] = np.sum(x_stem*sinc_terms)
            ii+=1
        
        axes[i].set_title(f"Frecv {Fs} Hz")
        axes[i].plot(t_cont, x_cont)
        axes[i].stem(tn, x_stem, linefmt='--r', markerfmt='ro',basefmt=" ")
        axes[i].plot(t_cont, x_hat, 'b--', linewidth=2)
        i+=1

    axes[-1].set_xlabel('Timp')
    fig.text(0.04, 0.5, 'Amplitudine',rotation='vertical')
    plt.savefig("../plots/1.1.pdf")
    plt.show()

# ?? nu mai functioneaza pentru B >1 dar presupun ca e greseala de implementare

if __name__=="__main__":
    main()