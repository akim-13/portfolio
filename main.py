import numpy as np


class Layer:
    def __init__(self, num_of_inputs, num_of_neurons):
        self.weights = 0.01 * np.random.randn(num_of_inputs, num_of_neurons)
        self.biases = np.zeros((1, num_of_neurons))


    def forward_pass(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases
        return self.output


class ActivationFunction:
    def __init__(self, inputs, is_for_hidden_layer=True):
        self.inputs = inputs

        if is_for_hidden_layer:
            self.output = self.activate_rectifier()
        else:
            self.output = self.activate_sigmoid()

            
    # A.K.A. ReLU
    def activate_rectifier(self):
        return np.maximum(0, self.inputs)


    def activate_sigmoid(self):
        return 1 / (1 + np.exp(-self.inputs))
        

class SpamClassifier:
    def __init__(self, k):
        self.k = k
        features, labels = None, None


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

        self.labels = dataset[:, 0]
        self.features = dataset[:, 1:]

        print("Shape of the spam training data set:", dataset.shape)
        print(dataset)
        print("Shape of labels:", self.labels.shape)
        print(self.labels)
        print("Shape of features:", self.features.shape)
        print(self.features)

        
    def train(self):
        self.populate_features_and_labels(True)
        # first_layer = Layer
        # Unsure whether it's supposed to be self.features here.
        ActivationFunction(self.features, False)
        

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
