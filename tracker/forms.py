from django import forms
from .models import SocialPost, PostMetric, DailyLog


class SocialPostForm(forms.ModelForm):
    class Meta:
        model = SocialPost
        fields = ['title', 'platform', 'post_type', 'status', 'caption', 'tags', 'scheduled_at', 'published_at', 'post_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. How we scaled to 50k MAU'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'post_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your copy, hooks, and call-to-actions here...'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'growth, saas, indiehacker, tech'}),
            'scheduled_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'published_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'post_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/p/...'}),
        }


class PostMetricForm(forms.ModelForm):
    class Meta:
        model = PostMetric
        fields = ['metric_date', 'source', 'views', 'likes', 'comments', 'shares', 'saves', 'clicks', 'reach', 'impressions', 'notes']
        widgets = {
            'metric_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'views': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'likes': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'comments': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'shares': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'saves': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'clicks': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'reach': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'impressions': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notes on spike, algorithm behavior, etc.'}),
        }


class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = ['log_date', 'focus_area', 'content_items_created', 'hours_spent', 'productivity_score', 'key_learnings', 'notes']
        widgets = {
            'log_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'focus_area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Video Production & Scripting'}),
            'content_items_created': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'hours_spent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0'}),
            'productivity_score': forms.Select(choices=[(i, f"{i} / 5 Stars") for i in range(1, 6)], attrs={'class': 'form-select'}),
            'key_learnings': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Key takeaways from content performance today'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'General observations'}),
        }
