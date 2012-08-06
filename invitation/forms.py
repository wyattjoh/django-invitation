from django import forms
from django.conf import settings
import re

invitation_blacklist = getattr(settings, 'INVITATION_BLACKLIST', ())

class InvitationKeyForm(forms.Form):
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        self.remaining_invitations = kwargs.pop('remaining_invitations', None)
        self.user_email = kwargs.pop('user_email', None)
        super(InvitationKeyForm, self).__init__(*args, **kwargs)        
    
    def clean(self):
        cleaned_data = super(InvitationKeyForm, self).clean()

        if self.remaining_invitations <= 0:
            raise forms.ValidationError("Sorry, you don't have any invitations left")
        
        if self.user_email == self.cleaned_data['email']:
            raise forms.ValidationError("You can't send an invitation to yourself")
        
        for email_match in invitation_blacklist:
            if re.search(email_match, self.cleaned_data['email']):
                raise forms.ValidationError("Thanks, but there's no need to invite us!")
        
        # Always return the cleaned data, whether you have changed it or
        # not.
        return cleaned_data
    