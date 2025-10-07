import numpy as np
import matplotlib.pyplot as plt


# 1

def _1_a():
    X=np.linspace(0,0.03,int(0.03/0.0005))
    x_t=np.cos(520*np.pi*X+np.pi/3)
    y_t=np.cos(280*np.pi*X-np.pi/3)
    z_t=np.cos(120*np.pi*X+np.pi/3)

    plt.figure(figsize=(10, 8))

    plt.subplot(3, 1, 1)
    plt.plot(X, x_t)
    plt.title('x_t')
    plt.xlabel('Timp (s)')
    plt.ylabel('Amplitudine')

    plt.subplot(3, 1, 2)
    plt.plot(X, y_t)
    plt.title('y_t')
    plt.xlabel('Timp (s)')
    plt.ylabel('Amplitudine')

    plt.subplot(3, 1, 3)
    plt.plot(X, z_t)
    plt.title('z_t')
    plt.xlabel('Timp (s)')
    plt.ylabel('Amplitudine')

    plt.tight_layout()
    plt.savefig('../plots/1.pdf')
    plt.show()


def _2_a():
    X=np.linspace(0,0.1,160)
    Y_a=np.sin(2*np.pi*400*X)

    plt.stem(X,Y_a)
    plt.savefig('../plots/2_a.pdf')
    plt.show()

def _2_b():
    t=np.linspace(0,3,300)
    Y_b=np.sin(2*np.pi*3*t)
    plt.plot(t,Y_b)
    plt.xlabel('Timp (s)')
    plt.ylabel('Amplitudine')
    plt.savefig('../plots/2_b.pdf')
    plt.show()
    
    
def _2_c():
    t = np.linspace(0,1,240)
    A = t*240-np.floor(t*240)
    
    plt.plot(t,A)
    plt.xlabel('Timp (s)')
    plt.ylabel('Amplitudine')
    plt.savefig('../plots/2_c.pdf')
    plt.show()


def main():
    _2_c()

if __name__ == "__main__":
    main()