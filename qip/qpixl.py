from helper import *
from qiskit import QuantumCircuit


def cFRQI(a, compression):
    a = convertToAngles(a, 1) # convert grayscale to angles
    
    n = len(a)
    k = ilog2(n)
    
    a = 2*a 
    a = sfwht(a)
    a = grayPermutation(a) 
    
    idx = list(range(0,n))
    a = sorted(a, key=abs)

    # set smallest absolute values of a to zero according to compression param
    cutoff = (compression / 100.0) * n
    for it in idx[:cutoff]:
        a[it]=0.0
    
    # Construct FRQI circuit
    circuit = QuantumCircuit(k+1)
    # Hadamard register
    circuit.h(range(0,k))
    # Compressed uniformly controlled rotation register
    ctrl, pc, i = 0

    while i < (1<<k):
        # Reset the parity check
        pc = 0

        # Add RY gate
        if  a[i] != 0:
            circuit.ry(k, a[i])

        # Loop over sequence of consecutive zero angles
        while True:
            # Compute control qubit
            if i == (1<<k) - 1:
                ctrl=0
            else:
                ctrl = grayCode(i) ^ grayCode(i + 1)
                ctrl = k - countr_zero(ctrl, n_bits=k) - 1

            # Update parity check
            pc ^= 1 << ctrl
            i += 1
            
            if not (i < (1<<k) and a[i] == 0):
                break

        for j in range(0, k):
            if (pc >> j) & 1:
                circuit.cnot(j, k)
                
    return circuit
