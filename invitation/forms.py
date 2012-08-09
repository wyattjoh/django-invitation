from django import forms
from django.conf import settings
import re


class InvitationKeyForm(forms.Form):
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        self.remaining_invitations = kwargs.pop('remaining_invitations', None)
        self.user_email = kwargs.pop('user_email', None)
        self.invitation_blacklist = getattr(settings, 'INVITATION_BLACKLIST', ())
    
        super(InvitationKeyForm, self).__init__(*args, **kwargs)        
    
    def clean(self):
        cleaned_data = super(InvitationKeyForm, self).clean()

        if self.remaining_invitations <= 0:
            raise forms.ValidationError("Sorry, you don't have any invitations left")
        
        if 'email' in self.cleaned_data:
            if self.user_email == self.cleaned_data['email']:
                self._errors['email'] = self.error_class([u"You can't send an invitation to yourself"])
                del cleaned_data['email']
            
        if 'email' in self.cleaned_data:    
            for email_match in self.invitation_blacklist:
                if re.search(email_match, self.cleaned_data['email']) is not None:
                    self._errors['email'] = self.error_class([u"Thanks, but there's no need to invite us!"])
                    del cleaned_data['email']
                    break
        
        # Always return the cleaned data, whether you have changed it or
        # not.
        return cleaned_data
    