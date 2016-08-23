from django.forms.widgets import ClearableFileInput

class StableImageInput(ClearableFileInput):
    template_with_initial = '<div>%(clear_template)s</div><div><label>%(input_text)s:</label> %(input)s</div>'
    template_with_clear = '<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s:</label> %(clear)s'

