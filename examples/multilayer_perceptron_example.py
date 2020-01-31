import tensorflow.compat.v1 as tf
from tensorflow.examples.tutorials.mnist import input_data

# Here we set tensorflow to work wih version 1 behavior and load in data from the mnist library
# with one-hot encoding on the labels. 
# Ex: 2 = [0,0,1,0,0,0,0,0,0,0]
#     5 = [0,0,0,0,0,1,0,0,0,0]
tf.disable_v2_behavior()
mnist = input_data.read_data_sets("./datasets/", one_hot=True)

# First we define the training batch size, which will be used later on. Then we define 
# Tensorflow placeholders for our functions. These will be used so that we have something to 
# hold our input data with. You will see that we need to define x and y so that the feed_dict in
# sess.run() can place the data somewhere 
# x is of the dimension None x 784 indicating a flat vector of length 784. This represents the intensity
# values of each pixel in the 28x28 input picture. 

batch_size = 100
x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

def neural_network_model(data, layer_sizes):
    """
    data is the input data
    layer_sizes is a list of the sizes of all of the layers for input, output, and hidden layers - inclusive.
    """

    # Each hidden layer is a dictionary of weights and biases of appropriate sizes. The weights are of the dimension
    # [size of previous layer, size of current layer]
    # The biases are of the dimension
    # [size of current layer]
     
    hidden_layers = []
    for i in range(len(layer_sizes)-1):
        hidden_layers.append({'weights':tf.Variable(tf.random_normal([layer_sizes[i], layer_sizes[i+1]])), 
                              'biases':tf.Variable(tf.random_normal([layer_sizes[i+1]]))})

    # The layer operations are defined here. Each layer is a matrix multiplication of the layer inputs and the 
    # layer weights. The biases of the current layer are then added to the result
    # After that, the results are sent through and activation function, this output is sent to the next layer
    # The first hidden layer recieves its input from the raw data, this is why it is outside of the hidden layer
    # for loop. The last layer does not go through an activation function. This is why it is also outside of the
    # for loop.
    # Note: We use len(layer_sizes) - 2 because: 
    # lets say we have the input [784, 500, 500, 500, 10]. The input layer is 784 nodes, there are three hidden
    # layers of 500 nodes each and the output has ten outcomes. layer_outputs[0] is the resultant output from the
    # first hidden layer. layer_outputs[1] is the output of the second hidden layer, and layer_outputs[3] is the 
    # output of the third hidden layer. The output of the third hidden layer is the input to the output layer.
    # Because the output layer has no operations performed on it, this is regarded as the final output or "answer"
    # the model provides. It happens that len(layer_sizes) - 2 = 3, which is the index of the output of the final
    # hidden layer in layer_outputs.

    layer_outputs = []
    layer_outputs.append(tf.add(tf.matmul(data, hidden_layers[0]['weights']), hidden_layers[0]['biases']))
    layer_outputs[0] = tf.nn.relu(layer_outputs[0])

    for i in range(1, len(layer_sizes) - 2):
        layer_outputs.append(tf.add(tf.matmul(layer_outputs[i-1], hidden_layers[i]['weights']), hidden_layers[i]['biases']))
        layer_outputs[i] = tf.nn.relu(layer_outputs[i])

    layer_outputs.append(tf.add(tf.matmul(layer_outputs[len(layer_sizes)-3], hidden_layers[len(layer_sizes)-2]['weights']), hidden_layers[len(layer_sizes)-2]['biases']))
    
    return layer_outputs[len(layer_sizes)-2]

def train_neural_network(x, layer_sizes):
    # First, we save the predicted output the neural network came up with for the input data of this function
    # Next, we define the cost function. This will be used to provide a quantitative measure of how correct we are
    # In this case, it is softmax cross entropy with logits
    # Next, we will choose an optimizer. This is a function which does all of the heavy lifting of cost optimization
    # with backpropagation
    # Then, we define the number of epochs to run. An epoch is a full session of feeding data forward through the 
    # neural network, and then optimizing the weights and biases with our optimizer through backpropagation
    
    prediction = neural_network_model(x, layer_sizes)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)
    n_epochs = 10
    
    # Here we actually begin the tensorflow session. up until now everything has been definitions
    # We first initialize all variables. This fills everything in so that its ready for our intitial round of data
    # Essentially, it is a shorthand init function to get everything set up and ready for the first iteration.
    # Ex: this fills in our placeholders and our random weights and biases
    # Next, we use a handy batch training function from mnist to automatically train the model off of batches
    # It returns the data and labels for a set batch. Up next, we take that batch of data and pass it into 
    # our tensorflow session. This then populates the x and y data and returns our cost and optimizer (I believe)
    # We dont need the optimizer return so we throw it out and keep track of the cost for that epoch 
    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
        
        #training
        for epoch in range(n_epochs):
            epoch_loss = 0 #cost
            #super high level tensorflow training magic
            for _ in range(int(mnist.train.num_examples/batch_size)):
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict={x:epoch_x, y:epoch_y})
                epoch_loss += c
            print('Epoch ', epoch, ' completed out of ', n_epochs, ' loss: ', epoch_loss)
        
        
        # Now, we check to see if the argmaxes of our output tensor and our label tensor match. 
        # Check out this stackoverflow post for more info on argmax : https://stackoverflow.com/questions/41708572/tensorflow-questions-regarding-tf-argmax-and-tf-equal
        # TL;DR it returns the index of the largest value across the specified axis of a tensor.
        #***This is probably correct***
        # So our output might look like [10, 100, 45, 22.2, .....] and our label may be [0, 1, 0, 0, ....]
        # This would imply that our prediction (output) is correct 
        # *** ***
        # This is then used to calculate the accuracy of our model

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1)) #gives the max of those matrixes
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))  #casts the corrext to a float
        print("Accuracy: ", accuracy.eval({x:mnist.test.images, y:mnist.test.labels}))

# Finally, we pass our data placeholder and the dimensions of the neural network into the training function
# and let it run
train_neural_network(x, [784,500,500,500,10])