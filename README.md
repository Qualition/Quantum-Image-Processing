# Quantum Image Processing
A series of python modules for implementing Quantum Image and Signal Processing protocols for image encoding, classification, and alteration using Quantum Machine Learning.


The readme goes through several embedding schemes we have come up with that are either good for simulating (simulator friendly encodings) and NISQ friendly hardware friendly. 
The main feature is that we have implemented an embedding in qiskit for the FRQI-QPIXL framework  (Amankwah et al., May 2022, https://www.nature.com/articles/s41598-022-11024-y ). 
This is included in two folders, one for a qiskit version and another for a pennylane version.  ```qpixl.py``` for the full version with compression, and  ```param_qpixl.py``` contains the parameterized version that can be used to generate a NISQ friendly image feature map for QML amongst other things.

- Contents
    - Introduction
    - QPIXL (```QPIXL.ipynb```)
        - compression
        -  Photoshop
            - single image transforms
            - entangling multiple images
            - Animations
            - Simple RGB images
        - QNN with QPIXL embedding
            - Cancer Dataset with classical autoencoder preconditioning
            - Loading data
            - Defining QNN tree tensor network ansatz
            - Defining resnet18 autoencoder
            - running hybrid classical-quantum QNN

# QPIXL


## Introduction

### Quantum killers for NISQ
The depth (and connectivity) of a circuit completely determines how well it can be implemented on existing hardware. The killing blow to most
algorithms is that they require fully connected and very deep circuits (which get decomposed to even deeper circuits with limited gatesets). 
Due to non-zero error rates, the probability that at least an error has occured throughout the run of a circuit eventually becomes 1. This can
be mitigated, but at some point it can't be done. This is why short circuits for flexible data embeddings are so important.

### Images in quantum computing
Although quantum computers have a more obvious to see advantage in quantum tasks, nonetheless it is thought that we can see some advantages in tasks involving
classical data loaded onto a quantum computer. Although pictures may not be 'the' data-type that will see an advantage from quantum computing, it is nonetheless 
the case that a lot of data can be input in an image-like format, and studying pictoral algorihtms is definitely way easier on the eyes than pure data-driven tasks! 
Also, with a quantum state representing an image, you can see the results of any quantum transformation of the picture as a new picture! Of course, it needs to be 
seen from many 'angles', but maybe it can help with visualizing what 

## QPIXL algorithm

Why do we need another type of embedding in the mix? QPIXL is a framework to decompose popular image encodings such as FRQI, NEQR and their improved counterparts. 
It works by optimally decomposing the gates, and removing any 0 angles that are found. Thanks to the optimal decomposition
the quantum gates can then be further reduced by removing pairs of CNOTS that used to be interweaved by rotation gates. 
They cancel out an become the identity. 
The FRQI embedding looks as follows: 

![](figures/frqi.png)

but decomposed into CNOTS and rotations it looks like this! 

![](figures/frqi_decomp.png)

With QPIXL, the basic embedding, after transforming the image into an angle representation (using arctangent on the pixel values and a walsh hadamard transform) you have this much shorter decomposition! 

![](figures/qpixl_decomp.png)

## Compression
If you set the angles 2-6 to 0 (or if they are already 0), you get something that looks like this! The 0 angle rotations are the identity, and 'disappear', and the remaining the pairs of CNOTS cancelling out :O

![](figures/qpixl_decomp_comp.png)


So you can greatly compress the depth up to some percentage (treshold at which you set angles to 0). Whaty does this look like? See the image below 

For a simple image that is hopefully familiar 

![](figures/aliens_comp.png)

And a more complex image

![](figures/world_comp.png)


![](figures/test_gif.gif)