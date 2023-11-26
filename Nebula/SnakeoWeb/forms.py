from django import forms

class LobbyCreationForm(forms.Form):
    title = forms.CharField(label="lobby title", max_length=30)
