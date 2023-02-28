# Quantum Image Processing
A series of python modules for implementing Quantum Image and Signal Processing protocols for image encoding, classification, and alteration using Quantum Machine Learning.

For the purposes of the hackathon, we wish to implement the QPIXL algorithm in Qiskit (and potentially pennylane) to encode images in O(pixels) depth and log_2(pixels) width, with optional compression. This will then be used to do two things - 1, we will train a QNN to classify cancerous cells from healthy ones. 2. The encoded image will be transformed in various interesting ways and reconstructed to get a very visual idea of what a quantum transformation does to a high dimensional quantum vector. Of course, QML on images may not see any improvements beyond classical ML in this specific subfield, but maybe the techniques of encoding high-dimensional complex classical data into a quantum computer may give rise to ideas of how to better use QML to problems that may be better suited to it. 

## INDEX
- QPIXL
- Batched Raw feature vector
- QML with different encodings


# QPIXL

![](figures/test_gif.gif)
