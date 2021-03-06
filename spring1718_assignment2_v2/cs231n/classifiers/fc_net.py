from builtins import range
from builtins import object
import numpy as np

from cs231n.layers import *
from cs231n.layer_utils import *


class TwoLayerNet(object):
    """
    A two-layer fully-connected neural network with ReLU nonlinearity and
    softmax loss that uses a modular layer design. We assume an input dimension
    of D, a hidden dimension of H, and perform classification over C classes.

    The architecture should be affine - relu - affine - softmax.

    Note that this class does not implement gradient descent; instead, it
    will interact with a separate Solver object that is responsible for running
    optimization.

    The learnable parameters of the model are stored in the dictionary
    self.params that maps parameter names to numpy arrays.
    """

    def __init__(self, input_dim=3*32*32, hidden_dim=100, num_classes=10,
                 weight_scale=1e-3, reg=0.0):
        """
        Initialize a new network.

        Inputs:
        - input_dim: An integer giving the size of the input
        - hidden_dim: An integer giving the size of the hidden layer
        - num_classes: An integer giving the number of classes to classify
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - reg: Scalar giving L2 regularization strength.
        """
        self.params = {}
        self.reg = reg

        ############################################################################
        # TODO: Initialize the weights and biases of the two-layer net. Weights    #
        # should be initialized from a Gaussian centered at 0.0 with               #
        # standard deviation equal to weight_scale, and biases should be           #
        # initialized to zero. All weights and biases should be stored in the      #
        # dictionary self.params, with first layer weights                         #
        # and biases using the keys 'W1' and 'b1' and second layer                 #
        # weights and biases using the keys 'W2' and 'b2'.                         #
        ############################################################################
        w1 = np.random.normal(0.0, weight_scale, (input_dim, hidden_dim))
        b1 = np.zeros((1, hidden_dim))
        w2 = np.random.normal(0.0, weight_scale, (hidden_dim, num_classes))
        b2 = np.zeros((1, num_classes))
        self.params["W1"] = w1
        self.params["b1"] = b1
        self.params["W2"] = w2
        self.params["b2"] = b2
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################


    def loss(self, X, y=None):
        """
        Compute loss and gradient for a minibatch of data.

        Inputs:
        - X: Array of input data of shape (N, d_1, ..., d_k)
        - y: Array of labels, of shape (N,). y[i] gives the label for X[i].

        Returns:
        If y is None, then run a test-time forward pass of the model and return:
        - scores: Array of shape (N, C) giving classification scores, where
          scores[i, c] is the classification score for X[i] and class c.

        If y is not None, then run a training-time forward and backward pass and
        return a tuple of:
        - loss: Scalar value giving the loss
        - grads: Dictionary with the same keys as self.params, mapping parameter
          names to gradients of the loss with respect to those parameters.
        """
        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the two-layer net, computing the    #
        # class scores for X and storing them in the scores variable.              #
        ############################################################################
        w1, b1, w2, b2 = self.params["W1"], self.params["b1"], self.params["W2"], self.params["b2"]
        layer1_output, layer1_cache = affine_relu_forward(X, w1, b1)
        layer2_output, layer2_cache = affine_forward(layer1_output, w2, b2)
        scores = layer2_output
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If y is None then we are in test mode so just return scores
        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TODO: Implement the backward pass for the two-layer net. Store the loss  #
        # in the loss variable and gradients in the grads dictionary. Compute data #
        # loss using softmax, and make sure that grads[k] holds the gradients for  #
        # self.params[k]. Don't forget to add L2 regularization!                   #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        loss, dout = softmax_loss(scores, y)
        w1_l2_norm = np.sum(w1 ** 2)
        w2_l2_norm = np.sum(w2 ** 2)
        loss += ((0.5 * self.reg * w1_l2_norm) + (0.5 * self.reg * w2_l2_norm))
        dout, grads["W2"], grads["b2"] = affine_backward(dout, layer2_cache)
        dout, grads["W1"], grads["b1"] = affine_relu_backward(dout, layer1_cache)
        '''
        The gradients must be increased by a factor of (2*lambda*W) because of the derivative of the regularization
        used.
        '''
        # The 0.5 (included factor to simplify the expression for the gradient) must be also considered.
        partial_adding_factor = 0.5 * 2 * self.reg
        grads["W2"] += partial_adding_factor * w2
        grads["W1"] += partial_adding_factor * w1
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads


