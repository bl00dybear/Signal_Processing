import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from scipy.io import wavfile

def _1():
    t = np.linspace(0,1,200)
    A_sin = np.sin(2*np.pi*2*t)
    A_cos = np.cos(2*np.pi*2*t-np.pi/2)
    
    fig, (ax1, ax2) = plt.subplots(2, 1)

    ax1.plot(t, A_sin)
    ax1.set_title('Semnal sinus')
    ax1.set_ylabel('Amplitudine')
    ax1.grid(True)
    ax1.legend(loc='upper right')

    ax2.plot(t, A_cos, color='orange')
    ax2.set_title('Semnal cosinus')
    ax2.set_xlabel('Timp [s]')
    ax2.set_ylabel('Amplitudine')
    ax2.grid(True)
    ax2.legend(loc='upper right')

    fig.tight_layout()
    plt.savefig("../plots/1.pdf")
    plt.show()


def _2():
    t = np.linspace(0,1,200)
    A_1 = np.sin(2*np.pi*2*t)
    A_2 = np.sin(2*np.pi*2*t + np.pi/2)
    A_3 = np.sin(2*np.pi*2*t + np.pi)
    A_4 = np.sin(2*np.pi*2*t + 3*np.pi/2)
    
    plt.plot(t,A_1)
    plt.plot(t,A_2)
    plt.plot(t,A_3)
    plt.plot(t,A_4)
    plt.xlabel("Timp")
    plt.ylabel("Amplitudine")
    plt.grid(True)
    plt.savefig("../plots/2.1.pdf")
    plt.show()
    plt.close()
        
    SNR = 0.1
    z = np.random.normal(loc=0.0,scale=1.0,size=t.shape)
    
    sigma1 = np.sqrt(np.mean(A_1 ** 2) / (SNR*np.mean(z**2)))
    sigma2 = np.sqrt(np.mean(A_1 ** 2) / (1*np.mean(z**2)))
    sigma3 = np.sqrt(np.mean(A_1 ** 2) / (10*np.mean(z**2)))
    sigma4 = np.sqrt(np.mean(A_1 ** 2) / (100*np.mean(z**2)))
    
    
    
    A_zgomot1 = A_1 + sigma1*z   
    A_zgomot2 = A_1 + sigma2*z  
    A_zgomot3 = A_1 + sigma3*z  
    A_zgomot4 = A_1 + sigma4*z  

    fig2 , axis2 = plt.subplots(4,1)

    
    signals = [A_zgomot1,A_zgomot2,A_zgomot3,A_zgomot4]

    for ax, y in zip(axis2, signals):
        ax.plot(t, y)
        ax.set_ylabel('Amplitudine')
        ax.grid(True)

    axis2[-1].set_xlabel('Timp [s]')
    plt.savefig("../plots/2.2.pdf")
    plt.show()
    plt.close(fig2)


def _3():
    fs=14100
    
    t=np.linspace(0,10,16000)
    s_2a=np.sin(2*np.pi*400*t)
    sd.play(s_2a,fs)
    sd.wait()
    
    
    t=np.linspace(0,10,16000)
    s_2b=np.sin(2*np.pi*3*t)
    sd.play(s_2b,fs)
    sd.wait()
    
    t = np.linspace(0,10,16000)
    s_2c = t*240-np.floor(t*240)
    sd.play(s_2c,fs)
    sd.wait()
    
    t = np.linspace(0,10,16000)
    s_2d = np.sign(np.sin(2*np.pi*t))
    sd.play(s_2d,fs)
    sd.wait()
    
    wavfile.write("../plots/3.wav",fs,s_2c)
    
    _,s_2c_loaded = wavfile.read("../plots/3.wav")
    
    sd.play(s_2c_loaded,fs)
    sd.wait()


