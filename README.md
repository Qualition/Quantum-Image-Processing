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
            - Simple RGB images
            - animation
        - QNN with QPIXL embedding for Cancerous cell classification
            - Cancer Dataset with classical autoencoder preconditioning
            - Loading data with resnet18 autoencoder
            - Defining QNN tree tensor network ansatz
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

This lets you see by how much you can compress an image and still retain a high level of detail, obviously finer features disappear the more compression you add, much like traditional JPEG compression. 


## Quantum photoshop
### Single image alteration
You can imagine that you can now do some quantum operation on this encoded state!!!
So what do a global rotation do to our image? Below is an exampled for RY rotations applied to each qubit with the same angle.

![](figures/test_gif.gif)

You can play around in the notebook for way more options! What does a superposition look like? Does seeing the imaginary part after a rotation look different from the real part? The world is your oyster and the code is ready fopr you to explore what quantum operations do to high-dimensional embeddings ina super visual way!

### Entangling multiple images

Of course, you can imagine, what if you load two quantum registers with images? Maybe you can entangle them and see the result. Here, the creation of the world, the tripicht from Bosch is entangled with the transpose of itself: 

![](figures/world_combined.png)

Kind of funky, doesn't make much sense, but maybe you can make something more beautiful?

### RGB Batch encoding
You can of course think that you can split the different channels and encode each one separately! There are schemes to do this more compactly, but this particular one is very nice for artistic purposes. For example, Mario here has found himself going through a very strange quantum pipeline where 2/3rds of him have been rotated around the Y axis :O

![](figures/RGB.png)

### Animation
You can animate the transformation from one statevector representing an image to another smoothely! Ever wondered what that looks like (using linear interpolation for the different angles?) The possibilities are endless - maybe you can use a time evolution operator? Creativity is your only boundary. 

![](figures/transform.gif)

## QNN with QPIXL embedding for Cancerous cell classification
Of course, all is well and fun, and we can visualize some cool quantum operations on an 'inmage state', but obviously the main reason for these embeddings is not to make nice pictures, but to use them to encode data for tasks like classification for QML, or we can use image embedding to encode different types of data - linear depth is a pretty nice embedding ratio after-all! 

### QML with QPIXL embedding with classical autoencoder for image compression
#### Cancer Dataset with classical autoencoder preconditioning
So instead of using just a directly image loaded QML, we first pretrain a classical autoencoder and do a transfer learning approach. FOr this toy example we use a pretrained resnet18, but one could imagine refining model parameters to a dataset at the same time as the quantum weights! 

![](figures/QPIXL_network.png)

#### Loading the data with ResNet18

We use the cancer dataset, which we prereduced to be 260x260 in size from around 500x500 classically, and left it to be a 'true' 'false' set, with the boolean value representing the presence of cancer

![](figures/data_eg.png)

This is compressed by the autoencoder and then turned into angles for QPIXL to feed into the Quantum Ansats

#### Defining QNN Tree Tensor Netwrok Ansatz

We then define an ansatz of the form 

![](figures/tree_ansatz.png)

extended to all the 11 qubits + 1  of the input from QPIXL, we add additinal RZ rotations after each gate and allow it to output two measurements. 

#### running hybrid classical-quantum QNN
We allowed this to train on a 70-30 split of the dataset using a cross-entropy loss function and the ADAM optimizer, with a stepsize of 4e-4 and 30 epochs. The idea is to optimize the autoencoder and classifier individually at first, getting them to a good initial state and then optimizing both together, sadly we did not manage to get that far, but the results for just optimizing the Quantum part on the ResNet18 comopressed feature vector encoded by QPIXL is very promising!  It reached an accuracy on the training data of 70% after 20 epochs! Alhtough the training accuracy is lower, but this is promising, maybe this is something that can be looked at further and compared to other embedding schemes! :D 

```
Training started:
...
...
Phase: train Epoch: 20/30 Loss: 0.6958 Acc: 0.6254      
Phase: test   Epoch: 20/30 Loss: 0.6296 Acc: 0.7099       
``` 
The model was pickled mid-training and can be found in the folder ```models/model_QCNN.pickle```, and can be loaded in the ```QPIXL.ipynb``` notebook. 

### Overall QPIXL summary
WE made modules that should make it easy to embedd qpixl into any image workflow, including parameterized forms that can be used by optimizers in QNN, optimization and QML tasks for both qiskit and pennylane. WE hope this will make it easier for researchers to quickly use such a powerful embedding strategy within their current workflow without having to re-implement everything (if they use packages such as qiskit and pennylane). Furthermore, we have shown how you can visualize complex quantum transformations of these high-dimensional quantum states in a friendly and fun pictoral way - and perhaps a way to make new art with these machines? Whatever the case, we hope that you find QPIXL and these schemes helpful! 
