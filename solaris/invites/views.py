from django.shortcuts import render
from invitations.views import SendInvite, AcceptInvite 

from solaris.views import SolarisViewMixin

class SolarisSendInvite(SolarisViewMixin, SendInvite):
    template_name='invites/send_invite.html'
    submit='Invite'

    def get_context_data(self, **kwargs):
        page_context = super(SolarisSendInvite, self).get_context_data(**kwargs)
        
        page_context['submit'] = 'Invite'
        return page_context

class SolarisAcceptInvite(SolarisViewMixin, SendInvite):
    template_name='invites/accept_invite.html'
