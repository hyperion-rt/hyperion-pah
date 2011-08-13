import glob
import os

import numpy as np

import matplotlib as mpl
mpl.use('Agg')

np.seterr(all='ignore')

from hyperion.dust import SimpleSphericalDust, prepare_emiss
from hyperion.util.integrate import interp1d_log10, integrate_loglog
from hyperion.util.constants import pi

# Read in Draine opacity file
d = SimpleSphericalDust('input/kmh_no200_rescale.par')
d.optical_properties._extrapolate(1.e-6,1.e5)
d.write('dust_files/kmh_no200.hdf5')
d.plot('dust_files/kmh_no200.png')

# Read in Draine opacity file
d = SimpleSphericalDust('input/draine_opac_new.dat')
d.optical_properties._extrapolate(1.e-6,1.e5)

# Create interpolating function for absorptive opacity
kappa_nu = interp1d_log10(d.optical_properties.nu, d.optical_properties.chi * (1. - d.optical_properties.albedo), bounds_error=False, fill_value=0.)

# Read in interstellar radiation field
isrf = np.loadtxt('input/mmp83.dat', dtype=[('wav', float), ('jlam', float)])
wav = isrf['wav'][::-1] # wavelength in microns
jlam = isrf['jlam'][::-1] # 4*pi*J in ergs/cm^2/s/micron
nu = 3.e14 / wav

# Create interpolating function for mean intensity
jnu = interp1d_log10(nu, jlam * wav / nu, bounds_error=False, fill_value=0.)

# Find common frequency scale
nu_common = np.unique(np.hstack([d.optical_properties.nu, nu]))
nu_common.sort()

# Find the energy density of the interstellar radiation field weighted by the absorptive opacity
u_isrf = integrate_loglog(nu_common, jnu(nu_common) * kappa_nu(nu_common))

print u_isrf

# Find the emissivity files
draine_emiss = glob.glob(os.path.join('input/','emit_draine*.dat'))
U = [u_isrf * float(os.path.basename(filename).replace('emit_draine_', '').replace('.dat', '')) for filename in draine_emiss]

print u_isrf

draine_emiss = np.array(draine_emiss)
U = np.array(U)
order = np.argsort(U)

prepare_emiss(draine_emiss[order], U[order], 'E', 'processed/emit_draine.hdf5')

d.emissivities.set_custom('processed/emit_draine.hdf5')
d.write('dust_files/draine.hdf5')
d.plot('dust_files/draine.png')
