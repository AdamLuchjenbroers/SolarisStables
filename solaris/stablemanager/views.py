from genshi import Markup
from solaris.core import render_page

def stable_main(request):
    body = Markup('<P>Stable Management will go here</P>')
    return render_page(body=body, selected=None, request=request)


def stable_registration(request):
    body = Markup('<P>This will become a Stable Registration Page</P>')
    return render_page(body=body, selected=None, request=request)
