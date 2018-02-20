class Instance:
    # Add features to constructor
    def __init__(self, location, label):
        self.location = location
        self.label = label
    
    def __str__(self):
        return "(location: {}, label: {})".format(self.location, self.label)