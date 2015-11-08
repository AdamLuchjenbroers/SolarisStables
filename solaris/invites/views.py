from django.forms.forms import NON_FIELD_ERRORS

from invitations.views import SendInvite, AcceptInvite 
from solaris.views import SolarisViewMixin

class SolarisSendInvite(SolarisViewMixin, SendInvite):
    template_name='invites/send_invite.html'
    submit='Invite'

    def get_context_data(self, **kwargs):
        page_context = super(SolarisSendInvite, self).get_context_data(**kwargs)
        
        print "Dumping KWARGS"
        for (key, value) in kwargs.iteritems():
            print "%s => %s" % (key, value)
        
        if 'success_message' in kwargs:
            page_context['success_message'] = kwargs['success_message']
            
        page_context['submit'] = 'Invite'
        return page_context
    
    def form_invalid(self, form):
        form._errors[NON_FIELD_ERRORS] = form.error_class(['An error was encountered while sending the invite'])
        return super(SolarisSendInvite, self).form_invalid(form)

class SolarisAcceptInvite(SolarisViewMixin, AcceptInvite):
    template_name='invites/accept_invite.html'
    submit='Accept'
    
    def get_context_data(self, **kwargs):
        page_context = super(SolarisSendInvite, self).get_context_data(**kwargs)
        
        page_context['submit'] = 'Invite'
        return page_context
