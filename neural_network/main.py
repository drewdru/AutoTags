import sys, os
import neural_network
from vk_base import models
import json
import random

class NetworkInfo:
    num_inputs = 2
    num_hidden = 5
    num_outputs = 1

    hidden_layer_weights = None
    hidden_layer_bias = None
    output_layer_weights = None
    output_layer_bias = None

    total_error = 1

    is_read_file_error = False

    def __init__(self, is_train=False):
        self.training_sets = [
            [[0, 0], [0]],
            [[0, 1], [1]],
            [[1, 0], [1]],
            [[1, 1], [0]]
        ]
        self.get_network_from_file(is_train)

    def get_network_from_file(self, is_train=False):
        network = None
        try:
            with open('network.json') as json_data:
                network = json.load(json_data)
        except FileNotFoundError as error:
            if not is_train:
                print(error)
                print('if you want create new neural-network run with key -t')
                self.is_read_file_error = True
        if network:
            self.num_hidden = network['hidden_layer']['count_neurons']    
            self.hidden_layer_bias = []
            self.hidden_layer_weights = []    
            for neuron in network['hidden_layer']['neurons']:
                self.hidden_layer_bias.append(neuron['bias'])
                for weight in neuron['weights']:
                    self.hidden_layer_weights.append(weight)
            
            self.output_layer_bias = []
            self.output_layer_weights = []    
            for neuron in network['output_layer']['neurons']:
                self.output_layer_bias.append(neuron['bias'])
                for weight in neuron['weights']:
                    self.output_layer_weights.append(weight)
            
            self.total_error = network['total_error']

def train(epsilon=0.0001):
    network = NetworkInfo(is_train=True)
    nn = neural_network.NeuralNetwork(
        num_inputs = network.num_inputs, 
        num_hidden = network.num_hidden, 
        num_outputs = network.num_outputs, 
        hidden_layer_weights = network.hidden_layer_weights, 
        hidden_layer_bias = network.hidden_layer_bias, 
        output_layer_weights = network.output_layer_weights, 
        output_layer_bias = network.output_layer_bias,
    )
    total_error = network.total_error
    while total_error > epsilon:
        training_inputs, training_outputs = random.choice(network.training_sets)
        nn.train(training_inputs, training_outputs)
        total_error = nn.calculate_total_error(network.training_sets)

    network_data = nn.inspect(network.training_sets)
    with open('network.json', 'w') as outfile:
        json.dump(network_data, outfile)
    print(json.dumps(network_data, sort_keys=True, indent=4, separators=(',', ': ')))
    print(nn.feed_forward(network.training_sets[0][0]))
    print('Total error: ', total_error)

def main():
    network = NetworkInfo()
    if network.is_read_file_error:
        return
    nn = neural_network.NeuralNetwork(
        num_inputs = network.num_inputs, 
        num_hidden = network.num_hidden, 
        num_outputs = network.num_outputs, 
        hidden_layer_weights = network.hidden_layer_weights, 
        hidden_layer_bias = network.hidden_layer_bias, 
        output_layer_weights = network.output_layer_weights, 
        output_layer_bias = network.output_layer_bias,
    )
    network_data = nn.inspect(network.training_sets)
    print(json.dumps(network_data, sort_keys=True, indent=4, separators=(',', ': ')))
    print(nn.feed_forward(network.training_sets[0][0]))

def help():
    print('Usage: python main.py [-h] [-t]')
    print('-t, --train [value]         train neural-network or create new (standart value = 0.0001)')

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