from directories import *
from back_process import *

#Técnica basada en promedio de dinámica estroboscópica para patrones estacionarios.

if __name__ == '__main__':
    disco = 'F'
    initial_dir_data = str(disco) + ':/mnustes_science/experimental_data'
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(parent=root, initialdir=initial_dir_data, title='Elección de carpeta')

    X_mm = np.loadtxt(directory + '/X_mm.txt', delimiter=',')
    T_s = np.loadtxt(directory + '/T_s.txt', delimiter=',')
    Z_mm_stroboscopic = np.loadtxt(directory + '/Z_mm_stroboscopic.txt', delimiter=',')

    Nx = len(X_mm)
    proyeccion = np.zeros(Nx)
    for i in range(Nx):
        proyeccion[i] = np.mean(Z_mm_stroboscopic[:, i])

    analytical_signal = hilbert(proyeccion)
    amplitude_envelope = np.abs(analytical_signal)


    plt.show()

    def func(x, a, b, d):
        return a * np.exp(-b * (x - d) ** 2)

    popt, pcov = curve_fit(func, X_mm, amplitude_envelope,bounds=([0, 0, 0], [20, 20, 200]))

    np.savetxt(directory + '/proyeccion.txt', proyeccion, delimiter=',')
    np.savetxt(directory + '/hilbert_envelope.txt', amplitude_envelope, delimiter=',')
    plt.plot(X_mm, proyeccion)
    plt.plot(X_mm, amplitude_envelope)
    plt.plot(X_mm, func(X_mm, *popt), 'r--')
    plt.xlim(X_mm[0], X_mm[-1])
    plt.grid(linestyle='--', alpha=0.5)
    plt.xlabel('$x$', size='40')
    plt.ylabel('$Re(\psi)$', size='40')
    plt.savefig(directory + '/proyeccion.png', dpi=1000)
    plt.show()
    plt.close()
