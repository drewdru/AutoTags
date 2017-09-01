import sys, os
from . import neural_network
# from vk_base import models
import json
import random
import math

from PIL import Image

def get_histogram(img, size):
    """Get the image histogram on the 3rd channels
       @return histograms array
    """
    histogram_r = []
    histogram_g = []
    histogram_b = []
    for i in range(256):
        histogram_r.append(0)
        histogram_g.append(0)
        histogram_b.append(0)
    for i in range(size[0]):
        for j in range(size[1]):
            r, g, b = img.getpixel((i, j))
            histogram_r[r] += 1
            histogram_g[g] += 1
            histogram_b[b] += 1
    histogram = []
    for i in range(256):
        histogram_r[i] /= size[0]*size[1]
        histogram_g[i] /= size[0]*size[1]
        histogram_b[i] /= size[0]*size[1]
        histogram.append(histogram_r[i])
        histogram.append(histogram_g[i])
        histogram.append(histogram_b[i])
    return histogram

def create_training_sets():
    """Create training sets from directories with images.
       Use directories  for image classification.
    """
    image_paths = ['./autumn/', './summer/', './spring/', './winter/']
    image_list = {'image': []}
    size = 64, 64

    for season_idx, path in enumerate(image_paths):
        season = [0, 0, 0, 0]
        season[season_idx] = 1
        image_list = os.listdir(path)
        for in_image in image_list:
            img = Image.open(path + in_image)
            img = img.convert(mode='RGB')
            img = img.resize(size, Image.ANTIALIAS)
            histogram = get_histogram(img, size)
            obj = {
                'histogram': histogram,
                'season': season,
            }
            image_list['image'].append(obj)

    with open('training_set.json', 'w') as outfile:
        json.dump(image_list, outfile)


class NetworkInfo:
    """Network info class"""
    num_inputs = 256*3
    num_hidden = 4
    num_outputs = 4

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
        """Setup training sets from file"""
        while True:
            try:
                with open('training_set.json') as json_data:
                    training_set = json.load(json_data)
                    for image in training_set['image']:
                        row = [image['histogram'], image['season']]
                        self.training_sets.append(row)
                break
            except FileNotFoundError:
                create_training_sets()

    def get_network_from_file(self, is_train=False):
        """Setup neural network from file"""
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

def train(epsilon=0.001):
    """Training neural_network"""
    network = NetworkInfo(is_train=True)
    neural_network_data = neural_network.NeuralNetwork(
        num_inputs=network.num_inputs,
        num_hidden=network.num_hidden,
        num_outputs=network.num_outputs,
        hidden_layer_weights=network.hidden_layer_weights,
        hidden_layer_bias=network.hidden_layer_bias,
        output_layer_weights=network.output_layer_weights,
        output_layer_bias=network.output_layer_bias,
    )
    print('networ is get')
    total_error = network.total_error
    count = 0
    while total_error > epsilon:
        try:
            training_inputs, training_outputs = random.choice(network.training_sets)
            neural_network_data.train(training_inputs, training_outputs)
            outputs = neural_network_data.feed_forward(training_inputs)
            for i in range(len(outputs)):
                outputs[i] = round(outputs[i])
            if count == 1000:
                print(outputs, training_outputs)
                total_error = neural_network_data.calculate_total_error(network.training_sets)
                print('error = ', total_error)
                network_data = neural_network_data.inspect(network.training_sets)
                with open('network.json', 'w') as outfile:
                    json.dump(network_data, outfile)
                count = 0
            else:
                count += 1
        except Exception as error:
            print(error)
            network_data = neural_network_data.inspect(network.training_sets)
            with open('network.json', 'w') as outfile:
                json.dump(network_data, outfile)

    network_data = neural_network_data.inspect(network.training_sets)
    with open('network.json', 'w') as outfile:
        json.dump(network_data, outfile)
    print(json.dumps(network_data, sort_keys=True, indent=4, separators=(',', ': ')))
    print(neural_network_data.feed_forward(network.training_sets[0][0]))
    print('Total error: ', total_error)

def main(filepath='./ToTest/Kuindji_Raneural_network_datayy_vesna.jpg'):
    """Get image season"""
    size = 64, 64
    network = NetworkInfo()
    if network.is_read_file_error:
        return
    neural_network_data = neural_network.NeuralNetwork(
        num_inputs=network.num_inputs,
        num_hidden=network.num_hidden,
        num_outputs=network.num_outputs,
        hidden_layer_weights=network.hidden_layer_weights,
        hidden_layer_bias=network.hidden_layer_bias,
        output_layer_weights=network.output_layer_weights,
        output_layer_bias=network.output_layer_bias,
    )

    img = Image.open(filepath)
    img.show()
    img = img.convert(mode='RGB')
    img = img.resize(size, Image.ANTIALIAS)
    histogram = get_histogram(img, size)

    network_outputs = neural_network_data.feed_forward(histogram)
    answer_text = ['autumn', 'summer', 'spring', 'winter']
    print('network_outputs:')
    answer = []
    for indx, output in enumerate(network_outputs):
        print(answer_text[indx].title() + ':\t', output)
        if round(output) == 1:
            answer.append(indx)
    if len(answer) == 0:
        index = max_to_index(network_outputs)
        print('Season: maybe is a ', answer_text[index])
    elif len(answer) > 1:
        index = max_of_outputs_to_index(answer, network_outputs)
        print('Season: likely is a ', answer_text[index])
        for result in answer:
            if result != index:
                print('And it looks like a ', answer_text[result])
    else:
        print('Season is a ', answer_text[answer[0]])

def max_to_index(value):
    """@return index of max value"""
    max_value = 0
    index_of_max = 0
    for indx, output in enumerate(value):
        if output > max_value:
            max_value = output
            index_of_max = indx
    return index_of_max

def max_of_outputs_to_index(answer, network_outputs):
    """@return index of max value"""
    max_value = 0
    index_of_max = 0
    for output in answer:
        if network_outputs[output] > max_value:
            max_value = network_outputs[output]
            index_of_max = output
    return index_of_max

def helper():
    """View help info"""
    print('Usage: python main.py [-h] [-t] [-f]')
    print('-t, --train [error]        train neural-network or create new (standart error = 0.0001)')
    print('-f, --file [file_path]       get image season')

if __name__ == "__main__":
    try:
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            sys.exit(helper())
        if sys.argv[1] == '--file' or sys.argv[1] == '-f':
            try:
                sys.exit(main(sys.argv[2]))
            except IndexError as error:
                print(error)
                helper()
                sys.exit()
        if sys.argv[1] == '--train' or sys.argv[1] == '-t':
            try:
                sys.exit(train(sys.argv[2]))
            except IndexError:
                sys.exit(train())
    except IndexError:
        sys.exit(main())
