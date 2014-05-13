from solaris.forms import SolarisModelForm
from solaris.cms.models import NewsPost

class NewsPostForm(SolarisModelForm):
	pass

	class Meta:
		model = NewsPost