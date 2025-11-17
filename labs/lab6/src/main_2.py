import numpy as np
import matplotlib.pyplot as plt

def convo(h,x,n):
    conv=[0]*n
    for i in range(n):
        for k in range(n):
            conv[i]+=h[k]*x[i-k]

    return conv

def main():
    n=100
    t=np.linspace(0,100,100)
    x=np.random.rand(n)

    fig, axes = plt.subplots(4,1,figsize=(8, 20))
    axes[0].plot(t,x)
    x=convo(x,x,n)
    axes[1].plot(t,x)
    x=convo(x,x,n)
    axes[2].plot(t,x)
    x=convo(x,x,n)
    axes[3].plot(t,x)
    axes[0].set_title("Convolutii pe vector random")
    plt.savefig("../plots/2.1.pdf")
    plt.show()

    # Observatii: convolutiile au efect de dispersie a "semnalului" si devine mai smooth

    A=2
    t=np.linspace(0,1,100)
    sig=A*(t>0.01)*(t<0.1)
    fig, axes = plt.subplots(4,1,figsize=(8, 20))
    axes[0].plot(t,sig)
    sig=convo(sig,sig,n)
    axes[1].plot(t,sig)
    sig=convo(sig,sig,n)
    axes[2].plot(t,sig)
    sig=convo(sig,sig,n)
    axes[3].plot(t,sig)
    axes[0].set_title("Convolutii pe semnal rectangular")
    axes[-1].set_xlabel('Timp')
    fig.text(0.04, 0.5, 'Amplitudine',rotation='vertical')
    plt.savefig("../plots/2.2.pdf")
    plt.show()

    


if __name__=="__main__":
    main()