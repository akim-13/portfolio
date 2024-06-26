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


    def update_params(self, learning_rate=1.0):
        # Update parameters using Stochastic Gradient Descent.
        self.weights -= learning_rate * self.weights_grad
        self.biases -= learning_rate * self.biases_grad


class ActivationFunction:
    def __init__(self, is_for_output_layer):
        self.is_for_output_layer = is_for_output_layer


    def forward_pass(self, inputs):
        self.inputs = inputs
        if self.is_for_output_layer:
            self.output = self._calc_sigmoid(inputs)
        else:
            self.output = self._calc_rectifier(inputs)

        return self.output


    def backward_pass(self, output_grad):
        if self.is_for_output_layer:
            self.gradient = output_grad * self._calc_sigmoid_derivative(self.output)
        else:
            self.gradient = output_grad * self._calc_rectifier_derivative(self.inputs)
        return self.gradient
            

    @staticmethod
    def _calc_rectifier(inputs):
        return np.maximum(0, inputs)


    @staticmethod
    def _calc_rectifier_derivative(inputs):
        derivative = np.array(inputs, copy=True)
        derivative[inputs <= 0] = 0
        derivative[inputs > 0] = 1
        return derivative


    @staticmethod
    def _calc_sigmoid(inputs):
        return 1 / (1 + np.exp(-inputs))


    @staticmethod
    def _calc_sigmoid_derivative(output):
        return output * (1 - output)


class MeanSquaredErrorLoss:
    def forward_pass(self, predictions, labels):
        labels = labels.reshape(-1, 1)
        loss = np.mean((predictions - labels) ** 2)
        return loss


    def backward_pass(self, predictions, labels):
        labels = labels.reshape(-1, 1)
        gradient = 2 * (predictions - labels) / len(labels)
        return gradient


