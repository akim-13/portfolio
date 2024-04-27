import numpy as np


class Layer:
    def __init__(self, num_of_inputs, num_of_neurons):
        self.weights = 0.01 * np.random.randn(num_of_inputs, num_of_neurons)
        self.biases = np.zeros((1, num_of_neurons))


    # I.e. update weights and biases for all connections with the previous layer.
    def forward_pass(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases
        return self.output


class ActivationFunction:
    def __init__(self, is_for_output_layer):
        self.is_for_output_layer = is_for_output_layer


    # I.e. update values of all neurons on the current level.
    def forward_pass(self, inputs):
        if self.is_for_output_layer:
            self.output = self.calc_sigmoid(inputs)
        else:
            self.output = self.calc_rectifier(inputs)

        return self.output

            
    # A.K.A. ReLU
    @staticmethod
    def calc_rectifier(inputs):
        return np.maximum(0, inputs)


    @staticmethod
    def calc_sigmoid(inputs):
        return 1 / (1 + np.exp(-inputs))
        

class SpamClassifier:
    def __init__(self, k):
        self.k = k
        features_data, labels_data = None, None


    def populate_features_and_labels(self, is_training_data):
        if is_training_data:
            dataset_filename = 'training_spam.csv'
        else:
            dataset_filename = 'test_spam.csv'

        dataset_relative_path = f'./data/{dataset_filename}'

        try:
            dataset = np.loadtxt(open(dataset_relative_path), delimiter=',').astype(int)
        except FileNotFoundError:
            print(f'ERROR: "{dataset_relative_path}" file not found.')
            return
        except:
            print(f'ERROR: improper contents or something is wrong with the file/permissions ("{dataset_relative_path}").')
            return


        self.labels_data = dataset[:, 0]
        self.features_data = dataset[:, 1:]

        print("Shape of the spam training data set:", dataset.shape)
        print(dataset)
        print("Shape of labels_data:", self.labels_data.shape)
        print(self.labels_data)
        print("Shape of features_data:", self.features_data.shape)
        print(self.features_data)
        

    def generate_batches_of_size(self, batch_size):
        num_of_inputs = self.features_data.shape[0]
        indices = np.arange(num_of_inputs)
        np.random.shuffle(indices)

        features_data_shuffled = self.features_data[indices]
        labels_data_shuffled = self.labels_data[indices]

        for i in range(0, num_of_inputs, batch_size):
            features_data_batch = features_data_shuffled[i:i + batch_size]
            labels_data_batch = labels_data_shuffled[i:i + batch_size]
            yield (features_data_batch, labels_data_batch)


    def train(self):
        self.populate_features_and_labels(True)
        num_of_inputs = np.shape(self.features_data)[1]
        # A.K.A. the number of neurons in the first hidden layer.
        num_of_outputs_1 = 32
        hidden_layer_1 = Layer(num_of_inputs, num_of_outputs_1)
        activation_function_1 = ActivationFunction(False)

        # Cut the number of neurons in half in the second layer to prevent overfitting.
        num_of_outputs_2 = int(num_of_outputs_1 / 2)
        hidden_layer_2 = Layer(num_of_outputs_1, num_of_outputs_2)
        activation_function_2 = ActivationFunction(False)

        output_layer = Layer(num_of_outputs_2, 1)
        activation_function_output = ActivationFunction(True)

        # The size of batches should be a multiple of the number of inputs
        # to prevent the last batch from being smaller than the rest!
        for features_data_batch, labels_data_batch in self.generate_batches_of_size(20):
            # Pass through the 1st hidden layer.
            hidden_layer_1.forward_pass(features_data_batch)
            activation_function_1.forward_pass(hidden_layer_1.output)

            # Pass through the 2nd hidden layer.
            hidden_layer_2.forward_pass(activation_function_1.output)
            activation_function_2.forward_pass(hidden_layer_2.output)

            # Pass through the output layer.
            output_layer.forward_pass(activation_function_2.output)
            activation_function_output.forward_pass(output_layer.output)

            print('First outputs are:')
            print(activation_function_output.output[:20])
            print()
        

    def predict(self, data):
        self.populate_features_and_labels(False)
        return np.zeros(data.shape[0])

    
def create_classifier():
    classifier = SpamClassifier(k=1)
    classifier.train()
    return classifier


def main():
    classifier = create_classifier()

if __name__ == "__main__":
    main()
