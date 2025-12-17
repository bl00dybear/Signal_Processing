import numpy as np

def main():
    n=20
    p=np.random.randint(0,100,n)
    q=np.random.randint(0,100,n)

    # p=[1,2]
    # q=[2,1]

    len=2*n-1
    pfft=np.fft.fft(p,len)
    qfft=np.fft.fft(q,len)
    res_fft=pfft*qfft
    res=np.fft.ifft(res_fft,len)

    print(p,q)

    print(res.real)


if __name__=="__main__":
    main()