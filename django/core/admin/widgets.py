from __future__ import unicode_literals

import re

from django.contrib.postgres.forms.array import SimpleArrayField
from django.forms.widgets import MultiWidget, TextInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class AdminArrayFieldWidget(MultiWidget):
    is_hidden = False
    input_class = TextInput
    outer_html = '<ul{id_attr} data-element-counter="{element_count}" class="arrayfield-list"' \
                 'style="padding: 0; margin: 0; display: none;">{content}{add_new}</ul>'
    inner_html = '<li style="list-style-type: none;">{widget}' \
                 '<a href="#" class="delete-arraywidget-item" style="color: #CC3434; padding-left: 8px">Delete</a></li>'
    add_new_html = '<li style="list-style-type: none;"><a href="#" class="add-arraywidget-item">Add new entry</a></li>'

    def __init__(self, input_widget, attrs=None):
        self.widget = input_widget
        super(AdminArrayFieldWidget, self).__init__([], attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if value:
            widget_count = len(value)
        else:
            widget_count = 1
        self.widgets = [self.widget for i in range(widget_count)]

        output = super(AdminArrayFieldWidget, self).render(name, value, attrs)

        return format_html(self.outer_html,
                           id_attr=format_html(' id="{}"', name) if name else '',
                           element_count=widget_count,
                           content=mark_safe(output),
                           add_new=format_html(self.add_new_html))

    def format_output(self, rendered_widgets):
        output = []
        for widget in rendered_widgets:
            output.append(format_html(self.inner_html,
                                      widget=widget))
        return '\n'.join(output)

    def value_from_datadict(self, data, files, name):
        pattern = re.compile(r'^{}_[0-9]+$'.format(name))
        data_keys = [key for key in data if pattern.match(key)]
        data_keys = sorted(data_keys, key=lambda x: int(x.split('_')[-1]))

        self.widgets = [self.widget for i in range(len(data_keys))]

        ret = []
        for i, key in enumerate(data_keys):
            widget = self.widgets[i]
            value = widget.value_from_datadict(data, files, key)
            if value:
                ret.append(value)
        return ret

    def decompress(self, value):
        """This is only to handle None"""
        if value is None:
            return []
        raise TypeError('Cannot handle type {}'.format(type(value).__name__))


class AdminArrayField(SimpleArrayField):
    widget = AdminArrayFieldWidget

    def __init__(self, *args, **kwargs):
        widget = self.widget(input_widget=kwargs['base_field'].widget)
        kwargs.setdefault('widget', widget)
        kwargs.setdefault('delimiter', '\x1f')
        super(AdminArrayField, self).__init__(*args, **kwargs)

    def prepare_value(self, value):
        return value

    def to_python(self, value):
        if value:
            value = self.delimiter.join(value)

        return super(AdminArrayField, self).to_python(value)


class NoneReadOnlyAdminArrayFieldWidget(AdminArrayFieldWidget):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            return mark_safe('-')
        return super(NoneReadOnlyAdminArrayFieldWidget, self).render(name, value, attrs)


class NoneReadOnlyAdminArrayField(AdminArrayField):
    widget = NoneReadOnlyAdminArrayFieldWidget
