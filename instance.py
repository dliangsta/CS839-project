class Instance:
    # Add features to constructor
    def __init__(self, location, word, label, features):
        self.location = location
        self.word = word
        self.lowered_word = word.lower()
        # Only aphabetic characters of word
        self.stripped_word = ''.join([char for char in word if char.isalpha() or char.isdigit()])
        self.stripped_lowered_word = self.stripped_word.lower()
        self.label = label
        self.features = features
        
    def __str__(self):
        return "(location: {}, word: '{}', stripped_word: '{}', label: {})".format(self.location, self.word, self.stripped_word, self.label, self.features)