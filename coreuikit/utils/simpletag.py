__author__ = ('Imam Omar Mochar', ('iomarmochtar@gmail.com',))

"""
Simple XML builder, i create it for generating HTML tag(s)
"""

from django.utils.safestring import mark_safe

# alternative of xml attribute that also become keyword in python side
ALTERNATE_MAP = {
    'klass': 'class'
}


class Tag(object):
    name = None

    def __init__(self, name):
        self.name = name

    def __call__(self, *contents, **attrs):
        h_attrs = []

        for k, v in attrs.items():
            if k in ALTERNATE_MAP:
                k = ALTERNATE_MAP[k]
            h_attrs.append('{}="{}"'.format(k,v))

        content = '<{tagname}{h_attrs}>{contents}</{tagname}>'.format(
                    tagname=self.name,
                    contents=' '.join(contents) if contents else '',
                    h_attrs=' {}'.format(' '.join(h_attrs)) if h_attrs else ''
                )

        is_safe = attrs.get('is_safe', False)
        return content if not is_safe else mark_safe(content)


class IntheMiddle(object):
    """
    Bridging to Tag class
    """

    def __getattribute__(self, name):
        node = Tag(name)
        return node


class Helpers(object):

    @classmethod
    def components(self, *args, **kwargs):
        separator = kwargs.get('separator', '&nbsp;')
        return mark_safe(
            separator.join(args)
        )


SimpleTag = IntheMiddle()