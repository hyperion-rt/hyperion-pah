import numpy as np
np.seterr(all='ignore')

import matplotlib
matplotlib.use('Agg')

import atpy
from hyperion.dust import IsotropicSphericalDust

# Loop over grain sizes
for size in ['usg', 'vsg', 'big']:

    # Read in opacities
    t = atpy.Table('processed/opacities_%s.hdf5' % size)

    # Create isotropic dust type
    d = IsotropicSphericalDust(t['wav'], t['chi'], t['albedo'])
    d.optical_properties._extrapolate(1.e-3,1.e5)
    d.optical_properties._sort()

    # Set emissivities
    d.emissivities.set_custom('processed/emissivities_%s.hdf5' % size)

    # Write dust properties out to file
    d.write('dust_files/%s.hdf5' % size)

    # Make a plot of the main quantities
    d.plot('dust_files/%s.png' % size)
