from django.forms import ModelForm
from solaris.cms.models import NewsPost

from markitup.widgets import MarkItUpWidget

class NewsPostForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewsPostForm, self).__init__(*args, **kwargs)
        
        self.fields['content'].widget = MarkItUpWidget() 

    class Meta:
        model = NewsPost
        fields = ('title', 'content')
