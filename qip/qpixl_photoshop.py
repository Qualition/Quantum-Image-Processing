from helper import *
from qpixl import *

def one_image_photoshop(backend, img,shape,comp=10, state_to_prob = np.abs):
    test = pad_0(img)
    test = convertToAngles(test)
    qc = cFRQI(test,10)
    ### INSERT DESIRED GATES HERE
    for i in range(1):
        qc.cnot(i,i+10)
    #################
    job = backend.run(qc)
    sv = np.real(job.result().get_statevector())
    img = decodeQPIXL(sv, state_to_prob = state_to_prob)
    img = reconstruct_img(img, shape)
    return img


def two_image_comb(backend, img1,img2,shape,comp=10,state_to_prob = np.abs):
    img1 = convertToAngles(pad_0(img1))
    img2 = convertToAngles(pad_0(img2))
    qc1 = cFRQI(img1,comp)
    qc2 = cFRQI(img2,comp)
    big_qc = QuantumCircuit(qc1.width()+qc2.width())
    big_qc = big_qc.compose(qc1, qubits=list(range(qc1.width())))
    big_qc = big_qc.compose(qc2, qubits=list(range(qc1.width(),qc1.width()*2)))
    ### INSERT DESIRED GATES HERE
    big_qc.x(range(11,22))
    for i in range(11):
        big_qc.cnot(i, i+qc1.width())
        # Example of CNOT between two images
    #########################
    job = backend.run(big_qc)
    sv = np.real(job.result().get_statevector())
    img = decodeQPIXL(sv, state_to_prob = state_to_prob)#Image 1 is the one that is recovered
    img = reconstruct_img(img, shape)
    return img
