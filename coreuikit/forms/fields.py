
class TextInlineFieldMixin(object):

    display = None

    def __init__(self, display=None, *args, **kwargs):
        kwargs['label'] = ''
        self.display = display
        return super().__init__(*args, **kwargs)