class SpamClassifier:
    def train(self, filename):
        self._populate_features_and_labels(True)
        setup = self._set_up(32)

        batch_size = 50
        num_of_epochs = 1500
        for epoch in range(num_of_epochs + 1):

            total_loss, total_correct = self._go_through_epoch(setup, batch_size)

            if epoch % 100 == 0:
                total_samples = len(self.labels_of_samples)
                num_of_batches = total_samples / batch_size
                mean_epoch_loss = total_loss / num_of_batches
                epoch_accuracy = total_correct / total_samples
                print('='*20 + f' EPOCH {epoch} ' + '='*20+'\n')
                print(f'LOSS: {mean_epoch_loss:.4f}')
                print(f'ACC : {epoch_accuracy:.4f} ({total_correct}/{total_samples})\n')

        print('='*52 + '\n\nTraining completed.')

        layers = setup[0]
        self._save_model(layers, filename)
        print('Model parameters saved successfully.\n')


    def predict(self, filename):
        self._populate_features_and_labels(False)
        setup = self._set_up(32)
        layers = setup[0]
        activation_functions = setup[1]

        self._load_model(layers, filename)

        print('Model parameters loaded successfully.\nTesting...', end=' ')

        # Forward pass.
        neuron_activations = self.samples
        for layer, activation_function in zip(layers, activation_functions):
            neuron_activations = layer.forward_pass(neuron_activations)
            neuron_activations = activation_function.forward_pass(neuron_activations)

        print('Done.\n')

        loss = MeanSquaredErrorLoss().forward_pass(neuron_activations, self.labels_of_samples)
        predicted_labels = (neuron_activations > 0.5).astype(int)
        correct_predictions = (predicted_labels == self.labels_of_samples.reshape(-1, 1)).sum()
        accuracy = correct_predictions / len(self.labels_of_samples)

        print(f'Loss: {loss:.3f}')
        print(f'Accuracy: {accuracy*100:.2f}%')


    def _populate_features_and_labels(self, is_training_data):
        if is_training_data:
            dataset_filename = 'training_spam.csv'
        else:
            dataset_filename = 'testing_spam.csv'

        dataset_relative_path = f'./data/{dataset_filename}'

        try:
            dataset = np.loadtxt(open(dataset_relative_path), delimiter=',').astype(int)
        except FileNotFoundError:
            print(f'ERROR: "{dataset_relative_path}" file not found.')
            return
        except:
            print(f'ERROR: improper contents or something is wrong with the file/permissions ("{dataset_relative_path}").')
            return

        self.labels_of_samples = dataset[:, 0]
        self.samples = dataset[:, 1:]


    def _set_up(self, num_of_neurons_in_first_hidden_layer):
        num_of_inputs = np.shape(self.samples)[1]

        hidden_layer_1 = Layer(num_of_inputs, num_of_neurons_in_first_hidden_layer)
        activation_function_1 = ActivationFunction(False)

        hidden_layer_2 = Layer(num_of_neurons_in_first_hidden_layer, int(num_of_neurons_in_first_hidden_layer/2))  
        activation_function_2 = ActivationFunction(False)
        
        output_layer = Layer(int(num_of_neurons_in_first_hidden_layer/2), 1)  
        activation_function_output = ActivationFunction(True)

        layers = [ hidden_layer_1, hidden_layer_2, output_layer ]
        activation_functions = [ activation_function_1, activation_function_2, activation_function_output ]

        return layers, activation_functions


    def _go_through_epoch(self, setup, batch_size):
        hidden_layer_1, hidden_layer_2, output_layer = setup[0]
        activation_function_1, activation_function_2, activation_function_output = setup[1]

        total_loss = 0
        total_correct = 0

        for samples_batch, labels_of_samples_batch in self._generate_batches_of_size(batch_size):
            # Forward pass.
            output1 = hidden_layer_1.forward_pass(samples_batch)
            activated_output1 = activation_function_1.forward_pass(output1)

            output2 = hidden_layer_2.forward_pass(activated_output1)
            activated_output2 = activation_function_2.forward_pass(output2)

            final_output = output_layer.forward_pass(activated_output2)
            predictions = activation_function_output.forward_pass(final_output)

            # Calculate loss.
            batch_loss = MeanSquaredErrorLoss().forward_pass(predictions, labels_of_samples_batch)
            total_loss += batch_loss

            # Calculate accuracy.
            predicted_labels = (predictions > 0.5).astype(int)
            correct_predictions = (predicted_labels == labels_of_samples_batch.reshape(-1, 1)).sum()
            total_correct += correct_predictions

            # Backward pass.
            loss_gradient = MeanSquaredErrorLoss().backward_pass(predictions, labels_of_samples_batch)

            grad_output = activation_function_output.backward_pass(loss_gradient)
            grad_layer_out = output_layer.backward_pass(grad_output)

            grad_activation_2 = activation_function_2.backward_pass(grad_layer_out)
            grad_layer_2 = hidden_layer_2.backward_pass(grad_activation_2)

            grad_activation_1 = activation_function_1.backward_pass(grad_layer_2)
            grad_layer_1 = hidden_layer_1.backward_pass(grad_activation_1)

            # Update weights and biases.
            learning_rate = 0.03
            hidden_layer_1.update_params(learning_rate)
            hidden_layer_2.update_params(learning_rate)
            output_layer.update_params(learning_rate)

        return total_loss, total_correct


    def _generate_batches_of_size(self, batch_size):
        num_of_inputs = self.samples.shape[0]
        indices = np.arange(num_of_inputs)
        np.random.shuffle(indices)

        samples_shuffled = self.samples[indices]
        labels_of_samples_shuffled = self.labels_of_samples[indices]

        for i in range(0, num_of_inputs, batch_size):
            samples_batch = samples_shuffled[i:i + batch_size]
            labels_of_samples_batch = labels_of_samples_shuffled[i:i + batch_size]
            yield (samples_batch, labels_of_samples_batch)


    @staticmethod
    def _save_model(layers, filename='model_parameters.npz'):
        data_dict = {}
        for i, layer in enumerate(layers):
            data_dict[f'weights_{i}'] = layer.weights
            data_dict[f'biases_{i}'] = layer.biases

        try:
            np.savez(filename, **data_dict)
        except:
            print(f'ERROR: Something went wrong while saving the file "{filename}".')


    @staticmethod
    def _load_model(layers, filename='model_parameters.npz'):
        try:
            data = np.load(filename)
        except:
            print(f'ERROR: Something went wrong while loading the file "{filename}".')

        for i, layer in enumerate(layers):
            layer.weights = data[f'weights_{i}']
            layer.biases = data[f'biases_{i}']


def main():
    # SpamClassifier().train('./data/spam_classifier_parameters.npz')
    SpamClassifier().predict('./data/93_percent_parameters.npz')


if __name__ == "__main__":
    main()

