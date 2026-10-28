from django import forms
from .models import PlayStoreMetric, GrowthGoal


class PlayStoreMetricForm(forms.ModelForm):
    class Meta:
        model = PlayStoreMetric
        fields = [
            'app_name', 'package_name', 'metric_date', 'source',
            'store_listing_visitors', 'store_listing_acquisitions',
            'uninstalls', 'active_devices', 'average_rating', 'notes'
        ]
        widgets = {
            'app_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skyniya Growth App'}),
            'package_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'com.skyniya.growth'}),
            'metric_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'store_listing_visitors': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'store_listing_acquisitions': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'uninstalls': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'active_devices': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'average_rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1.0', 'max': '5.0'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Experiments, ASO keywords, icon changes'}),
        }


class GrowthGoalForm(forms.ModelForm):
    class Meta:
        model = GrowthGoal
        fields = [
            'title', 'metric_type', 'target_value', 'current_value',
            'unit', 'start_date', 'deadline', 'status', 'notes'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 50,000 TikTok Followers'}),
            'metric_type': forms.Select(attrs={'class': 'form-select'}),
            'target_value': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'views, installs, %'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Key strategy or sprint plan'}),
        }
