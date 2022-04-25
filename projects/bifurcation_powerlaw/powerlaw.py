from back_process import *

if __name__ == '__main__':
    disc = 'E'
    gammas_np = genfromtxt(disc + ':/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/gammas.csv', delimiter=',')
    velocities_np = genfromtxt(disc + ':/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/velocities.csv', delimiter=',')
    velocities_error_np = genfromtxt(disc + ':/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/velocities_err.csv', delimiter=',')


    popt, pcov = curve_fit(fit_criticalpower_02, gammas_np, velocities_np, bounds=[(0, 0.6, 0), (10, 0.7, 10)])
    A = popt[0]
    c = popt[1]
    noise = popt[2]
    print(noise)

    x_grid = np.arange(0, 1, 0.001)
    velocity_noisy_fitted = []
    for i in range(len(x_grid)):
        epsilon_i = x_grid[i] - c
        velocity_noisy_fitted_i = A * ((epsilon_i + (epsilon_i ** 2 + 2 * noise) ** 0.5) / 2) ** 0.5
        velocity_noisy_fitted.append(velocity_noisy_fitted_i)
    velocity_noisy_fitted_np = np.array(velocity_noisy_fitted)

    x_grid_antierror = np.arange(c, 1, 0.001)
    velocity_fitted = []
    for i in range(len(x_grid_antierror)):
        epsilon_i = x_grid_antierror[i] - c
        velocity_fitted_i = A * (epsilon_i) ** 0.5
        velocity_fitted.append(velocity_fitted_i)
    velocity_fitted_np = np.array(velocity_fitted)

    fig, ax = plt.subplots()
    textstr = '\n'.join((
        r'$A=%.3f$' % (A,),
        r'$\mathrm{\Gamma_c}=%.3f$' % (c,),
        r'$\mathrm{\eta}=%.4f$' % (noise,)))

    plt.xlabel('$\Gamma_0$', size=15)
    plt.ylabel('$\langle v \\rangle$ (mm/s)', size=15)
    plt.errorbar(gammas_np, velocities_np, yerr=velocities_error_np, marker='o', ls='', capsize=5, capthick=1,
                 ecolor='k', color='k')
    plt.plot(x_grid_antierror, velocity_fitted_np, '--', linewidth='2', c='r', label='Noise included')
    plt.plot(x_grid, velocity_noisy_fitted_np, '-', linewidth='2', c='r', label='No noise')
    plt.ylim([0, 1])
    plt.xlim([0.61, 0.79])
    plt.legend(loc='best', fancybox=True, shadow=True)
    plt.grid(True)
    plt.title('$<v> = A \sqrt{(\Gamma_0^2 - \Gamma_c^2)}$')
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    # place a text box in upper left in axes coords
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
    plt.savefig(disc + ':/mnustes_science/experimental_data/faraday_drift_03/dvelocities_info/velocity_processed/fit_01')
    plt.show()
    plt.close()