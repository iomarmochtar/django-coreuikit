from string import punctuation

trans_table = str.maketrans('', '', punctuation)


class Helper(object):

    @classmethod
    def convert_flat(self, text):
        name = text.translate(trans_table)
        return '_'.join(name.split()).lower()
