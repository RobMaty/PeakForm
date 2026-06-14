from django import forms
from .models import Plan


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'description', 'level', 'duration_weeks', 'price', 'is_free', 'image_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if len(description) < 20:
            raise forms.ValidationError('Description must be at least 20 characters long.')
        return description

    def clean_duration_weeks(self):
        weeks = self.cleaned_data.get('duration_weeks')
        if weeks is not None and (weeks < 1 or weeks > 52):
            raise forms.ValidationError('Duration must be between 1 and 52 weeks.')
        return weeks

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Price cannot be negative.')
        return price

    def clean(self):
        cleaned_data = super().clean()
        is_free = cleaned_data.get('is_free')
        price = cleaned_data.get('price')
        if is_free and price is not None and price > 0:
            raise forms.ValidationError('A free plan cannot have a price greater than $0.00.')
        if not is_free and (price is None or price == 0):
            cleaned_data['is_free'] = True
        return cleaned_data
