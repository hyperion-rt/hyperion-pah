import numpy as np
np.seterr(all='ignore')

import atpy
from hyperion.dust import IsotropicSphericalDust

# Loop over grain sizes
for size in ['usg', 'vsg', 'big']:

    # Read in opacities
    t = atpy.Table('processed/opacities_%s.hdf5' % size)

    # Create isotropic dust type
    d = IsotropicSphericalDust(t['wav'], t['chi'], t['albedo'])

    # Set emissivities
    d.emissivities = 'processed/emissivities_%s.hdf5' % size

    # Write dust properties out to file
    d.write('dust_files/%s.hdf5' % size)

    # Make a plot of the main quantities
    d.plot('dust_files/%s.png' % size)
