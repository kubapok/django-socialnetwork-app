from django import forms

from .models import *

class FriendshipRequestForm(forms.ModelForm):
    class Meta:
        model = FriendshipRequest
        fields = ('requested',)



class RespondToRequestsForm(forms.ModelForm):
    class Meta:
        model = FriendshipRequest
        fields = ('answer',)


class connectionsForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    class Meta:
        fields = ('user',)
