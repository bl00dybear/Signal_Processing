import pandas as pd
import numpy as np

def main():
    df = pd.read_csv("Train.csv")    
    x=np.array(df['Count'])
    x=x[:3*24]
    print(x)

    w=5
    x=np.convolve(x,np.ones(w), 'valid')/w
    print(x)

if __name__=="__main__":
    main()