import csv
from io import BytesIO
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from tracker.models import SocialPost, PostMetric, DailyLog
from analytics.models import PlayStoreMetric, GrowthGoal


@login_required
def reports_index_view(request):
    """
    Export center: export posts, analytics, and playstore logs to CSV/Excel.
    """
    user = request.user
    post_count = SocialPost.objects.filter(user=user).count()
    playstore_count = PlayStoreMetric.objects.filter(user=user).count()
    daily_log_count = DailyLog.objects.filter(user=user).count()

    return render(request, 'reports/index.html', {
        'post_count': post_count,
        'playstore_count': playstore_count,
        'daily_log_count': daily_log_count,
    })


@login_required
def export_posts_csv(request):
    """
    Stream CSV export of all social media posts and latest metrics.
    """
    response = HttpResponse(content_type='text/csv')
    filename = f"skyniya_posts_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Title', 'Platform', 'Type', 'Status', 'Scheduled At',
        'Published At', 'Tags', 'Latest Views', 'Latest Likes', 'Latest Comments',
        'Latest Shares', 'Latest Saves', 'Engagement Rate %', 'Metric Source'
    ])

    posts = SocialPost.objects.filter(user=request.user).order_by('-created_at')
    for p in posts:
        m = p.latest_metric
        writer.writerow([
            p.id,
            p.title,
            p.get_platform_display(),
            p.get_post_type_display(),
            p.get_status_display(),
            p.scheduled_at.strftime('%Y-%m-%d %H:%M') if p.scheduled_at else '',
            p.published_at.strftime('%Y-%m-%d %H:%M') if p.published_at else '',
            p.tags,
            m.views if m else 0,
            m.likes if m else 0,
            m.comments if m else 0,
            m.shares if m else 0,
            m.saves if m else 0,
            m.engagement_rate if m else 0.0,
            m.get_source_display() if m else 'N/A'
        ])

    return response


@login_required
def export_posts_excel(request):
    """
    Export posts to formatted Microsoft Excel (.xlsx) using openpyxl.
    """
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Posts & Performance"

        # Headers
        headers = [
            'ID', 'Title', 'Platform', 'Type', 'Status', 'Scheduled Date',
            'Published Date', 'Tags', 'Views', 'Likes', 'Comments', 'Shares', 'Engagement Rate %', 'Source'
        ]
        ws.append(headers)

        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="0071E3", end_color="0071E3", fill_type="solid")
        for col_num in range(1, len(headers) + 1):
            cell = ws.cell(row=1, column=col_num)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")

        posts = SocialPost.objects.filter(user=request.user).order_by('-created_at')
        for p in posts:
            m = p.latest_metric
            ws.append([
                p.id,
                p.title,
                p.get_platform_display(),
                p.get_post_type_display(),
                p.get_status_display(),
                p.scheduled_at.strftime('%Y-%m-%d %H:%M') if p.scheduled_at else '',
                p.published_at.strftime('%Y-%m-%d %H:%M') if p.published_at else '',
                p.tags,
                m.views if m else 0,
                m.likes if m else 0,
                m.comments if m else 0,
                m.shares if m else 0,
                m.engagement_rate if m else 0.0,
                m.get_source_display() if m else 'N/A'
            ])

        # Adjust column widths
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = openpyxl.utils.get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        filename = f"skyniya_posts_{timezone.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except ImportError:
        # Fallback to CSV if openpyxl is not yet installed
        return export_posts_csv(request)


@login_required
def export_playstore_csv(request):
    """
    Stream CSV export of all Google Play Store metric records.
    """
    response = HttpResponse(content_type='text/csv')
    filename = f"skyniya_playstore_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow([
        'Date', 'App Name', 'Package Name', 'Source', 'Store Visitors',
        'Acquisitions (Installs)', 'Uninstalls', 'Active Devices', 'Conversion Rate %', 'Rating', 'Notes'
    ])

    records = PlayStoreMetric.objects.filter(user=request.user).order_by('-metric_date')
    for r in records:
        writer.writerow([
            r.metric_date.strftime('%Y-%m-%d'),
            r.app_name,
            r.package_name,
            r.get_source_display(),
            r.store_listing_visitors,
            r.store_listing_acquisitions,
            r.uninstalls,
            r.active_devices,
            r.conversion_rate,
            r.average_rating,
            r.notes
        ])

    return response


@login_required
def export_daily_logs_csv(request):
    """
    Stream CSV export of daily productivity logs.
    """
    response = HttpResponse(content_type='text/csv')
    filename = f"skyniya_daily_logs_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow([
        'Date', 'Focus Area', 'Items Created', 'Hours Spent', 'Productivity Rating (1-5)', 'Key Learnings', 'Notes'
    ])

    logs = DailyLog.objects.filter(user=request.user).order_by('-log_date')
    for l in logs:
        writer.writerow([
            l.log_date.strftime('%Y-%m-%d'),
            l.focus_area,
            l.content_items_created,
            l.hours_spent,
            l.productivity_score,
            l.key_learnings,
            l.notes
        ])

    return response
