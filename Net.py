from Neuron import *

Layer = []

class Net:

    def __init__(self, topology):
        self.m_error = 0.0
        self.m_layers = []

        numLayers = len(topology)

        for layerNum in range(0, numLayers):
            self.m_layers.append([])

            if layerNum == len(topology) - 1:
                numOutputs = 0
            else:
                numOutputs = topology[layerNum + 1]

            # We have a new layer, now fill it with neurons, and add a bias neuron in each layer.
            for neuronNum in range(0, topology[layerNum] + 1):
                lastIndex = len(self.m_layers) - 1
                self.m_layers[lastIndex].append(Neuron(numOutputs, neuronNum))

            # Force the bias node's output to 1.0 (last neuron pushed in the latest added layer):
            lastIndex = len(self.m_layers) - 1
            lastNeuronIndex = len(self.m_layers[lastIndex]) - 1
            self.m_layers[lastIndex][lastNeuronIndex].setOutputVal(1.0)

        self.inputLayer = self.m_layers[0]
        self.outputLayer = self.m_layers[len(self.m_layers) - 1]


    def getResults(self):
        results = []
        outputLayer = self.outputLayer

        for outputNeuron in range(0, len(outputLayer) - 1):
            results.append(outputLayer[outputNeuron].getOutputVal())
        return results


    def feedForward(self, inputVals):
        assert(len(inputVals) == len(self.inputLayer) - 1)

        # Assign (latch) the input values into the input neurons
        for i in range(0, len(inputVals)):
            self.inputLayer[i].setOutputVal(inputVals[i])

        # forward propagate
        for layerNum in range(1, len(self.m_layers)):
            prevLayer = self.m_layers[layerNum - 1]
            for n in range(0, len(self.m_layers[layerNum]) - 1):
                self.m_layers[layerNum][n].feedForward(prevLayer)
                n += 1
            layerNum += 1


    def backProp(self, targetVals):
        # Calculate overall net error (RMS of output neuron errors)
        self.m_error = 0.0

        for n in range(0, len(self.outputLayer) - 1):
            delta = targetVals[n] - self.outputLayer[n].getOutputVal()
            self.m_error += delta * delta

        self.m_error /= len(self.outputLayer) - 1    # get average error squared
        self.m_error = math.sqrt(self.m_error)  # RMS

        # Calculate output layer gradients
        for n in range(0, len(self.outputLayer) - 1):
            self.outputLayer[n].calcOutputGradients(targetVals[n])

        # Calculate hidden layer gradients
        layerNum = len(self.m_layers) - 2

        while layerNum > 0:
            hiddenLayer = self.m_layers[layerNum]
            nextLayer = self.m_layers[layerNum + 1]

            for n in range(0, len(hiddenLayer)):
                hiddenLayer[n].calcHiddenGradients(nextLayer)

            layerNum -= 1

        layerNum = len(self.m_layers) - 1

        while layerNum > 0:
            layer = self.m_layers[layerNum]
            prevLayer = self.m_layers[layerNum - 1]

            for n in range(0, len(layer) - 1):
                layer[n].updateInputWeights(prevLayer)
            layerNum -= 1


    def __str__(self):
        ret = ""
        for layer in self.m_layers:
            for neuron in layer:
                ret += str(neuron)
            ret += "\n"

        return ret