from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    rate = forms.TypedChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Comment
        fields = ['text', 'rate']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Izoh yozing...'}),
        }
