class Location:
    def __init__(self, doc_num, start):
        self.doc_num = doc_num
        self.start = start

    def __str__(self):
        return "[doc_num: {}, start: {}]".format(self.doc_num, self.start)