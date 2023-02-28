# Quantum AutoEncoder and Quantum Convolutional Neural Network

![QAE](https://user-images.githubusercontent.com/80008587/221870996-408f052a-2060-4a9f-8d79-229451cda961.png)
Source: https://arxiv.org/abs/1612.02806

The goal of this is to build an Quantum Autoencoder, a circuit which can compress a quantum state onto a smaller amount of qubits, while retaining the information from the initial state.
We give a digital image compressor example to demonstrate the capabilities of such a system to compress different quantum states, as well as the ability to compress images of labels 0 and 1 of the fashion MNIST dataset.
The Architecture of the Quantum AutoEncoder will be a Raw Feature Vector, a trainable Real Amplitudes ansatz and Swap Test. After that, we will take advantage of the QAE to classify ther images by a Quantum Convolutional Neural Network

## QAE Architecture

As stated before, the architecture will be a feature map, a trainable ansatz (we will use Real Amplitudes due to it uses only real numbers) and a swap test between the latent and trash space.
Latent space will consist in 4 qubits (first four) and trash space in 6 (5 to 10).

![image](https://user-images.githubusercontent.com/80008587/221895714-f63d57c8-4cb1-4f77-9e27-a91fbfea637d.png)

We are going to train it with 200 images of the fashion MNIST Dataset with labels 0 and 1. This is the decoded output of the AutoEncoder:

![image](https://user-images.githubusercontent.com/80008587/221873817-e55cd655-c9fe-4ed7-a130-d66c9a294327.png)

As far as we can see, we achieve good fidelity results by compressing an 32x32 image represented in 10 qubits to 4 qubits.

## Quantum Convolutional Neural Network

The Neural netowrk will consist in two convolutional layers and two pooling layers as we can see in the image.

![image](https://user-images.githubusercontent.com/80008587/221897049-0c8426f2-8732-4f46-a9d3-7dd38c53dd45.png)

We are going to compose this network to the encoder part of the QAE and then classify by obtaining the Z expectation value on the fourth qubit. Measuring this value we obtain 1 or -1, which corresponds to the classes.

![image](https://user-images.githubusercontent.com/80008587/221897608-785e307a-733d-4d2e-a14b-ea5e466bf180.png)

Also, we are going to bind the optimal parameters obtained in the QAE to the real amplitude ansatz.

We can see the result of the classification in this image:

![image](https://user-images.githubusercontent.com/80008587/221909685-c8fa6f95-eb62-4421-b42d-1b6d85c358ec.png)

64% for binary classification. Not bad for a fully quantum technique!
