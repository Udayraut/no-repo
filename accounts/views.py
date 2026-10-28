from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserAccountForm, UserProfileForm, NotificationPreferencesForm


@login_required
def profile_view(request):
    """
    Displays the user's personal profile information and SaaS activity summary.
    """
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {
        'profile': profile,
    })


@login_required
def settings_view(request):
    """
    Allows user to update account details, profile metadata, and notification preferences.
    """
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        account_form = UserAccountForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        notif_form = NotificationPreferencesForm(request.POST, instance=profile)

        action = request.POST.get('action')
        if action == 'account' and account_form.is_valid():
            account_form.save()
            messages.success(request, 'Account details updated successfully.')
            return redirect('accounts:settings')
        elif action == 'profile' and profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:settings')
        elif action == 'notifications' and notif_form.is_valid():
            notif_form.save()
            messages.success(request, 'Notification preferences saved.')
            return redirect('accounts:settings')
    else:
        account_form = UserAccountForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
        notif_form = NotificationPreferencesForm(instance=profile)

    return render(request, 'accounts/settings.html', {
        'account_form': account_form,
        'profile_form': profile_form,
        'notif_form': notif_form,
        'profile': profile,
    })
