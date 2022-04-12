from directories import *
from back_process import *

if __name__ == '__main__':
    disco = 'F'
    initial_dir_data = str(disco) + ':/mnustes_science/experimental_data'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    X_mm = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
    T_s = np.loadtxt(directory + '/T_s.txt', delimiter=',')
    Z_mm = np.loadtxt(directory + '/Z_mm.txt', delimiter=',')

    #plt.imshow(Z_mm)
    #plt.show()
    index_cresta_x = np.argmax(Z_mm[0, :])

    sample_rate = 400
    Nt = int(len(Z_mm[:, index_cresta_x]))

    yf = fft(Z_mm[:, index_cresta_x])
    xf = fftfreq(Nt, 1 / sample_rate)
    #plt.plot(xf, np.abs(yf))
    #plt.show()

    index_freq = np.argmin(yf)
    period = 1 / 7.46

    T_aux01 = np.zeros(Nt)
    #correr eje del tiempo y hacer primer maximo en t=0
    for i in range(Nt):
        T_aux01[i] = T_s[i] // period

    Z_primer_ciclo = Z_mm[0:100, :]
    (i_max, j_max) = unravel_index(Z_primer_ciclo.argmax(), Z_primer_ciclo.shape)

    plt.plot(Z_primer_ciclo[:, j_max], c='k')
    plt.axvline(x=i_max, c='r')
    plt.show()
    plt.close()

    T_s__fromax = T_s[i_max:-1]
    Z_mm_fromax = Z_mm[i_max:-1, :]
    T_aux01_fromax = T_aux01[0:-i_max]

    T_stroboscopic = []
    Z_mm_stroboscopic = []
    for i in range(len(T_aux01_fromax) - 1):
        if T_aux01_fromax[i] != T_aux01_fromax[i + 1]:
            T_stroboscopic.append(T_s__fromax[i + 1])
            Z_mm_stroboscopic.append(Z_mm_fromax[i + 1, :])
    T_stroboscopic = np.array(T_stroboscopic)
    Z_mm_stroboscopic = np.array(Z_mm_stroboscopic)


    np.savetxt(directory + '/T_stroboscopic.txt', T_stroboscopic, delimiter=',')
    np.savetxt(directory + '/Z_mm_stroboscopic.txt', Z_mm_stroboscopic, delimiter=',')

    norm = TwoSlopeNorm(vmin=np.amin(Z_mm_stroboscopic), vcenter=0, vmax=np.amax(Z_mm_stroboscopic))
    pcm = plt.pcolormesh(X_mm, T_stroboscopic, Z_mm_stroboscopic, norm=norm, cmap='seismic', shading='auto')
    cbar = plt.colorbar(pcm, shrink=1)
    cbar.set_label('$\eta(x, t)$', rotation=0, size=20, labelpad=-27, y=1.1)
    plt.xlim([X_mm[0], X_mm[-1]])
    plt.xlabel('$x$', size='40')
    plt.ylabel('$t$', size='40')
    plt.grid(linestyle='--', alpha=0.5)
    plt.savefig(directory + '/stroboscopic.png', dpi=1000)
    plt.show()
