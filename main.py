# This skeleton code simply classifies every input as ham
#
# Here you can see there is a parameter k that is unused, the
# point is to show you how you could set up your own. You might
# also pass in extra data via a train method (also does nothing
# here). Modify this code as much as you like so long as the 
# accuracy test in the cell below runs.

class SpamClassifier:
    def __init__(self, k):
        self.k = k
        
    def train(self):
        pass
        
    def predict(self, data):
        return np.zeros(data.shape[0])
    

def create_classifier():
    classifier = SpamClassifier(k=1)
    classifier.train()
    return classifier

classifier = create_classifier()
