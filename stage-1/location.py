class Location:
    def __init__(self, doc_num, line_num, start, end):
        self.doc_num = doc_num
        self.line_num = line_num
        self.start = start
        self.end = end

    def __str__(self):
        return "[doc_num: {}, line_num: {}, start: {}, end: {}]".format(self.doc_num, self.line_num, self.start, self.end)