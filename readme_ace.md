# Distributed Encoding Protocol for Faster Simulation

## Introduction

### Distributed Amplitude Encoding (DE)
There are two approaches to Quantum Computing, namely Quantum-inspired and Quantum Mechanical, where the latter is known as "true" quantum computing. This paradigm was explored in the passage above under QPIXL encoding protocol, which delved into a new manner of implementing FRQI with a linear scalability. As it can be observed, even with a linear scalability, which allows us to have a significantly lower depth compared to RFV and other Amplitude Encoding protocols, we are still unable to encode large images efficiently without use of a preprocessing step, which was the Autoencoder. Hence in this passage, we will look at a new approach which though may not be reliazable with actual hardware, has promise for a much faster simulation. 

The Distributed Encoder, as the name suggests, relies on a "Divide and Conquer" approach, where the image vector (image after being flattened), can be split into chunks of size n, and we can encode each chunk separately using RFV, hence we can encode images as large as 3,840 x 2,160 pixels in a matter of seconds, with log2(n) qubits, and a shallow depth. The process is as follows :

- Import image
- Break image into smaller chunks
- Encode each chunk separately
- Simulate and extract the statevector for each chunk
- Multiply each chunk statevector by the recorded avg chunk ratio to maintain the original ratio
- And classically append
![image](https://user-images.githubusercontent.com/73689800/221870046-06d47c06-2dc3-4a13-90f4-d47d721d1f8a.png)

By using this approach, imagining a 32 x 32 image, instead of needing a RFV PQC with a depth of 2037 and width of 10, we can use 16 RFV PQCs with depth 121 and width of 6, which allows us to have a much faster simulation. This approach shows itself best as we go higher in resolution (Anything larger than 50 x 50), and thus in circuit volume, and we can see this is perhaps the only manner we can perform the simulated encoding.

Below you can see the decoded 4K Ghost in all his glory with RGB colors, where we split the initial image into three Red, Green, and Blue channels, encode each, and decode them by using RGB_Decoder.
![download](https://user-images.githubusercontent.com/73689800/221864333-8793fb2d-9330-4fae-97d4-5210e249813c.png)

### DE Coupled with Dimensionality Reduction
By adding a dimensionality reduction step such as PCA or the autoencoder we used in QPIXL, we can speed up the simulation even further, whilst maintaining almost perfect fidelity. Assume we are using PCA with 300 components. This allows us to reduce a 1,080 x 1,920 to 1,080 x 300, and we can then encode this, and apply the inverse transformation on the statevector extracted to reconstruct the original image with almost no loss in fidelity. Assuming we are using chunks of size 64, this allows us to encode the same image but with 2,160 circuits as compared to 32,400 circuits. Quite a substantial difference!

Below you can see the two images side by side, with and without applying PCA :

With PCA    

![download](https://user-images.githubusercontent.com/73689800/221865071-d3ca761b-c705-4a31-b439-2a3bf93527fd.png)    

Without PCA

![download](https://user-images.githubusercontent.com/73689800/221865342-b50f5c95-3876-491e-924d-88303c43b693.png)


