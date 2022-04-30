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
    zero_fix = 'no'
    Nx = len(X_mm)
    Nt = len(T_s)

    fps = 400
    forcing_freq = 14.9

    period_fps = int(fps * (2 / forcing_freq))
    print(period_fps)
    period_error_range = 8

    T_big_initial = 100
    big_initial_window = Z_mm[0:T_big_initial, :]
    i_max, j_max = np.unravel_index(big_initial_window.argmax(), big_initial_window.shape)

    initial_window_size = 20   # Numero PAR
    Z_strobo = []
    T_strobo = []
    while i_max <  Nt - period_fps:
        window = Z_mm[int(i_max - period_error_range / 2):int(i_max + period_error_range / 2), int(j_max - initial_window_size / 2):int(j_max + initial_window_size / 2)]
        i_max_new, j_max_new = np.unravel_index(window.argmax(), window.shape)
        i_max_Z = i_max + period_fps - period_error_range / 2 + i_max_new
        j_max_Z = j_max - initial_window_size / 2 + j_max_new
        Z_strobo.append(Z_mm[int(i_max_Z), :])
        T_strobo.append(T_s[int(i_max_Z)])
        Z_strobo_np = np.array(Z_strobo)
        T_strobo_np = np.array(T_strobo)
        i_max = i_max_Z
        j_max = j_max_Z

    Z_strobo_np = filtro_superficie(Z_strobo_np, 2, 'Y')
    #Z_strobo_np = filtro_superficie(Z_strobo_np, 4, 'X')

    if zero_fix == 'yes':
        Z_strobo_np[Z_strobo_np < 0] = 0
    np.savetxt(directory + '/T_stroboscopic.txt', T_strobo_np, delimiter=',')
    np.savetxt(directory + '/Z_mm_stroboscopic.txt', Z_strobo_np, delimiter=',')

    norm = TwoSlopeNorm(vmin=np.amin(Z_strobo_np), vcenter=0, vmax=np.amax(Z_strobo_np))
    pcm = plt.pcolormesh(X_mm, np.arange(len(Z_strobo_np[:, 0])), Z_strobo_np, norm = norm, cmap='seismic', shading='auto')
    cbar = plt.colorbar(pcm, shrink=1)
    cbar.set_label('$\eta(x, t)$', rotation=0, size=20, labelpad=-27, y=1.1)
    plt.xlim([X_mm[0], X_mm[-1]])
    plt.xlabel('$x$', size='20')
    plt.ylabel('$t$', size='20')
    plt.grid(linestyle='--', alpha=0.5)
    plt.savefig(directory + '/stroboscopic.png', dpi=300)
    plt.close()
