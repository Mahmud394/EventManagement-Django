from django import forms
from .models import Event, Participant, Category

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border p-2 rounded w-full'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'border p-2 rounded w-full'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'border p-2 rounded w-full'}),
            'name': forms.TextInput(attrs={'class': 'border p-2 rounded w-full'}),
            'location': forms.TextInput(attrs={'class': 'border p-2 rounded w-full'}),
            'category': forms.Select(attrs={'class': 'border p-2 rounded w-full'}),
        }

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border p-2 rounded w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border p-2 rounded w-full'}),
            'events': forms.SelectMultiple(attrs={'class': 'border p-2 rounded w-full'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border p-2 rounded w-full'}),
            # 'description': forms.Textarea(attrs={'rows': 3, 'class': 'border p-2 rounded w-full'}),
        }
