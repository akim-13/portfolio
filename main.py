import numpy as np

class Layer:
    def __init__(self, num_of_inputs, num_of_neurons):
        self.weights = 0.01 * np.random.randn(num_of_inputs, num_of_neurons)
        self.biases = np.zeros((1, num_of_neurons))

    def forward_pass(self, inputs):
        self.inputs = inputs
        self.output = np.dot(inputs, self.weights) + self.biases
        return self.output

    def backward_pass(self, output_grad):
        # Gradient on parameters.
        self.weights_grad = np.dot(self.inputs.T, output_grad)
        self.biases_grad = np.sum(output_grad, axis=0, keepdims=True)

        # Gradient on input values to pass to the previous layer.
        self.input_grad = np.dot(output_grad, self.weights.T)
        return self.input_grad

    def update_params(self, learning_rate):
        # Update parameters using gradients and learning rate.
        self.weights -= learning_rate * self.weights_grad
        self.biases -= learning_rate * self.biases_grad


class BinaryCrossEntropyLoss:
    def forward_pass(self, predictions, labels):
        # Clip values to avoid log(0) and log(1) in the denominator.
        predictions = np.clip(predictions, 1e-12, 1 - 1e-12)
        # A known formula.
        loss = -np.mean(labels * np.log(predictions) + (1 - labels) * np.log(1 - predictions))
        return loss


    def backward_pass(self, predictions, labels):
        predictions = np.clip(predictions, 1e-12, 1 - 1e-12)
        # Ensure that `labels` is a column vector.
        labels = labels.reshape(-1, 1)
        # A known formula.
        self.gradient = (-(labels / predictions) + (1 - labels) / (1 - predictions)) / len(predictions)
        return self.gradient


class ActivationFunction:
    def __init__(self, is_for_output_layer):
        self.is_for_output_layer = is_for_output_layer


    def forward_pass(self, inputs):
        self.inputs = inputs
        if self.is_for_output_layer:
            self.output = self.calc_sigmoid(inputs)
        else:
            self.output = self.calc_rectifier(inputs)
        return self.output


    def backward_pass(self, derivative_values):
        if self.is_for_output_layer:
            self.gradient = derivative_values * self.calc_sigmoid_derivative(self.output)
        else:
            self.gradient = derivative_values * self.calc_rectifier_derivative(self.inputs)
        return self.gradient
            

    @staticmethod
    def calc_rectifier(inputs):
        return np.maximum(0, inputs)


    @staticmethod
    def calc_rectifier_derivative(inputs):
        derivative = np.array(inputs, copy=True)
        derivative[inputs <= 0] = 0
        derivative[inputs > 0] = 1
        return derivative


    @staticmethod
    def calc_sigmoid(inputs):
        return 1 / (1 + np.exp(-inputs))


    @staticmethod
    def calc_sigmoid_derivative(output):
        return output * (1 - output)


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

        # print("Shape of the spam training data set:", dataset.shape)
        # print(dataset)
        # print("Shape of labels_data:", self.labels_data.shape)
        # print(self.labels_data)
        # print("Shape of features_data:", self.features_data.shape)
        # print(self.features_data)
        

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
        learning_rate = 0.01

        hidden_layer_1 = Layer(num_of_inputs, 32)
        activation_function_1 = ActivationFunction(False)

        # Assuming the previous layer has 32 neurons.
        hidden_layer_2 = Layer(32, 16)  
        activation_function_2 = ActivationFunction(False)
        
        # Output layer for binary classification.
        output_layer = Layer(16, 1)  
        activation_function_output = ActivationFunction(True)

        total_loss = 0
        num_of_batches = 0

        for features_data_batch, labels_data_batch in self.generate_batches_of_size(20):

            # Forward pass.
            output1 = hidden_layer_1.forward_pass(features_data_batch)
            activated_output1 = activation_function_1.forward_pass(output1)

            output2 = hidden_layer_2.forward_pass(activated_output1)
            activated_output2 = activation_function_2.forward_pass(output2)

            final_output = output_layer.forward_pass(activated_output2)
            predictions = activation_function_output.forward_pass(final_output)


            # Calculate loss.
            batch_loss = BinaryCrossEntropyLoss().forward_pass(predictions, labels_data_batch)
            total_loss += batch_loss
            num_of_batches += 1

            if num_of_batches % 10 == 0:
                print(f'Batch number {num_of_batches}')
                print(f'Features batch {np.shape(features_data_batch)}:\n{features_data_batch}\n')
                print(f'Labels batch {np.shape(labels_data_batch)}:\n{labels_data_batch}\n')
                print(f'Predictions {np.shape(predictions)}:\n {predictions}\n')
                print(f'Batch loss: {batch_loss}\n')


            # FIXME: The problems start from here(ish). 
            # Backward pass.
            loss_gradient = BinaryCrossEntropyLoss().backward_pass(predictions, labels_data_batch)

            # print(f'Loss gradient {np.shape(loss_gradient)}:\n {loss_gradient}\n')

            grad_output = activation_function_output.backward_pass(loss_gradient)

            grad_layer_out = output_layer.backward_pass(grad_output)
            output_layer.update_params(learning_rate)

            grad_activation_2 = activation_function_2.backward_pass(grad_layer_out)
            grad_layer_2 = hidden_layer_2.backward_pass(grad_activation_2)
            hidden_layer_2.update_params(learning_rate)

            grad_activation_1 = activation_function_1.backward_pass(grad_layer_2)
            grad_layer_1 = hidden_layer_1.backward_pass(grad_activation_1)
            hidden_layer_1.update_params(learning_rate)

            

        mean_epoch_loss = total_loss / num_of_batches
        print(f'Mean epoch loss: {mean_epoch_loss}')


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
