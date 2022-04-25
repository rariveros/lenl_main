from back_process import *

if __name__ == '__main__':
    ### Definiendo parametros y eligiendo carpeta a detectar ###
    disco = 'E'
    file = disco +':/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed'
    gammas = genfromtxt(file + '/gammas.csv', delimiter=',')
    velocities = genfromtxt(file + '/velocities.csv', delimiter=',')
    velocities_error = genfromtxt(file + '/velocities_err.csv', delimiter=',')
    cut = 14
    gammas_log = np.log(gammas[cut:-1] - 0.691 * np.ones(len(gammas[cut:-1])))
    #print(gammas[cut])
    velocities_log = np.log(velocities[cut:-1])
    velocities_error_log = velocities_error[cut:-1] / velocities[cut:-1]

    ### Ajuste de curva ###
    def linear_fit(x, m, n):
        return m * x + n
    popt, pcov = curve_fit(linear_fit, gammas_log, velocities_log)
    m = popt[0]
    n = popt[1]
    x_grid = np.arange(gammas_log[0] - np.abs(gammas_log[0] - gammas_log[1]), gammas_log[-1] + np.abs(gammas_log[0] - gammas_log[1]), 0.01)
    velocities_log_fit = m * x_grid + n

    ### Figuras y Gráficas ###
    fig, ax = plt.subplots()
    textstr = '\n'.join((r'$m=%.3f$' % (m,), r'$n=%.3f$' % (n,)))
    plt.errorbar(gammas_log, velocities_log, yerr=velocities_error_log, marker='o', ls='', capsize=5, capthick=1, ecolor='k', color='k')
    plt.plot(x_grid, velocities_log_fit, '-', linewidth='2', c='r', label='No noise')
    plt.xlabel('$\ln(\Gamma_0 - \Gamma_c$)', size=15)
    plt.ylabel('$\ln(\langle v \\rangle$)', size=15)
    #plt.legend(loc='best', fancybox=True, shadow=True)
    plt.grid(True)
    plt.title('$ln-ln$', fontsize=20)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
    plt.xlim([x_grid[0], x_grid[-1]])
    plt.ylim([velocities_log_fit[0], velocities_log_fit[-1]])
    plt.savefig(file + '/ln-ln.png', dpi=300)
    plt.show()
    plt.close()