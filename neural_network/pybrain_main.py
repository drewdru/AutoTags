import sys, os
import neural_network
from vk_base import models
import json
import random

from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal


class NetworkInfo:
    num_inputs = 64
    num_hidden = 4
    num_outputs = 10

    hidden_layer_weights = None
    hidden_layer_bias = None
    output_layer_weights = None
    output_layer_bias = None

    total_error = 1

    is_read_file_error = False

    training_sets = []

    def __init__(self, is_train=False):
        self.get_training_sets()
        self.get_network_from_file(is_train)
    
    def get_training_sets(self):
        records = models.Images().get_thematic_training_set()
        print(len(records))
        for index, record in enumerate(records):
            row = []
            hash_array = []
            for hash in record.image_hash:
                hash_array.append(int(hash))
            row.append(hash_array)
            row.append([record.super_id])
            self.training_sets.append(row)

    # def get_network_from_file(self, is_train=False):
    #     network = None
    #     try:
    #         with open('network5.json') as json_data:
    #             network = json.load(json_data)
    #     except FileNotFoundError as error:
    #         if not is_train:
    #             print(error)
    #             print('if you want create new neural-network run with key -t')
    #             self.is_read_file_error = True
    #     if network:
    #         self.num_hidden = network['hidden_layer']['count_neurons']    
    #         self.hidden_layer_bias = []
    #         self.hidden_layer_weights = []    
    #         for neuron in network['hidden_layer']['neurons']:
    #             self.hidden_layer_bias.append(neuron['bias'])
    #             for weight in neuron['weights']:
    #                 self.hidden_layer_weights.append(weight)
            
    #         self.output_layer_bias = []
    #         self.output_layer_weights = []    
    #         for neuron in network['output_layer']['neurons']:
    #             self.output_layer_bias.append(neuron['bias'])
    #             for weight in neuron['weights']:
    #                 self.output_layer_weights.append(weight)
    #         self.total_error = network['total_error']

def train(epsilon=0.001):
    means = [(-1,0),(2,4),(3,1)]
    cov = [diag([1,1]), diag([0.5,1.2]), diag([1.5,0.7])]
    alldata = ClassificationDataSet(2, 1, nb_classes=3)
    for n in range(400):
        for klass in range(3):
            input = multivariate_normal(means[klass],cov[klass])
            alldata.addSample(input, [klass])
    
    tstdata, trndata = alldata.splitWithProportion( 0.25 )

    trndata._convertToOneOfMany( )
    tstdata._convertToOneOfMany( )

    print("Number of training patterns: ", len(trndata))
    print("Input and output dimensions: ", trndata.indim, trndata.outdim)
    print("First sample (input, target, class):")
    print(trndata['input'][0], trndata['target'][0], trndata['class'][0])

    fnn = buildNetwork( trndata.indim, 5, trndata.outdim, outclass=SoftmaxLayer )
    trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

    ticks = arange(-3.,6.,0.2)
    X, Y = meshgrid(ticks, ticks)
    # need column vectors in dataset, not arrays
    griddata = ClassificationDataSet(2,1, nb_classes=3)
    for i in range(X.size):
        griddata.addSample([X.ravel()[i],Y.ravel()[i]], [0])
    griddata._convertToOneOfMany()  # this is still needed to make the fnn feel comfy

    for i in range(20):
        trainer.trainEpochs( 1 )
        trnresult = percentError( trainer.testOnClassData(),trndata['class'] )
        tstresult = percentError( trainer.testOnClassData(dataset=tstdata ), tstdata['class'] )

        print("epoch: %4d" % trainer.totalepochs, \
            "  train error: %5.2f%%" % trnresult, \
            "  test error: %5.2f%%" % tstresult)
        
        out = fnn.activateOnDataset(griddata)
        out = out.argmax(axis=1)  # the highest output activation gives the class
        out = out.reshape(X.shape)

        figure(1)
        ioff()  # interactive graphics off
        clf()   # clear the plot
        hold(True) # overplot on
        for c in [0,1,2]:
            here, _ = where(tstdata['class']==c)
            plot(tstdata['input'][here,0],tstdata['input'][here,1],'o')
        if out.max()!=out.min():  # safety check against flat field
            contourf(X, Y, out)   # plot the contour
        ion()   # interactive graphics on
        draw()  # update the plot
    
    ioff()
    show()


def main():
    pass

if __name__ == "__main__":
    try:
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            sys.exit(help())
        if sys.argv[1] == '--train' or sys.argv[1] == '-t':
            try:
                sys.exit(train(sys.argv[2]))
            except IndexError:
                sys.exit(train())
    except IndexError:
        sys.exit(main())