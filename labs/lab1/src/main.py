import numpy as np
import matplotlib.pyplot as plt


# 1
# X=np.linspace(0,0.03,int(0.03/0.0005))
# x_t=np.cos(520*np.pi*X+np.pi/3)
# y_t=np.cos(280*np.pi*X-np.pi/3)
# z_t=np.cos(120*np.pi*X+np.pi/3)

# plt.figure(figsize=(10, 8))

# plt.subplot(3, 1, 1)
# plt.plot(X, x_t)
# plt.title('x_t')
# plt.xlabel('Timp (s)')
# plt.ylabel('Amplitudine')

# plt.subplot(3, 1, 2)
# plt.plot(X, y_t)
# plt.title('y_t')
# plt.xlabel('Timp (s)')
# plt.ylabel('Amplitudine')

# plt.subplot(3, 1, 3)
# plt.plot(X, z_t)
# plt.title('z_t')
# plt.xlabel('Timp (s)')
# plt.ylabel('Amplitudine')

# plt.tight_layout()
# plt.savefig('lab1/plots/1.pdf')
# plt.show()

# b

#2
#a
# X=np.linspace(0,0.1,160)
# Y_a=np.sin(2*np.pi*400*X)

# plt.stem(X,Y_a)
# plt.savefig('lab1/plots/2_a.pdf')
# plt.show()

#b
t=np.linspace(0,3,300)
Y_b=np.sin(2*np.pi*3*t)
plt.plot(t,Y_b)
plt.xlabel('Timp (s)')
plt.ylabel('Amplitudine')
plt.savefig('lab1/plots/2_b.pdf')
plt.show()