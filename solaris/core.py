# -*- coding: iso-8859-1 -*-
# ------------------------------------------------------------
# Common functions that are useful in many places
# ------------------------------------------------------------

from .views import SolarisView

def render_page(body='', selected='', adminbar=False, request=None):
    # Use SolarisView to perform rendering
    # Slightly clunky, but it consolidates the code
    view = SolarisView(body=body, selected=selected)
    
    return view.get(request)
  
