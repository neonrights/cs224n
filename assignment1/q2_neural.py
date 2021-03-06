#!/usr/bin/env python

import numpy as np
import random

from q1_softmax import softmax
from q2_sigmoid import sigmoid, sigmoid_grad
from q2_gradcheck import gradcheck_naive


def forward_backward_prop(X, labels, params, dimensions):
    """
    Forward and backward propagation for a two-layer sigmoidal network

    Compute the forward propagation and for the cross entropy cost,
    the backward propagation for the gradients for all parameters.

    Notice the gradients computed here are different from the gradients in
    the assignment sheet: they are w.r.t. weights, not inputs.

    Arguments:
    X -- M x Dx matrix, where each row is a training example x.
    labels -- M x Dy matrix, where each row is a one-hot vector.
    params -- Model parameters, these are unpacked for you.
    dimensions -- A tuple of input dimension, number of hidden units
                  and output dimension
    """

    ### Unpack network parameters (do not modify)
    ofs = 0
    Dx, H, Dy = (dimensions[0], dimensions[1], dimensions[2])

    W1 = params[ofs:(ofs + Dx * H)].reshape(Dx, H)
    ofs += Dx * H
    b1 = params[ofs:(ofs + H)].reshape(1, H)
    ofs += H
    W2 = np.reshape(params[ofs:(ofs + H * Dy)], (H, Dy))
    ofs += H * Dy
    b2 = np.reshape(params[ofs:(ofs + Dy)], (1, Dy))

    # Note: compute cost based on `sum` not `mean`.
    ### YOUR CODE HERE: forward propagation
    hidden = sigmoid(np.matmul(X, W1) + b1)
    logits = softmax(np.matmul(hidden, W2) + b2)
    cost = -np.sum(labels * np.log(logits))
    ### END YOUR CODE

    M = X.shape[0]
    assert hidden.shape == (M, H)
    assert logits.shape == (M, Dy)

    ### YOUR CODE HERE: backward propagation
    dcost = logits - labels
    gradW2 = np.matmul(hidden.transpose(), dcost)
    gradb2 = dcost.sum(0).reshape(1, Dy)
    dH = np.matmul(dcost, W2.transpose()) * sigmoid_grad(hidden)
    gradW1 = np.matmul(X.transpose(), dH)
    gradb1 = dH.sum(0).reshape(1, H)
    ### END YOUR CODE

    assert gradW1.shape == W1.shape
    assert gradb1.shape == b1.shape
    assert gradW2.shape == W2.shape
    assert gradb2.shape == b2.shape

    ### Stack gradients (do not modify)
    grad = np.concatenate((gradW1.flatten(), gradb1.flatten(),
        gradW2.flatten(), gradb2.flatten()))

    assert params.shape == grad.shape
    return cost, grad


def sanity_check():
    """
    Set up fake data and parameters for the neural network, and test using
    gradcheck.
    """
    print("Running sanity check...")

    N = 20
    dimensions = [10, 5, 10]
    data = np.random.randn(N, dimensions[0])   # each row will be a datum
    labels = np.zeros((N, dimensions[2]))
    for i in range(N):
        labels[i, random.randint(0,dimensions[2]-1)] = 1

    params = np.random.randn((dimensions[0] + 1) * dimensions[1] + (
        dimensions[1] + 1) * dimensions[2], )

    gradcheck_naive(lambda params:
        forward_backward_prop(data, labels, params, dimensions), params)


def your_sanity_checks():
    """
    Use this space add any additional sanity checks by running:
        python q2_neural.py
    This function will not be called by the autograder, nor will
    your additional tests be graded.
    """
    print("Running your sanity checks...")
    ### YOUR CODE HERE
    #raise NotImplementedError
    ### END YOUR CODE


if __name__ == "__main__":
    sanity_check()
    your_sanity_checks()
