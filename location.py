class Location:
    def __init__(self, doc_num, line_num, char_num):
        self.doc_num = doc_num
        self.line_num = line_num
        self.char_num = char_num

    def __str__(self):
        return "[doc_num: {}, line_num: {}, char_num: {}]".format(self.doc_num, self.line_num, self.char_num)