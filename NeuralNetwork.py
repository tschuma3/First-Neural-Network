import numpy as np
import matplotlib.pyplot as plt

class NeuralNetwork:
    def __init__(self, learning_Rate):
        self.weights = np.array([np.random.randn(), np.random.randn()])
        self.bias = np.random.randn()
        self.learning_Rate = learning_Rate

    #Layer 2
    #Sigmoid function
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    #Sigmoid after deriving
    def sigmoid_Deriv(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    #Makes a prediction using layers
    def prediction(self, input_Vector):
        layer_1 = np.dot(input_Vector, self.weights) + self.bias
        layer_2 = self.sigmoid(layer_1)
        prediction = layer_2
        return prediction
    
    #Computes the gradients
    def compute_Gradients(self, input_Vector, target):
        #First time
        layer_1 = np.dot(input_Vector, self.weights) + self.bias
        layer_2 = self.sigmoid(layer_1)
        prediction = layer_2

        #Second time
        dError_DPrediction = 2 * (prediction - target)
        dPrediction_DLayer1 = self.sigmoid_Deriv(layer_1)
        dLayer1_DBias = 1
        dLayer1_DWeights = (0 * self.weights) + (1 + input_Vector)

        #Calculates the error bias and error weights
        dError_DBias = (dError_DPrediction * dPrediction_DLayer1 * dLayer1_DBias)
        dError_DWeights = (dError_DPrediction * dPrediction_DLayer1 * dLayer1_DWeights)

        return dError_DBias, dError_DWeights

    #Updates the parameters
    def updates_Parameters(self, dError_DBias, dError_DWeights):
        self.bias = self.bias - (dError_DBias * self.learning_Rate)
        self.weights = self.weights - (dError_DWeights * self.learning_Rate)

    #Training the brain
    def train(self, input_Vectors, targets, iterations):
        cumulative_Errors = []
        for current_Iteration in range(iterations):
            #Picks a data point at random
            random_Data_Index = np.random.randint(len(input_Vectors))

            input_Vector = input_Vectors[random_Data_Index]
            target = targets[random_Data_Index]

            #Computes the gradients and update the weights
            dError_dBias, dError_DWeights = self.compute_Gradients(input_Vector, target)

            #Updates the bias and weights
            self.updates_Parameters(dError_dBias, dError_DWeights)

            #Checks and observes the error change over 100 iterations
            if current_Iteration % 100 == 0:
                cumulative_Error = 0
                #Loop through all the instances to measure the error
                for data_Instance_Index in range(len(input_Vectors)):
                    date_Point = input_Vectors[data_Instance_Index]
                    target = targets[data_Instance_Index]

                    #Computes the prediction results
                    prediction = self.prediction(date_Point)
                    #Computes the error for every instance
                    error = np.square(prediction - target)

                    #Computes the sum of the errors and add to the array
                    cumulative_Error = cumulative_Error + error
                cumulative_Errors.append(cumulative_Error)
        
        return cumulative_Errors
    
#Makes a prediction and displays the result in a graph
input_vectors = np.array(
     [
         [3, 1.5],
         [2, 1],
         [4, 1.5],
         [3, 4],
         [3.5, 0.5],
         [2, 0.5],
         [5.5, 1],
         [1, 1],
     ]
   )

targets = np.array([0, 1, 0, 1, 0, 1, 1, 0])

learning_Rate = 0.1

neural_network = NeuralNetwork(learning_Rate)

training_error = neural_network.train(input_vectors, targets, 10000)

plt.plot(training_error)
plt.xlabel("Iterations")
plt.ylabel("Error for all training instances")
plt.savefig("cumulative_error1.png")
