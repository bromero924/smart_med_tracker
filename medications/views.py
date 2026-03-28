from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import DoseLog
from .utils import get_next_dose, get_overdue_doses
from django.shortcuts import render


def landing_page(request):
    return render(request, 'landing.html')


def privacy_page(request):
    return render(request, 'privacy.html')


def terms_page(request):
    return render(request, 'terms.html')


@login_required
def dashboard(request):
    user = request.user
    next_dose = get_next_dose(user)
    overdue_doses = get_overdue_doses(user)
    recent_doses = DoseLog.objects.filter(
        user=user).order_by('-scheduled_datetime')[:10]

    context = {
        'next_dose': next_dose,
        'overdue_doses': overdue_doses,
        'recent_doses': recent_doses,
    }
    return render(request, 'medications/dashboard.html', context)


def take_dose(request, dose_id):
    dose = get_object_or_404(DoseLog, id=dose_id)

    dose.status = 'taken'
    dose.confirmed_datetime = timezone.now()
    dose.dose_ml_given = dose.scheduled_dose_ml
    dose.administered_by = 'parent'
    dose.confirmed_by = 'manual'
    dose.save()

    return redirect('dashboard')
