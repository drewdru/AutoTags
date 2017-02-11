import sys, os
import neural_network
from vk_base import models
import json
import random

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
        # self.training_sets = [
        #     [[0, 0], [0]],
        #     [[0, 1], [1]],
        #     [[1, 0], [1]],
        #     [[1, 1], [0]]
        # ]
        self.get_training_sets()
        # print(self.training_sets)
        self.get_network_from_file(is_train)
    
    def get_training_sets(self):
        records = models.Images().get_thematic_training_set()
        print(len(records))
        for index, record in enumerate(records):
            # if index == 1000:
            #     break
            row = []
            hash_array = []
            for hash in record.image_hash:
                hash_array.append(int(hash))
            row.append(hash_array)

            album_super_id_array = []
            album_super_id_bin = bin(record.super_id).replace('0b', '')
            tmp = ''
            for value in range(10 - len(album_super_id_bin)):
                tmp += '0'
            album_super_id_bin = tmp + album_super_id_bin
            for value in album_super_id_bin:
                album_super_id_array.append(int(value))
            row.append(album_super_id_array)
            self.training_sets.append(row)

    def get_network_from_file(self, is_train=False):
        network = None
        try:
            with open('network5.json') as json_data:
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

def train(epsilon=0.001):
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
    print('networ is get')
    total_error = network.total_error
    count = 0
    while total_error > epsilon:
        try:
            training_inputs, training_outputs = random.choice(network.training_sets)
            # for rang in range(random.randint(100,500)):
            #     nn.train(training_inputs, training_outputs) 
            outputs = nn.feed_forward(network.training_sets[0][0])
            for i in range(len(outputs)):
                outputs[i] = round(outputs[i])

            while outputs != training_outputs:
                nn.train(training_inputs, training_outputs)
                outputs = nn.feed_forward(network.training_sets[0][0])
                for i in range(len(outputs)):
                    outputs[i] = round(outputs[i])

            if count == 100:
                print(outputs, training_outputs)
                total_error = nn.calculate_total_error(network.training_sets)
                print('error = ', total_error)
                network_data = nn.inspect(network.training_sets)
                with open('network5.json', 'w') as outfile:
                    json.dump(network_data, outfile)
                count = 0
            else:
                count += 1
        except Exception as e:
            print(e)
            network_data = nn.inspect(network.training_sets)
            with open('network5.json', 'w') as outfile:
                json.dump(network_data, outfile)

    network_data = nn.inspect(network.training_sets)
    with open('network5.json', 'w') as outfile:
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
    print(network.training_sets[0])
    array_id = nn.feed_forward(network.training_sets[0][0])
    str_array_id = ''
    for id in array_id:
        str_array_id += str(round(id))
    album_super_id = int(str_array_id, 2)    
    print('super_id', album_super_id)
    album_id_record = models.Albums().get_by_super_id(album_super_id)
    if album_id_record is not None:
        print('album_id', album_id_record.album_id) 

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