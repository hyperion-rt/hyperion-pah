import os
import glob
import atpy
import numpy as np

from hyperion.util.constants import c

wav = None
U = []
jnu = {}
jnu['big'] = []
jnu['usg'] = []
jnu['vsg'] = []

for filename in glob.glob(os.path.join('input/emissivity/', 'spec_MW3.1_60_U*_big.dat')):

    # Extract U value
    U.append(float(filename.split('_')[-2][1:]))
    
    for size in ['big', 'vsg', 'usg']:
        
        # Construct filename
        filename_size = filename.replace('big', size)
    
        # Extract emissivities
        emissivities = np.loadtxt(filename_size, usecols=[0,2], skiprows=61, dtype=[('lambda', float), ('jnu', float)])

        # Check wavelength grid
        if wav is None:
            wav = emissivities['lambda']
        elif not np.all(emissivities['lambda']==wav):
            raise Exception("Wavelength grids do not agree")
        
        # Append emissivity to lists
        jnu[size].append(emissivities['jnu'])

# Make array with U values
U = np.array(U)

# Find correct order for U values
order = np.argsort(U)

# Sort U values
U = U[order]

# Produce final emissivity arrays
for size in ['big', 'vsg', 'usg']:

    # Cast emissivities to array and sort
    jnu_array = np.array(jnu[size]).transpose()[:,order]
        
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
    t.add_column('E', U)
    ts.append(t)
    
    # Write out to HDF5 file
    ts.write('processed/emissivities_%s.hdf5' % size, overwrite=True)
