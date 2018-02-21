class Instance:
    # Add features to constructor
    def __init__(self, location, label, features):
        self.location = location
        self.label = label
        self.features = features
        
    def __str__(self):
        return "(location: {}, label: {})".format(self.location, self.label)