from helper import *
from qiskit import QuantumCircuit


def cFRQI(a, compression):
    """
    Takes a standard image in a numpy array (so that the matrix looks like
    the image you want if you picture the pixels) and returns the QPIXL
    compressed FRQI circuit. The compression ratio determines
    how many gates will be filtered and then cancelled out. 
    a = numpy array of image
    compression = number between 0 an 100, where 0 is no compression and 100 is no image
    returns: qiskit circuit with encoded image
    """
    a = convertToAngles(a) # convert grayscale to angles
    a = preprocess_image(a) # need to flatten the transpose for easier decoding, 
                            # only really necessary if you want to recover an image.
                            # for classification tasks etc. transpose isn't required.
    n = len(a)
    k = ilog2(n)

    a = 2*a 
    a = sfwht(a)
    a = grayPermutation(a) 
    a_sort_ind = np.argsort(np.abs(a))

    # set smallest absolute values of a to zero according to compression param
    cutoff = int((compression / 100.0) * n)
    for it in a_sort_ind[:cutoff]:
        a[it] = 0
    # print(a)
    # Construct FRQI circuit
    circuit = QuantumCircuit(k + 1)
    # Hadamard register
    circuit.h(range(k))
    # Compressed uniformly controlled rotation register
    ctrl, pc, i = 0, 0, 0
    while i < (2**k):
        # Reset the parity check
        pc = int(0)

        # Add RY gate
        if a[i] != 0:
            circuit.ry(a[i], k)

        # Loop over sequence of consecutive zero angles to 
        # cancel out CNOTS (or rather, to not include them)
        if i == ((2**k) - 1):
            ctrl=0
        else:
            ctrl = grayCode(i) ^ grayCode(i+1)
            ctrl = k - countr_zero(ctrl, n_bits=k+1) - 1

        # Update parity check
        pc ^= (2**ctrl)
        i += 1
        
        while i < (2**k) and a[i] == 0:
            # Compute control qubit
            if i == ((2**k) - 1):
                ctrl=0
            else:
                ctrl = grayCode(i) ^ grayCode(i+1)
                ctrl = k - countr_zero(ctrl, n_bits=k+1) - 1

            # Update parity check
            pc ^= (2**ctrl)
            i += 1
                        
        for j in range(k):
            if (pc >> j)  &  1:
                circuit.cnot(j, k)
                
    return circuit