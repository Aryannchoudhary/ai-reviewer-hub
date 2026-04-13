from django import forms
from .models import CodeReview

class CodeReviewForm(forms.ModelForm):
    class Meta:
        model = CodeReview
        fields = ['language', 'code']
        widgets = {
    'language': forms.Select(choices=CodeReview.LANGUAGE_CHOICES, attrs={'class': 'form-control'}),
            'code': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Paste your code here...'
            }),
        }

from .models import CodeSubmission

class CodeSubmissionForm(forms.ModelForm):
    class Meta:
        model = CodeSubmission
        fields = ['language', 'code']
        widgets = {
            'language': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Paste your code here...'
            }),
        }