import datetime
import calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import SocialPost, PostMetric, DailyLog
from .forms import SocialPostForm, PostMetricForm, DailyLogForm


@login_required
def post_list_view(request):
    """
    Search, filter, and paginate social media posts.
    """
    posts = SocialPost.objects.filter(user=request.user)

    q = request.GET.get('q', '').strip()
    platform = request.GET.get('platform', '').strip()
    status = request.GET.get('status', '').strip()

    if q:
        posts = posts.filter(
            Q(title__icontains=q) | 
            Q(caption__icontains=q) | 
            Q(tags__icontains=q)
        )

    if platform:
        posts = posts.filter(platform=platform)

    if status:
        posts = posts.filter(status=status)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tracker/post_list.html', {
        'page_obj': page_obj,
        'posts': page_obj,
        'platform_filter': platform,
        'status_filter': status,
        'query': q,
        'platform_choices': SocialPost.PLATFORM_CHOICES,
        'status_choices': SocialPost.STATUS_CHOICES,
    })


@login_required
def post_create_view(request):
    """
    Create a new social media post record.
    """
    if request.method == 'POST':
        form = SocialPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, f'Post "{post.title}" created successfully.')
            return redirect('tracker:post_detail', pk=post.pk)
    else:
        form = SocialPostForm()

    return render(request, 'tracker/post_form.html', {
        'form': form,
        'is_create': True,
    })


@login_required
def post_detail_view(request, pk):
    """
    Detailed view of a social post, its metrics history, and metrics log form.
    """
    post = get_object_or_404(SocialPost, pk=pk, user=request.user)
    metrics = post.metrics.all().order_by('-metric_date', '-created_at')
    metric_form = PostMetricForm(initial={'metric_date': timezone.now().date()})

    return render(request, 'tracker/post_detail.html', {
        'post': post,
        'metrics': metrics,
        'metric_form': metric_form,
    })


@login_required
def post_update_view(request, pk):
    """
    Edit an existing social media post.
    """
    post = get_object_or_404(SocialPost, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SocialPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, f'Post "{post.title}" updated.')
            return redirect('tracker:post_detail', pk=post.pk)
    else:
        form = SocialPostForm(instance=post)

    return render(request, 'tracker/post_form.html', {
        'form': form,
        'post': post,
        'is_create': False,
    })


@login_required
def post_delete_view(request, pk):
    """
    Delete a social post with confirmation.
    """
    post = get_object_or_404(SocialPost, pk=pk, user=request.user)
    if request.method == 'POST':
        title = post.title
        post.delete()
        messages.success(request, f'Post "{title}" has been deleted.')
        return redirect('tracker:post_list')

    return render(request, 'tracker/post_confirm_delete.html', {'post': post})


@login_required
def metric_create_view(request, post_pk):
    """
    Add a new metric snapshot (Manual or API-Sync) for a post.
    """
    post = get_object_or_404(SocialPost, pk=post_pk, user=request.user)
    if request.method == 'POST':
        form = PostMetricForm(request.POST)
        if form.is_valid():
            metric = form.save(commit=False)
            metric.post = post
            # Update or create if snapshot on same date and source already exists
            existing = PostMetric.objects.filter(post=post, metric_date=metric.metric_date, source=metric.source).first()
            if existing:
                existing.views = metric.views
                existing.likes = metric.likes
                existing.comments = metric.comments
                existing.shares = metric.shares
                existing.saves = metric.saves
                existing.clicks = metric.clicks
                existing.reach = metric.reach
                existing.impressions = metric.impressions
                existing.notes = metric.notes
                existing.save()
                messages.success(request, f"Metrics for {metric.metric_date} updated ({metric.get_source_display()}).")
            else:
                metric.save()
                messages.success(request, f"New metrics recorded ({metric.get_source_display()}).")
            return redirect('tracker:post_detail', pk=post.pk)
        else:
            messages.error(request, "Please check the entered metric numbers.")
    return redirect('tracker:post_detail', pk=post.pk)


@login_required
def daily_log_view(request):
    """
    Daily content tracker: record daily focus, hours, output items, and reflection notes.
    """
    today = timezone.now().date()
    today_log = DailyLog.objects.filter(user=request.user, log_date=today).first()

    if request.method == 'POST':
        form = DailyLogForm(request.POST, instance=today_log)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, "Daily content log saved successfully.")
            return redirect('tracker:daily_log')
    else:
        form = DailyLogForm(instance=today_log, initial={'log_date': today})

    past_logs = DailyLog.objects.filter(user=request.user).order_by('-log_date')[:30]

    return render(request, 'tracker/daily_log.html', {
        'form': form,
        'today_log': today_log,
        'past_logs': past_logs,
        'today': today,
    })


@login_required
def calendar_view(request):
    """
    Visual monthly calendar showcasing scheduled & published content and daily outputs.
    """
    now = timezone.now()
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))

    if month > 12:
        year += 1
        month = 1
    elif month < 1:
        year -= 1
        month = 12

    cal = calendar.Calendar(firstweekday=6)  # Sunday start
    month_days = cal.monthdatescalendar(year, month)

    start_date = month_days[0][0]
    end_date = month_days[-1][-1]

    # Fetch posts in this range
    posts = SocialPost.objects.filter(
        user=request.user
    ).filter(
        Q(scheduled_at__date__range=(start_date, end_date)) |
        Q(published_at__date__range=(start_date, end_date))
    )

    # Fetch daily logs in this range
    logs = DailyLog.objects.filter(
        user=request.user,
        log_date__range=(start_date, end_date)
    )

    # Organize events by date string 'YYYY-MM-DD'
    events_by_date = {}
    for p in posts:
        event_date = None
        if p.status == 'scheduled' and p.scheduled_at:
            event_date = p.scheduled_at.date()
        elif p.published_at:
            event_date = p.published_at.date()
        elif p.scheduled_at:
            event_date = p.scheduled_at.date()

        if event_date:
            d_str = event_date.strftime('%Y-%m-%d')
            if d_str not in events_by_date:
                events_by_date[d_str] = []
            events_by_date[d_str].append({
                'type': 'post',
                'title': f"{p.get_platform_display()}: {p.title}",
                'status': p.status,
                'url': p.get_absolute_url(),
                'platform': p.platform,
            })

    for log in logs:
        d_str = log.log_date.strftime('%Y-%m-%d')
        if d_str not in events_by_date:
            events_by_date[d_str] = []
        events_by_date[d_str].append({
            'type': 'log',
            'title': f"Log: {log.focus_area} ({log.hours_spent}h)",
            'status': 'completed',
            'url': reverse('tracker:daily_log'),
            'platform': 'daily_log',
        })

    # Calendar metadata
    month_name = calendar.month_name[month]
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    calendar_weeks = []
    for week in month_days:
        week_data = []
        for d in week:
            d_str = d.strftime('%Y-%m-%d')
            week_data.append({
                'date': d,
                'day': d.day,
                'is_current_month': d.month == month,
                'is_today': d == now.date(),
                'events': events_by_date.get(d_str, []),
            })
        calendar_weeks.append(week_data)

    return render(request, 'tracker/calendar.html', {
        'weeks': calendar_weeks,
        'year': year,
        'month': month,
        'month_name': month_name,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    })
