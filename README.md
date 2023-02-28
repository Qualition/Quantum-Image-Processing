# Quantum Image Processing - embeddings from visualization to classification
A series of python modules for implementing Quantum Image and Signal Processing protocols for image encoding, alteration and classification.


The readme goes through several embedding schemes we have come up with that are either simulator friendly encodings or NISQ friendly as well as implementing them in both artistic and scientific settings.
The main feature is that we have implemented an embedding for the recent **FRQI-QPIXL** framework  (Amankwah et al., May 2022, https://www.nature.com/articles/s41598-022-11024-y ). This is included in two folders, one Qiskit (`QPIXL_qiskit/`) and the other for Pennylane (`QPIXL_pennylane/`).  In both folders ```qpixl.py``` contains a function that generates the full QPIXL embedding with compression on both platforms, and  ```param_qpixl.py``` contains the parameterized version that can be used to generate a NISQ-friendly image feature map for QML amongst other things. In pennylane this can also compress, but in qiskit, it cannot due to limitations on how the parameter vector is processed. This QPIXL embedding is linear in depth with respect to the pixel number, which makes it NISQ-friendly. The circuit is also quick to prepare classically. The notebook describing how it can be used is in `Exploring_QPIXL.ipynb`, which can be explored at the reader's leasure - it includes interactive demos, examples and uses a hybrid quantum-classical network for classifying a cancer dataset. 

Then we have also developed a method for 'chunked' embedding where the image is split up and recombined into a compressed state vector. This method, which we call **Distributed Amplitude Encoding** is much easier on classical compute resources and allows for images as large as 4K to be processed with quantum operations being applied. The results are contained in the `Encoder_Distributed.ipynb`, where you can see how you chunk, normalize, process and stitch the picture back together. It can even handle RGB images. 

Finally, we have also looked at how well standard image embeddings perform in QML using a full quantum workflow - that is, direct quantum embedding, quantum autoencoder, and QNN classifier, and these can be seen in `Autoencoder-QCNN.ipynb`. Here the fashion-MINST data is used to benchmark performance. In the future, we hope to compare different embedding schemes and the performance of the same QNN with varying embeddings of the same dataset, which should be very interesting.

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
    - Distributed Amplitude Encoding
        - Description
        - Coupling scheme with dimensionality reduction  
    - Quantum Autoencoder with Quantum Convolutional Neural Network
        - Autoencoder Architecture
        - Quantum Convolutional Neural Network Results


# QPIXL


## Introduction

### Quantum killers for NISQ
The depth (and connectivity) of a circuit completely determines how well it can be implemented on existing hardware. The killing blow to most
algorithms is that they require fully connected and very deep circuits (which get decomposed to even deeper circuits with limited gatesets). 
Due to non-zero error rates, the probability that at least an error has occurred throughout the run of a circuit eventually becomes 1. This can
be mitigated, but at some point, it can't be done. This is why short circuits for flexible data embeddings are so important.

### Images in quantum computing
Although quantum computers have a more obvious to see an advantage in quantum tasks, nonetheless it is thought that we can see some advantages in tasks involving
classical data loaded onto a quantum computer. Although pictures may not be 'the' data type that will see an advantage from quantum computing, it is nonetheless 
the case that a lot of data can be input in an image-like format, and studying pictoral algorithms is definitely way easier on the eyes than pure data-driven tasks! 
Also, with a quantum state representing an image, you can see the results of any quantum transformation of the picture as a new picture! Of course, it needs to be 
seen from many 'angles', but maybe it can help with visualizing what 

## QPIXL algorithm

Why do we need another type of embedding in the mix? QPIXL is a framework to decompose popular image encodings such as FRQI, NEQR, and their improved counterparts. 
It works by optimally decomposing the gates, and removing any 0 angles that are found. Thanks to the optimal decomposition
the quantum gates can then be further reduced by removing pairs of CNOTS that used to be interwoven by rotation gates. 
They cancel out and become the identity. 
The FRQI embedding looks as follows: 

![](figures/frqi.png)

but decomposed into CNOTS and rotations it looks like this! 

![](figures/frqi_decomp.png)

With QPIXL, the basic embedding, after transforming the image into an angle representation (using arctangent on the pixel values and a Walsh Hadamard transform) you have this much shorter decomposition! 

![](figures/qpixl_decomp.png)

## Compression
If you set the angles 2-6 to 0 (or if they are already 0), you get something that looks like this! The 0 angle rotations are the identity, and 'disappear', and the remaining pairs of CNOTS canceling out :O

![](figures/qpixl_decomp_comp.png)


So you can greatly compress the depth up to some percentage (threshold at which you set angles to 0). What does this look like? See the image below 

For a simple image that is hopefully familiar 

![](figures/aliens_comp.png)

And a more complex image

![](figures/world_comp.png)

This lets you see how much you can compress an image and still retain a high level of detail, obviously finer features disappear the more compression you add, much like traditional JPEG compression. 


## Quantum photoshop
### Single image alteration
You can imagine that you can now do some quantum operations on this encoded state!!!
So what does a global rotation do to our image? Below is an example of RY rotations applied to each qubit with the same angle.

![](figures/test_gif.gif)

You can play around in the notebook for way more options! What does a superposition look like? Does seeing the imaginary part after a rotation look different from the real part? The world is your oyster and the code is ready for you to explore what quantum operations do to high-dimensional embeddings in a super visual way!

### Entangling multiple images

Of course, you can imagine, what if you load two quantum registers with images? Maybe you can entangle them and see the result. Here, the creation of the world, the tripicht from Bosch is entangled with the transpose of itself: 

![](figures/world_combined.png)

Kind of funky, doesn't make much sense, but maybe you can make something more beautiful?

### RGB Batch encoding
You can of course think that you can split the different channels and encode each one separately! There are schemes to do this more compactly, but this particular one is very nice for artistic purposes. For example, Mario here has found himself going through a very strange quantum pipeline where 2/3rds of him have been rotated around the Y axis :O

![](figures/RGB.png)

### Animation
You can animate the transformation from one statevector representing an image to another smoothly! Ever wondered what that looks like (using linear interpolation for the different angles?) The possibilities are endless - maybe you can use a time evolution operator? Creativity is your only boundary. 

![](figures/transform.gif)

## QNN with QPIXL embedding for Cancerous cell classification
Of course, all is well and fun, and we can visualize some cool quantum operations on an 'image state', but obviously, the main reason for these embeddings is not to make nice pictures, but to use them to encode data for tasks like classification for QML, or we can use image embedding to encode different types of data - linear depth is a pretty nice embedding ratio after-all! 

### QML with QPIXL embedding with classical autoencoder for image compression
#### Cancer Dataset with classical autoencoder preconditioning
So instead of using just a directly loaded image QML, we first pre-train a classical autoencoder and do a transfer learning approach. For this toy example, we use a pre-trained resnet18, but one could imagine refining model parameters to a dataset at the same time as the quantum weights! 

![](figures/QPIXL_network.png)

#### Loading the data with ResNet18

We use the cancer dataset, which we reduced to 260x260 in size from around 500x500 classically, and left it to be a 'true' 'false' set, with the boolean value representing the presence of cancer
The dataset can be downloaded here or you can request the modified version from us. https://challengedata.ens.fr/participants/challenges/11/
![](figures/data_eg.png)

This is compressed by the autoencoder and then turned into angles for QPIXL to feed into the Quantum Ansats

#### Defining QNN Tree Tensor Netwrok Ansatz

We then define an ansatz of the form 

![](figures/tree_ansatz.png)

extended to all the 11 qubits + 1  of the input from QPIXL, we add additional RZ rotations after each gate and allow it to output two measurements. 

#### running hybrid classical-quantum QNN
We allowed this to train on a 70-30 split of the dataset using a cross-entropy loss function and the ADAM optimizer, with a stepsize of 4e-4 and 30 epochs. The idea is to optimize the autoencoder and classifier individually at first, getting them to a good initial state and then optimizing both together, sadly we did not manage to get that far, but the results for just optimizing the Quantum part on the ResNet18 compressed feature vector encoded by QPIXL is very promising!  It reached an accuracy on the training data of 70% after 20 epochs! Although the training accuracy is lower, this is promising, maybe this is something that can be looked at further and compared to other embedding schemes! :D 

```
Training started:
...
...
Phase: train Epoch: 20/30 Loss: 0.6958 Acc: 0.6254      
Phase: test   Epoch: 20/30 Loss: 0.6296 Acc: 0.7099       
``` 
The model was pickled mid-training and can be found in the folder ```models/model_QCNN.pickle```, and can be loaded in the ```QPIXL.ipynb``` notebook. 

### Overall QPIXL summary
WE made modules that should make it easy to embed qpixl into any imaging workflow, including parameterized forms that can be used by optimizers in QNN, optimization, and QML tasks for both qiskit and pennylane. We hope this will make it easier for researchers to quickly use such a powerful embedding strategy within their current workflow without having to re-implement everything (if they use packages such as qiskit and pennylane). Furthermore, we have shown how you can visualize complex quantum transformations of these high-dimensional quantum states in a friendly and fun pictorial way - and perhaps a way to make new art with these machines? Whatever the case, we hope that you find QPIXL and these schemes helpful! 


# Distributed Amplitude Encoding (DE)
There are two approaches to Quantum Computing, namely Quantum-inspired and Quantum Mechanical, where the latter is known as "true" quantum computing. This paradigm was explored in the passage above under the QPIXL encoding protocol, which delved into a new manner of implementing FRQI with linear scalability. As it can be observed, even with linear scalability, which allows us to have a significantly lower depth compared to RFV and other Amplitude Encoding protocols, we are still unable to encode large images efficiently without the use of a preprocessing step, which was the Autoencoder. Hence in this passage, we will look at a new approach that though may not be realizable with actual hardware, has promise for a much faster simulation. 

The Distributed Encoder, as the name suggests, relies on a "Divide and Conquer" approach, where the image vector (image after being flattened), can be split into chunks of size n, and we can encode each chunk separately using RFV, hence we can encode images as large as 3,840 x 2,160 pixels in a matter of seconds, with log2(n) qubits, and a shallow depth. The process is as follows :

- Import image
- Break image into smaller chunks
- Encode each chunk separately
- Simulate and extract the statevector for each chunk
- Multiply each chunk statevector by the recorded avg chunk ratio to maintain the original ratio
- And classically append
![image](https://user-images.githubusercontent.com/73689800/221870046-06d47c06-2dc3-4a13-90f4-d47d721d1f8a.png)

By using this approach, imagining a 32 x 32 image, instead of needing an RFV PQC with a depth of 2037 and width of 10, we can use 16 RFV PQCs with a depth 121 and width of 6, which allows us to have a much faster simulation. This approach shows itself best as we go higher in resolution (Anything larger than 50 x 50), and thus in circuit volume, and we can see this is perhaps the only manner we can perform the simulated encoding.

Below you can see the decoded 4K Ghost in all his glory with RGB colors, where we split the initial image into three Red, Green, and Blue channels, encode each and decode them by using RGB_Decoder.
![download](https://user-images.githubusercontent.com/73689800/221864333-8793fb2d-9330-4fae-97d4-5210e249813c.png)

### DE Coupled with Dimensionality Reduction
By adding a dimensionality reduction step such as PCA or the autoencoder we used in QPIXL, we can speed up the simulation even further, whilst maintaining almost perfect fidelity. Assume we are using PCA with 300 components. This allows us to reduce a 1,080 x 1,920 to 1,080 x 300, and we can then encode this, and apply the inverse transformation on the statevector extracted to reconstruct the original image with almost no loss in fidelity. Assuming we are using chunks of size 64, this allows us to encode the same image but with 2,160 circuits as compared to 32,400 circuits. Quite a substantial difference!

Below you can see the two images side by side, with and without applying PCA :

With PCA    

![download](https://user-images.githubusercontent.com/73689800/221865071-d3ca761b-c705-4a31-b439-2a3bf93527fd.png)    

Without PCA

![download](https://user-images.githubusercontent.com/73689800/221865342-b50f5c95-3876-491e-924d-88303c43b693.png)

### DE Filters

Here we can apply quantum filters as well, here is how they look on a moderately large image than a pure quantum approach as in QPIXL. 
![](figures\flower_1.jpg) 
Filter 1 ![](figures\filtered.png)
Filter 2 ![](figures\filter_pixel.png)
For applying filters, we select a chunk size of 4, and for each chunk, we apply a 4 x 4 unitary matrix as filter. Given the nature of the matrix, the effects can vary from bands, to blur, to even pixelation. 

Due to the constraint posed by the filters having to be unitary, we chose a few filters based on actual quantum operations, and we can use this as a visualization for how different operations can change a system through the image's evolution.

# Quantum AutoEncoder and Quantum Convolutional Neural Network

![QAE](https://user-images.githubusercontent.com/80008587/221870996-408f052a-2060-4a9f-8d79-229451cda961.png)
Source: https://arxiv.org/abs/1612.02806

The goal of this is to build a Quantum Autoencoder, a circuit that can compress a quantum state onto a smaller amount of qubits while retaining the information from the initial state.
We give a digital image compressor example to demonstrate the capabilities of such a system to compress different quantum states, as well as the ability to compress images of labels 0 and 1 of the fashion MNIST dataset.
The Architecture of the Quantum AutoEncoder will be a Raw Feature Vector, a trainable Real Amplitudes ansatz, and Swap Test. After that, we will take advantage of the QAE to classify the images by a Quantum Convolutional Neural Network

## QAE Architecture

As stated before, the architecture will be a feature map, a trainable ansatz (we will use Real Amplitudes due to it using only real numbers), and a swap test between the latent and trash space.
Latent space will consist of 4 qubits (first four) and trash space in 6 (5 to 10).

![image](https://user-images.githubusercontent.com/80008587/221895714-f63d57c8-4cb1-4f77-9e27-a91fbfea637d.png)

We are going to train it with 200 images of the fashion MNIST Dataset with labels 0 and 1. This is the decoded output of the AutoEncoder:

![image](https://user-images.githubusercontent.com/80008587/221873817-e55cd655-c9fe-4ed7-a130-d66c9a294327.png)

As far as we can see, we achieve good fidelity results by compressing a 32x32 image represented in 10 qubits to 4 qubits.

## Quantum Convolutional Neural Network

The Neural network will consist of two convolutional layers and two pooling layers as we can see in the image.

![image](https://user-images.githubusercontent.com/80008587/221897049-0c8426f2-8732-4f46-a9d3-7dd38c53dd45.png)

We are going to compose this network to the encoder part of the QAE and then classify it by obtaining the Z expectation value on the fourth qubit. Measuring this value we obtain 1 or -1, which corresponds to the classes.

![image](https://user-images.githubusercontent.com/80008587/221897608-785e307a-733d-4d2e-a14b-ea5e466bf180.png)

Also, we are going to bind the optimal parameters obtained in the QAE to the real amplitude ansatz.

We can see the result of the classification in this image:

![image](https://user-images.githubusercontent.com/80008587/221909685-c8fa6f95-eb62-4421-b42d-1b6d85c358ec.png)

64% for binary classification. Not bad for a fully quantum technique!
