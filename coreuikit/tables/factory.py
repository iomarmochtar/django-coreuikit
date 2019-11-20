import django_tables2 as tables
from .grid import GridList


def table_class_factory(model,
                        model_fields='__all__',
                        fields_class={},
                        template_name='django_tables2/bootstrap4.html',
                        table_attr='table table-responsive-sm table-bordered table-striped table-hover'
                        ):
    """Generate django-tables2 class

    :param model:
    :param model_fields:
    :return:
    """
    attrs = {
        'model': model,
        'template_name': template_name,
        'fields': model_fields,
        'attrs': {'class': table_attr}
    }
    Meta = type('Meta', (), attrs)
    class_name = '{}TableClassFactory'.format(model.__name__)
    table_class_attr = {
        'Meta': Meta
    }
    for name, cls in fields_class.items():
        table_class_attr[name] = cls
    return type(class_name, (GridList,), table_class_attr)
