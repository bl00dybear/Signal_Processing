import numpy as np
import matplotlib.pyplot as plt


def main():
    N = 64
    n1 = np.arange(N)
    n2 = np.arange(N)
    n1, n2 = np.meshgrid(n1, n2)

    data_list = []

    #(a)
    x1 = np.sin(2*np.pi*n1+3*np.pi*n2)
    Y1 = np.fft.fftshift(np.fft.fft2(x1))
    data_list.append((x1, np.abs(Y1), r'$x = \sin(2\pi n_1 + 3\pi n_2)$'))

    #(b)
    x2 = np.sin(4*np.pi*n1)+np.cos(6*np.pi*n2)
    Y2 = np.fft.fftshift(np.fft.fft2(x2))
    data_list.append((x2, np.abs(Y2), r'$x = \sin(4\pi n_1) + \cos(6\pi n_2)$'))

    # (c)
    Y3 = np.zeros((N, N), dtype=complex)
    Y3[0, 5] = 1
    Y3[0, N-5] = 1
    x3 = np.fft.ifft2(Y3)
    data_list.append((np.real(x3), np.abs(Y3), r'$Y_{0,5}=1, Y_{0,N-5}=1$'))

    #(d)
    Y4 = np.zeros((N, N), dtype=complex)
    Y4[5, 0] = 1
    Y4[N-5, 0] = 1
    x4 = np.fft.ifft2(Y4)
    data_list.append((np.real(x4), np.abs(Y4), r'$Y_{5,0}=1, Y_{N-5,0}=1$'))

    #(e)
    Y5 = np.zeros((N, N), dtype=complex)
    Y5[5, 5] = 1
    Y5[N-5, N-5] = 1
    x5 = np.fft.ifft2(Y5)
    data_list.append((np.real(x5), np.abs(Y5), r'$Y_{5,5}=1, Y_{N-5,N-5}=1$'))

    fig, axes = plt.subplots(5, 2, figsize=(10, 20))

    for i, (img, spectrum, title) in enumerate(data_list):
        ax_img = axes[i, 0]
        ax_spec = axes[i, 1]

        im1 = ax_img.imshow(img, cmap=plt.cm.gray)
        ax_img.set_title(f'Imagine: {title}')
        plt.colorbar(im1, ax=ax_img)

        im2 = ax_spec.imshow(20*np.log10(abs(spectrum+1e-13)),cmap=plt.cm.gray)
        ax_spec.set_title('Spectru Amplitudine')
        plt.colorbar(im2, ax=ax_spec)

    plt.tight_layout()
    plt.savefig("../plots/1.pdf")
    plt.show()



if __name__=="__main__":
    main()

    # Observatii:
    
# 1. Daca ne uitam pe bara din dreapta, scala de valori este foarte mica, si matematic vorbind ar fi trebuit sa fie o imagine doar cu 0 uri, pt ca $sin(n*pi)$ 
#     e zero mereu, nu n intreg, deci practic noi acolo avem doar zgomot rezultat din erorile de calcul.

# 2. Facand si aici calculul matematic, $sin(4*pi*n1)=0$ si $cos(6*pi*n2)=1$(din faptu ca avem multipli intregi de perioada). Erorile variaza pe axa orizontala 
#     (n1), dar constante pe verticala. In ceea ce priveste spectrul, punctul alb central este media semnalului (tot 1, pt ca si semnalu e "constant"). Apoi mai 
#     observam si linia aceea orizontala, care din ce am inteles eu este un fel de spectru al erorilor din prima imagine, erorile pe verticala, dupa Fourier se 
#     transpun in orizontal si sunt vizibile din cauza ca afisez cu scara logaritmica.

# 3. Aici am setat manual Y(0,5)=1. Indicele 0 pe randuri inseamna frecventa nula pe verticala (semnalu e constant sus-jos), iar indicele 5 pe coloane inseamna 
#     variatie pe orizontala, de unde rezulta dungile verticale. In spectru, punctele albe sunt pe marginea de sus (randul 0) confirmand lipsa frecventei verticale,
#     iar pozitia la indexul 5 ne arata fix de ce avem 5 benzi pe latimea imaginii. Noi punem si Y(0,N-5)=1, pentru ca vrem sa avem simetria pe care o cere Fourier, 
#     mai ales ca plecam de la spectru si vrem sa ajungem la o imagine sinusoida frumoasa, nu cu numere complexe.

# 4. Fenomenul anterior doar ca transpus.

# 5. Avem Y(5,5)=1. Asta inseamna ca avem variatie simultana: si pe verticala (index 5 la randuri) si pe orizontala (index 5 la coloane). Combinand cele doua miscari,
#     ne rezulta liniile diagonale. In spectru, punctul alb e la intersectia randului 5 cu coloana 5, iar celalalt de la (N-5, N-5) e perechea lui pentru simetrie, ca 
#     sa iasa imaginea reala.