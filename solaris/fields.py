from django.forms import fields, widgets

class TonnageField(fields.IntegerField):
    def __init__(self, min_value=20, max_value=100, *args, **kwargs):
        super(TonnageField, self).__init__(min_value=min_value, max_value=max_value, *args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(TonnageField, self).widget_attrs(widget)
        if isinstance(widget, widgets.NumberInput):
            attrs['step'] = 5

        return attrs  