class FullyConnectedNet(object):
    """
    A fully-connected neural network with an arbitrary number of hidden layers,
    ReLU nonlinearities, and a softmax loss function. This will also implement
    dropout and batch/layer normalization as options. For a network with L layers,
    the architecture will be

    {affine - [batch/layer norm] - relu - [dropout]} x (L - 1) - affine - softmax

    where batch/layer normalization and dropout are optional, and the {...} block is
    repeated L - 1 times.

    Similar to the TwoLayerNet above, learnable parameters are stored in the
    self.params dictionary and will be learned using the Solver class.
    """

    def __init__(self, hidden_dims, input_dim=3*32*32, num_classes=10,
                 dropout=1, normalization=None, reg=0.0,
                 weight_scale=1e-2, dtype=np.float32, seed=None):
        """
        Initialize a new FullyConnectedNet.

        Inputs:
        - hidden_dims: A list of integers giving the size of each hidden layer.
        - input_dim: An integer giving the size of the input.
        - num_classes: An integer giving the number of classes to classify.
        - dropout: Scalar between 0 and 1 giving dropout strength. If dropout=1 then
          the network should not use dropout at all.
        - normalization: What type of normalization the network should use. Valid values
          are "batchnorm", "layernorm", or None for no normalization (the default).
        - reg: Scalar giving L2 regularization strength.
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - dtype: A numpy datatype object; all computations will be performed using
          this datatype. float32 is faster but less accurate, so you should use
          float64 for numeric gradient checking.
        - seed: If not None, then pass this random seed to the dropout layers. This
          will make the dropout layers deteriminstic so we can gradient check the
          model.
        """
        self.normalization = normalization
        self.use_dropout = dropout != 1
        self.reg = reg
        self.num_layers = 1 + len(hidden_dims)
        self.dtype = dtype
        self.params = {}

        ############################################################################
        # TODO: Initialize the parameters of the network, storing all values in    #
        # the self.params dictionary. Store weights and biases for the first layer #
        # in W1 and b1; for the second layer use W2 and b2, etc. Weights should be #
        # initialized from a normal distribution centered at 0 with standard       #
        # deviation equal to weight_scale. Biases should be initialized to zero.   #
        #                                                                          #
        # When using batch normalization, store scale and shift parameters for the #
        # first layer in gamma1 and beta1; for the second layer use gamma2 and     #
        # beta2, etc. Scale parameters should be initialized to ones and shift     #
        # parameters should be initialized to zeros.                               #
        ############################################################################
        self.params["W1"] = np.random.normal(0.0, weight_scale, (input_dim, hidden_dims[0]))
        self.params["b1"] = np.zeros((1, hidden_dims[0]))
        if self.normalization == 'batchnorm':
            # Begin - BatchNorm block.
            self.params["gamma1"] = np.ones((1, hidden_dims[0]))
            self.params["beta1"] = np.zeros((1, hidden_dims[0]))
            # End - BatchNorm block.
        num_params_inside_hl = len(hidden_dims) - 1
        for i in range(num_params_inside_hl):
            index = str(i + 2)
            wx, bx = "W{}".format(index), "b{}".format(index)
            self.params[wx] = np.random.normal(0.0, weight_scale, (hidden_dims[i], hidden_dims[i + 1]))
            self.params[bx] = np.zeros((1, hidden_dims[i + 1]))
            if self.normalization == 'batchnorm':
                # Begin - BatchNorm block.
                self.params["gamma{}".format(index)] = np.ones((1, hidden_dims[i + 1]))
                self.params["beta{}".format(index)] = np.zeros((1, hidden_dims[i + 1]))
                # End - BatchNorm block.
        index = str(self.num_layers)
        wx, bx = "W{}".format(index), "b{}".format(index)
        self.params[wx] = np.random.normal(0.0, weight_scale, (hidden_dims[num_params_inside_hl], num_classes))
        self.params[bx] = np.zeros((1, num_classes))
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # When using dropout we need to pass a dropout_param dictionary to each
        # dropout layer so that the layer knows the dropout probability and the mode
        # (train / test). You can pass the same dropout_param to each dropout layer.
        self.dropout_param = {}
        if self.use_dropout:
            self.dropout_param = {'mode': 'train', 'p': dropout}
            if seed is not None:
                self.dropout_param['seed'] = seed

        # With batch normalization we need to keep track of running means and
        # variances, so we need to pass a special bn_param object to each batch
        # normalization layer. You should pass self.bn_params[0] to the forward pass
        # of the first batch normalization layer, self.bn_params[1] to the forward
        # pass of the second batch normalization layer, etc.
        self.bn_params = []
        if self.normalization=='batchnorm':
            self.bn_params = [{'mode': 'train'} for i in range(self.num_layers - 1)]
        if self.normalization=='layernorm':
            self.bn_params = [{} for i in range(self.num_layers - 1)]

        # Cast all parameters to the correct datatype
        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)


    def loss(self, X, y=None):
        """
        Compute loss and gradient for the fully-connected net.

        Input / output: Same as TwoLayerNet above.
        """
        X = X.astype(self.dtype)
        mode = 'test' if y is None else 'train'

        # Set train/test mode for batchnorm params and dropout param since they
        # behave differently during training and testing.
        if self.use_dropout:
            self.dropout_param['mode'] = mode
        if self.normalization=='batchnorm':
            for bn_param in self.bn_params:
                bn_param['mode'] = mode
        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the fully-connected net, computing  #
        # the class scores for X and storing them in the scores variable.          #
        #                                                                          #
        # When using dropout, you'll need to pass self.dropout_param to each       #
        # dropout forward pass.                                                    #
        #                                                                          #
        # When using batch normalization, you'll need to pass self.bn_params[0] to #
        # the forward pass for the first batch normalization layer, pass           #
        # self.bn_params[1] to the forward pass for the second batch normalization #
        # layer, etc.                                                              #
        ############################################################################
        if self.normalization == 'batchnorm':
            layer1_output, layer1_cache = self.affine_batchnorm_relu_forward(X, self.params["W1"], self.params["b1"],
                                                                             self.params["gamma1"],
                                                                             self.params["beta1"], self.bn_params[0])
        else:
            layer1_output, layer1_cache = affine_relu_forward(X, self.params["W1"], self.params["b1"])
        if self.use_dropout:
            temp_dropout_cache = list([None])
            layer1_output, layer1_dropout_cache = dropout_forward(layer1_output, self.dropout_param)
            temp_dropout_cache.append(layer1_dropout_cache)
        temp_output, temp_cache = list([None]), list([None])
        temp_output.append(layer1_output)
        temp_cache.append(layer1_cache)
        for i in range(self.num_layers - 2):
            index = str(i + 2)
            # wx, bx = "W{}".format(index), "b{}".format(index)
            wx, bx, gammax, betax = "W{}".format(index), "b{}".format(index), "gamma{}".format(index), \
                                    "beta{}".format(index)
            if self.normalization == 'batchnorm':
                layerx_output, layerx_cache = self.affine_batchnorm_relu_forward(temp_output[i + 1], self.params[wx],
                                                                                 self.params[bx], self.params[gammax],
                                                                                 self.params[betax],
                                                                                 self.bn_params[i + 1])
            else:
                layerx_output, layerx_cache = affine_relu_forward(temp_output[i + 1], self.params[wx], self.params[bx])
            if self.use_dropout:
                layerx_output, layerx_dropout_cache = dropout_forward(layerx_output, self.dropout_param)
                temp_dropout_cache.append(layerx_dropout_cache)
            temp_output.append(layerx_output)
            temp_cache.append(layerx_cache)
        index = str(self.num_layers)
        wx, bx = "W{}".format(index), "b{}".format(index)
        scores, layern_cache = affine_forward(temp_output[self.num_layers - 1], self.params[wx], self.params[bx])
        temp_output.append(scores)
        temp_cache.append(layern_cache)
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If test mode return early
        if mode == 'test':
            return scores

        loss, grads = 0.0, {}
        ############################################################################
        # TODO: Implement the backward pass for the fully-connected net. Store the #
        # loss in the loss variable and gradients in the grads dictionary. Compute #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        #                                                                          #
        # When using batch/layer normalization, you don't need to regularize the scale   #
        # and shift parameters.                                                    #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        loss, dout = softmax_loss(scores, y)
        regularization = 0
        for i in range(self.num_layers):
            regularization += (0.5 * self.reg * np.sum(self.params["W{}".format(str(i + 1))] ** 2))
        loss += regularization
        index = str(self.num_layers)
        wx, bx = "W{}".format(index), "b{}".format(index)
        dout, grads[wx], grads[bx] = affine_backward(dout, temp_cache[self.num_layers])
        for i in range(self.num_layers - 1, 0, -1):
            index = str(i)
            # wx, bx = "W{}".format(index), "b{}".format(index)
            wx, bx, gammax, betax = "W{}".format(index), "b{}".format(index), "gamma{}".format(index), \
                                    "beta{}".format(index)
            if self.use_dropout:
                dout = dropout_backward(dout, temp_dropout_cache[i])
            if self.normalization == 'batchnorm':
                dout, grads[wx], grads[bx], grads[gammax], grads[betax] = self\
                    .affine_batchnorm_relu_backward(dout, temp_cache[i])
            else:
                dout, grads[wx], grads[bx] = affine_relu_backward(dout, temp_cache[i])
        '''
        The gradients must be increased by a factor of (2*lambda*W) because of the derivative of the regularization
        used.
        '''
        # The 0.5 (included factor to simplify the expression for the gradient) must be also considered.
        partial_adding_factor = 0.5 * 2 * self.reg
        for i in range(self.num_layers):
            index = str(i + 1)
            wx = "W{}".format(index)
            grads[wx] += partial_adding_factor * self.params[wx]
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads

    def affine_batchnorm_relu_forward(self, x, w, b, gamma, beta, bn_param):
        """
        Convenience layer that performs an affine transform followed by a BatchNormalization and ReLU.
        """
        a, fc_cache = affine_forward(x, w, b)
        a_norm, bn_cache = batchnorm_forward(a, gamma, beta, bn_param)
        out, relu_cache = relu_forward(a_norm)
        cache = (fc_cache, bn_cache, relu_cache)
        return out, cache

    def affine_batchnorm_relu_backward(self, dout, cache):
        """
        Backward pass for the affine-batchnorm-relu convenience layer.
        """
        fc_cache, bn_cache, relu_cache = cache
        da = relu_backward(dout, relu_cache)
        da_norm, dgamma, dbeta = batchnorm_backward(da, bn_cache)
        dx, dw, db = affine_backward(da_norm, fc_cache)
        return dx, dw, db, dgamma, dbeta
