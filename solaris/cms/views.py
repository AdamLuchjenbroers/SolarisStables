# -*- coding: iso-8859-1 -*-
from genshi import Markup
from solaris.cms.models import StaticContent
from solaris.core import render_page
from django.shortcuts import get_object_or_404


def static_content(request, selected='>'):
    # Derive body text
    content = get_object_or_404(StaticContent, url='/%s' % selected).content
    body = Markup(content)
    
    return render_page(body=body, selected=selected)
        
