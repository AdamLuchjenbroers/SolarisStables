from solaris.forms import SolarisModelForm
from solaris.cms.models import NewsPost

class NewsPostForm(SolarisModelForm):
    class Meta:
        model = NewsPost
        fields = ('title', 'content')