def _4():
    t = np.linspace(0,1,400)
    sin_signal = np.sin(2*np.pi*t)
    sawtooth_signal = t - np.floor(t)
    sum_signal = sin_signal+sawtooth_signal
    
    fig , axis = plt.subplots(3,1)

    
    signals = [sin_signal,sawtooth_signal,sum_signal]

    for ax, y in zip(axis, signals):
        ax.plot(t, y)
        ax.set_ylabel('Amplitudine')
        ax.grid(True)

    axis[-1].set_xlabel('Timp [s]')
    plt.savefig("../plots/4.pdf")
    plt.show()
    plt.close(fig)


def _5():
    fs=14100
    
    t = np.linspace(0,10,16000)
    sig1 = np.sin(2*np.pi*400*t)
    sig2 = np.sin(2*np.pi*500*t)
    sum_sig=np.concatenate([sig1,sig2])
    
    sd.play(sum_sig,fs)
    sd.wait()
    
    # observatie: cu cat creste mai mult frecventa cu atat
    # sunetul e mai inalt, mai intepator la auz
    
    
def _6():
    fs = 44100
    
    f1=fs/2
    f2=fs/4
    f3=0
    
    t1 = np.linspace(0,0.01,4410)
    t2 = np.linspace(0,0.01,2205)
    t3 = np.linspace(0,1,2)
    
    sig1 = np.sin(2*np.pi*f1*t1)
    sig2 = np.sin(2*np.pi*f2*t2)
    sig3 = np.sin(2*np.pi*f3*t3)
            
    fig,axis=plt.subplots(3,1)
    
    signals = [sig1,sig2,sig3]
    ts = [t1,t2,t3]
    
    for ax,t,A in zip(axis,ts,signals):
        ax.plot(t,A)
        ax.set_ylabel('Amplitudine')
        ax.grid(True)
        
    axis[-1].set_xlabel('Timp [s]')
    plt.savefig("../plots/6.pdf")
    plt.show()
    plt.close(fig)
    
    # obersvatie: stim ca frecventa reprezinta cate perioade ale semnalului avem intr o secunda
    # (o secunda pt ca asa am scris formula, cf. cursului)
    # deci practic o frecventa mai mare inseamna un semnal mai des si mai ascutit.
    # frecventa 0 inseamna ca e semnal nul, adica sunt 0 perioade ale semnalului in 1s
    
    
def _7():
    t = np.linspace(0,1,1000)
    sig1 = np.sin(2*np.pi*16*t)
    sig2 = np.sin(2*np.pi*4*t)

    tt=np.linspace(0,1,250)
    
    decimated_s1 = sig1[3::4]
    decimated_s2 = sig2[3::4]
    
    double_decimated_s1 = decimated_s1[1::4]
    double_decimated_s2 = decimated_s2[1::4] 
    ttt = np.linspace(0,1,len(double_decimated_s1))
    
    sigs=[decimated_s1,decimated_s2]
    fig,axis = plt.subplots(2,1)
    
    for ax,A in zip(axis,sigs):
        ax.plot(tt,A)
        ax.set_ylabel('Amplitudine')
        ax.grid(True)
        
    axis[-1].set_xlabel('Timp [s]')
    plt.savefig("../plots/7.1.pdf")
    plt.show()
    plt.close(fig)
    
    sigs=[double_decimated_s1,double_decimated_s2]
    fig,axis = plt.subplots(2,1)
    
    for ax,A in zip(axis,sigs):
        ax.plot(ttt,A)
        ax.set_ylabel('Amplitudine')
        ax.grid(True)
        
    axis[-1].set_xlabel('Timp [s]')
    plt.savefig("../plots/7.2.pdf")
    plt.show()
    plt.close(fig)
    
    # (a): la nivel de observatii pot mentiona doar ca primul semnal este mai patratos
    # (b): dupa a doua decimare a celor 2 semnale, primul nu prea mai arata a sinusoida, pe cand al doilea inca 
    # are o oarecare forma de sinusoida

def main():
    _7()




if __name__ == "__main__":
    main()