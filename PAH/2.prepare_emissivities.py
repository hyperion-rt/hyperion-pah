import os
import glob
import atpy
import numpy as np

from hyperion.util.constants import c
from hyperion.util.interpolate import interp1d_fast_loglog
from hyperion.util.integrate import integrate_loglog

wav = None
U = []
jnu = {}
jnu['big'] = []
jnu['usg'] = []
jnu['vsg'] = []

for filename in glob.glob(os.path.join('input/emissivity/',
                                       'spec_MW3.1_60_U*_big.dat')):

    # Extract U value
    U.append(float(filename.split('_')[-2][1:]))

    for size in ['usg', 'vsg', 'big']:

        # Construct filename
        filename_size = filename.replace('big', size)

        # Extract emissivities
        emissivities = np.loadtxt(filename_size, usecols=[0, 2], skiprows=61,
                                  dtype=[('lambda', float), ('jnu', float)])

        # Check wavelength grid
        if wav is None:
            wav = emissivities['lambda']
            nu = c / (wav * 1.e-4)
        elif not np.all(emissivities['lambda'] == wav):
            raise Exception("Wavelength grids do not agree")

        # Append emissivity to lists
        jnu[size].append(emissivities['jnu'])

# Make array with U values
U = np.array(U)

# Find correct order for U values
order = np.argsort(U)

# Sort U values
U = U[order]

# Read in interstellar radiation field
isrf = np.loadtxt('input/mmp83.dat', dtype=[('wav', float), ('jlam', float)])
isrf_wav = isrf['wav'][::-1]  # wavelength in microns
isrf_jlam = isrf['jlam'][::-1]  # 4*pi*J in ergs/cm^2/s/micron
isrf_nu = c / (isrf_wav * 1.e-4)

# Find common frequency scale
nu_common = np.unique(np.hstack([nu, isrf_nu]))
nu_common.sort()

# Interpolate ISRF mean intensity to common frequency scale
isrf_jnu = interp1d_fast_loglog(isrf_nu, isrf_jlam * isrf_wav / isrf_nu,
                                nu_common, bounds_error=False, fill_value=0.)

u_isrf = {}

for size in ['usg', 'vsg', 'big']:

    # Read in opacity
    t = atpy.Table('processed/opacities_%s.hdf5' % size)

    # Sort by frequency
    t.sort('nu')

    # Interpolate absorptive opacity to common frequency scale
    kappa_nu = interp1d_fast_loglog(t['nu'], t['chi'] * (1. - t['albedo']),
                                    nu_common, bounds_error=False,
                                    fill_value=0.)

    # Find the energy density of the interstellar radiation field weighted by
    # the absorptive opacity
    u_isrf[size] = integrate_loglog(nu_common, isrf_jnu * kappa_nu)

# Produce final emissivity arrays
for size in ['big', 'vsg', 'usg']:

    # Cast emissivities to array and sort
    jnu_array = np.array(jnu[size]).transpose()[:, order]

    # Create a table set
    ts = atpy.TableSet()

    # Create a table with frequency and emissivity
    t = atpy.Table(name='Emissivities')
    t.add_column('nu', c * 1.e4 / wav)
    t.add_column('jnu', jnu_array)
    t.sort('nu')
    ts.append(t)

    # Create a table with the independent variable
    t = atpy.Table(name='Emissivity variable')
    t.add_column('specific_energy_abs', U * u_isrf[size])
    ts.append(t)

    # Write out to HDF5 file
    ts.write('processed/emissivities_%s.hdf5' % size, overwrite=True)
