class Instance:
    # Add features to constructor
    def __init__(self, location, word, label, features):
        self.location = location
        self.word = word
        self.label = label
        self.features = features
        
    def __str__(self):
        return "(location: {}, word: {}, label: {}, features: {})".format(self.location, self.word, self.label, self.features)