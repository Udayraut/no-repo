import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from .models import PlayStoreMetric, GrowthGoal
from .forms import PlayStoreMetricForm, GrowthGoalForm
from tracker.models import SocialPost, PostMetric


@login_required
def analytics_overview_view(request):
    """
    Main Analytics Dashboard: Platform breakdowns, growth trends, charts.
    """
    user = request.user

    # Aggregate social post views by platform
    platforms = ['instagram', 'youtube', 'twitter', 'tiktok', 'linkedin', 'facebook']
    platform_data = {}
    
    for p in platforms:
        posts = SocialPost.objects.filter(user=user, platform=p)
        count = posts.count()
        views = PostMetric.objects.filter(post__user=user, post__platform=p).aggregate(total=Sum('views'))['total'] or 0
        engagements = PostMetric.objects.filter(post__user=user, post__platform=p).aggregate(
            likes=Sum('likes'), comments=Sum('comments'), shares=Sum('shares')
        )
        total_eng = (engagements['likes'] or 0) + (engagements['comments'] or 0) + (engagements['shares'] or 0)
        
        platform_data[p] = {
            'count': count,
            'views': views,
            'engagement': total_eng
        }

    # Chart data: Views by platform
    chart_platform_labels = [p.capitalize() for p in platforms]
    chart_platform_views = [platform_data[p]['views'] for p in platforms]
    chart_platform_posts = [platform_data[p]['count'] for p in platforms]

    # Play Store overall metrics
    ps_totals = PlayStoreMetric.objects.filter(user=user).aggregate(
        total_visitors=Sum('store_listing_visitors'),
        total_installs=Sum('store_listing_acquisitions'),
        avg_rating=Avg('average_rating'),
    )

    # Recent 10 playstore records for trend chart
    ps_history = PlayStoreMetric.objects.filter(user=user).order_by('metric_date')[:15]
    ps_dates = [m.metric_date.strftime('%b %d') for m in ps_history]
    ps_installs = [m.store_listing_acquisitions for m in ps_history]
    ps_visitors = [m.store_listing_visitors for m in ps_history]

    return render(request, 'analytics/overview.html', {
        'platform_data': platform_data,
        'chart_platform_labels': json.dumps(chart_platform_labels),
        'chart_platform_views': json.dumps(chart_platform_views),
        'chart_platform_posts': json.dumps(chart_platform_posts),
        'ps_totals': ps_totals,
        'ps_dates': json.dumps(ps_dates),
        'ps_installs': json.dumps(ps_installs),
        'ps_visitors': json.dumps(ps_visitors),
    })


@login_required
def playstore_list_view(request):
    """
    List, filter, and paginate Google Play Store metric entries.
    """
    records = PlayStoreMetric.objects.filter(user=request.user)

    source_filter = request.GET.get('source', '')
    if source_filter:
        records = records.filter(source=source_filter)

    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Aggregates
    totals = records.aggregate(
        total_visitors=Sum('store_listing_visitors'),
        total_installs=Sum('store_listing_acquisitions'),
        total_uninstalls=Sum('uninstalls'),
        avg_rating=Avg('average_rating')
    )

    return render(request, 'analytics/playstore_list.html', {
        'page_obj': page_obj,
        'records': page_obj,
        'totals': totals,
        'source_filter': source_filter,
    })


@login_required
def playstore_create_view(request):
    """
    Add a new Google Play Store visitor/install entry (Manual or API Sync).
    """
    if request.method == 'POST':
        form = PlayStoreMetricForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, f"Google Play Store metric logged for {entry.metric_date} ({entry.get_source_display()}).")
            return redirect('analytics:playstore_list')
    else:
        form = PlayStoreMetricForm(initial={'metric_date': timezone.now().date()})

    return render(request, 'analytics/playstore_form.html', {'form': form})


@login_required
def playstore_delete_view(request, pk):
    """
    Delete a Play Store record.
    """
    entry = get_object_or_404(PlayStoreMetric, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, "Play Store metric entry deleted.")
        return redirect('analytics:playstore_list')
    return render(request, 'analytics/playstore_confirm_delete.html', {'entry': entry})


@login_required
def goal_list_view(request):
    """
    Track growth milestones, deadlines, and calculate progress percentages.
    """
    goals = GrowthGoal.objects.filter(user=request.user)
    status_filter = request.GET.get('status', '')
    if status_filter:
        goals = goals.filter(status=status_filter)

    active_count = goals.filter(status='active').count()
    completed_count = goals.filter(status='completed').count()

    return render(request, 'analytics/goal_list.html', {
        'goals': goals,
        'status_filter': status_filter,
        'active_count': active_count,
        'completed_count': completed_count,
    })


@login_required
def goal_create_view(request):
    """
    Create a new growth target with deadline.
    """
    if request.method == 'POST':
        form = GrowthGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, f'Growth Goal "{goal.title}" created!')
            return redirect('analytics:goal_list')
    else:
        form = GrowthGoalForm(initial={'start_date': timezone.now().date()})

    return render(request, 'analytics/goal_form.html', {
        'form': form,
        'is_create': True
    })


@login_required
def goal_update_view(request, pk):
    """
    Update goal progress or edit deadline.
    """
    goal = get_object_or_404(GrowthGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GrowthGoalForm(request.POST, instance=goal)
        if form.is_valid():
            updated_goal = form.save()
            # If current_value >= target_value, automatically set to completed
            if updated_goal.current_value >= updated_goal.target_value and updated_goal.status == 'active':
                updated_goal.status = 'completed'
                updated_goal.save()
                messages.success(request, f'Congratulations! Goal "{updated_goal.title}" marked as Completed!')
            else:
                messages.success(request, f'Goal "{updated_goal.title}" updated.')
            return redirect('analytics:goal_list')
    else:
        form = GrowthGoalForm(instance=goal)

    return render(request, 'analytics/goal_form.html', {
        'form': form,
        'goal': goal,
        'is_create': False
    })


@login_required
def goal_delete_view(request, pk):
    """
    Delete a growth goal.
    """
    goal = get_object_or_404(GrowthGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        title = goal.title
        goal.delete()
        messages.success(request, f'Goal "{title}" removed.')
        return redirect('analytics:goal_list')
    return render(request, 'analytics/goal_confirm_delete.html', {'goal': goal})
