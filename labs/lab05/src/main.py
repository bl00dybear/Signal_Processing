import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def main():
    df = pd.read_csv("Train.csv")
    
    print(df.shape)
    
    x=np.array(df['Count'])
    
    df['Datetime'] = pd.to_datetime(df['Datetime'],dayfirst=True)

# a b c
    print("Interval de esantionare: ", df['Datetime'][1]-df['Datetime'][0])
    print("Interval de acoperire: ", df['Datetime'].iloc[-1]-df['Datetime'][0] )
    
    fs = 1.0 / (df['Datetime'][1]-df['Datetime'][0]).total_seconds()
    print("Frecventa de esantionare: ",fs)
    print("Frecventa maxima prezenta ", fs/2)
    
# d
    X = np.fft.fft(x)
    
    t=np.arange(0,len(X)//2)
    
    plt.plot(t,np.abs(X[:len(X)//2]))
    plt.yscale('log')
    plt.xlabel('Indice bin (k)')
    plt.ylabel('magnitudine, log')
    plt.savefig("../plots/1.pdf")
    plt.show()
    
    x0 = [1]*len(x)

    print(X[0])

# e
    if np.abs(X[0]) > 1e-8:
        for i in range (len(x)):
            x0[i] = x[i] - X[0].real/len(x)
        X0 = np.fft.fft(x0)
        print(X0[0])
        plt.figure()
        plt.plot(np.abs(X0[1:len(X0)//2]))
        plt.yscale("log")
        plt.xlabel('Indice bin (k)')
        plt.ylabel('magnitudine, log')
        plt.savefig("../plots/2.pdf")
        plt.show()
        X=X0
        X[0]=0
        x=x0

# f
    A=np.abs(X)
    n=len(A)
    sorted_indexes=np.argsort(A[:n//2])
    for i in range (len(sorted_indexes)-1,len(sorted_indexes)-5,-1):
        bin_num=sorted_indexes[i]
        freq=bin_num * (1/(3600*n))
        amplit=A[bin_num]
        perioada_h = 1/(freq*3600)
        perioada_d = perioada_h/24
        print(f"{freq:.8f} Hz  {amplit:.2f}  {perioada_h:.2f} h  {perioada_d:.2f} d")

# g

    # 6 ian 2013 - prima zi de luni din 2013
    # 1000 de esantioane reprezinta 41 de zile si 16 ore, iar data de start la esantionare e 25 08 2012

    target_s=pd.Timestamp('2013-01-06 00:00:00')
    target_e=pd.Timestamp('2013-02-05 00:00:00')
    idx_s = int((target_s - df['Datetime'].iloc[0]).total_seconds() / 3600)
    idx_e = int((target_e - df['Datetime'].iloc[0]).total_seconds() / 3600)
    xm=x[idx_s:idx_e]
    ts = df['Datetime'].iloc[idx_s:idx_e]
    plt.plot(ts, xm)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.xlabel('Data')
    plt.ylabel('Count')
    plt.savefig("../plots/3.pdf")
    plt.show()

# h
    # Noi ca sa determinam data de start a esantionarii trebuie sa mapam cumva semnalul in timp.
    # Analizand semnalul nu e suficient, asa ca am mai putea observa fizic fenomenul si asa identificam 
    # cam pe unde se situeaza clipa prezentului in perioadele principale.
    # Astfel maparea se face din prezent in trecut si se poate determina data de start
    # Acest rationament este vulnerabil la anomalii (o anomalie ar fi ca azi ploua si lumea circula mai mult cu bullet train-ul)
    # Pentru a diminua potentialul existentei aceste erori, am putea efectua masuratori zilnice (pana ajungem la o eroare rezonabila)

# i
    # Alegerea am facut o folosindu ma de f) pentru a afisa mai mult de 4
    # conceptual la primele 5 le gasesc un sens uman (ani,luni,anotimpuri,zile,saptamani)
    # 0.00000002 Hz  1222623.35  18288.00 h  762.00 d
    # 0.00000003 Hz  644088.24  9144.00 h  381.00 d
    # 0.00001157 Hz  495641.78  24.00 h  1.00 d
    # 0.00000005 Hz  461221.83  6096.00 h  254.00 d
    # 0.00000166 Hz  347480.62  167.78 h  6.99 d
    # 0.00000006 Hz  324107.01  4572.00 h  190.50 d
    # 0.00001159 Hz  255190.29  23.97 h  1.00 d
    # 0.00000008 Hz  251377.97  3657.60 h  152.40 d
    # 0.00000011 Hz  228036.34  2612.57 h  108.86 d
    A=np.abs(X)
    n=len(A)
    sorted_indexes=np.argsort(A[:n//2])
    principal_indexes=sorted_indexes[len(sorted_indexes)-6:len(sorted_indexes)-1]
    for i in range(len(sorted_indexes)):
        k = sorted_indexes[i]
        if k != 0 and k not in principal_indexes:
            X[k] = 0
            X[-k] = 0

    x_rec = np.fft.ifft(X).real

    plt.figure()
    plt.plot(df['Datetime'], x_rec)
    plt.tight_layout()
    plt.xlabel('Data')
    plt.ylabel('Count')
    plt.savefig("../plots/4.pdf")
    plt.show()
    


if __name__=="__main__":
    main()