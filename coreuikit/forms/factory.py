from collections import OrderedDict
from .search import CharField


def form_factory(form_class, fields, fields_class={}):
    attrs = OrderedDict()

    for field in fields:
        # default to chartfield
        attrs[field] = fields_class.get(field,
                CharField(
                    display=' '.join([x.capitalize() for x in field.split('_')])
                )
            )

    class_name = '{}ClassFactory'.format(form_class.__name__)
    return type(class_name, (form_class,), attrs)
