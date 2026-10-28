import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from tracker.models import SocialPost, PostMetric, DailyLog
from analytics.models import PlayStoreMetric, GrowthGoal


@login_required
def dashboard_index_view(request):
    """
    Primary SaaS executive overview: KPIs, charts, active goals, recent content.
    """
    user = request.user
    today = timezone.now().date()

    # Core KPIs
    total_posts = SocialPost.objects.filter(user=user).count()
    published_posts = SocialPost.objects.filter(user=user, status='published').count()
    scheduled_posts = SocialPost.objects.filter(user=user, status='scheduled').count()

    total_views = PostMetric.objects.filter(post__user=user).aggregate(total=Sum('views'))['total'] or 0
    total_installs = PlayStoreMetric.objects.filter(user=user).aggregate(total=Sum('store_listing_acquisitions'))['total'] or 0

    # Active Goals
    active_goals = GrowthGoal.objects.filter(user=user, status='active').order_by('deadline')[:4]

    # Recent Posts
    recent_posts = SocialPost.objects.filter(user=user).order_by('-created_at')[:5]

    # Today's daily log
    today_log = DailyLog.objects.filter(user=user, log_date=today).first()

    # Views Trend (last 7 metrics snapshots across user's content)
    recent_metrics = PostMetric.objects.filter(post__user=user).order_by('metric_date')[:10]
    trend_labels = [m.metric_date.strftime('%b %d') for m in recent_metrics]
    trend_views = [m.views for m in recent_metrics]
    trend_eng = [m.total_engagement for m in recent_metrics]

    return render(request, 'dashboard/index.html', {
        'total_posts': total_posts,
        'published_posts': published_posts,
        'scheduled_posts': scheduled_posts,
        'total_views': total_views,
        'total_installs': total_installs,
        'active_goals': active_goals,
        'recent_posts': recent_posts,
        'today_log': today_log,
        'trend_labels': json.dumps(trend_labels),
        'trend_views': json.dumps(trend_views),
        'trend_eng': json.dumps(trend_eng),
    })


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)
