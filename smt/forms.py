from django import forms
from django.utils.html import format_html


class UploadTextFileForm(forms.Form):
    file = forms.FileField()


class MyInput(forms.widgets.CheckboxChoiceInput):

    def render(self, name=None, value=None, attrs=None, choices=()):
        if self.id_for_label:
            label_for = format_html(u' for="{0}"', self.id_for_label)
        else:
            label_for = u''
        return format_html(u'{1}<label{0}> {2}</label> <input type="number" value="0" name="iter_num[{3}]">', label_for, self.tag(), self.choice_label, self.choice_value )


class MyRenderer(forms.widgets.CheckboxFieldRenderer):
    choice_input_class = MyInput


class MySelect(forms.widgets.CheckboxSelectMultiple):

    renderer = MyRenderer
    _empty_value = []


class IBMModelOptions(forms.Form):
    options = (
    ('1', 'IBM1'),
    ('2', 'IBM2'),
    ('3', 'IBM3'),
    ('4', 'IBM4'),
    ('5', 'IBM5'),
    ('6', 'IBM6'), )

    models = forms.MultipleChoiceField(widget=MySelect, choices=options, initial=options[0])

    def get_html_input_dict(self, query_dict, param):
        import re
        dictionary = {}
        regex = re.compile('%s\[([\w\d_]+)\]' % param)
        for key, value in query_dict.items():
            match = regex.match(key)
            if match:
                inner_key = match.group(1)
                dictionary[inner_key] = value

        return dictionary

    def clean(self):
        result = super(IBMModelOptions, self).clean()
        numbers = self.get_html_input_dict(self.data, "iter_num")
        selected_models = result['models']
        models_with_numbers = {}
        for model in selected_models:
            models_with_numbers[model] = int(numbers[model])
        result['models'] = models_with_numbers
        return result
