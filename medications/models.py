from django.db import models
from django.contrib.auth.models import User


class Medication(models.Model):
    MEDICATION_TYPES = [
        ('pill', 'Pill'),
        ('liquid', 'Liquid'),
        ('injection', 'Injection'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    medication_type = models.CharField(max_length=20, choices=MEDICATION_TYPES)
    dosage = models.CharField(max_length=50)
    instructions = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TreatmentPlan(models.Model):
    PLAN_TYPES = [
        ('single', 'Single Medication'),
        ('alternating', 'Alternating Medications'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='treatment_plans')
    name = models.CharField(max_length=100)
    plan_type = models.CharField(
        max_length=20, choices=PLAN_TYPES, default='single')

    medication_primary = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name='primary_treatment_plans'
    )
    medication_secondary = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name='secondary_treatment_plans',
        null=True,
        blank=True
    )

    dose_ml_primary = models.DecimalField(max_digits=4, decimal_places=1)
    dose_ml_secondary = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True)

    interval_hours = models.PositiveIntegerField()
    start_datetime = models.DateTimeField()

    reminder_enabled = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DoseLog(models.Model):
    reminder_sent = models.BooleanField(default=False)
    overdue_alert_sent = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('taken', 'Taken'),
        ('missed', 'Missed'),
    ]

    CONFIRMED_BY_CHOICES = [
        ('manual', 'Manual'),
        ('device', 'Device'),
        ('both', 'Both'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='dose_logs')
    treatment_plan = models.ForeignKey(
        TreatmentPlan,
        on_delete=models.CASCADE,
        related_name='dose_logs'
    )
    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name='dose_logs'
    )

    scheduled_datetime = models.DateTimeField()
    confirmed_datetime = models.DateTimeField(null=True, blank=True)

    scheduled_dose_ml = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True)
    dose_ml_given = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True)
    administered_by = models.CharField(max_length=100, blank=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    confirmed_by = models.CharField(
        max_length=20, choices=CONFIRMED_BY_CHOICES, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medication.name} - {self.status}"


class DeviceEvent(models.Model):
    EVENT_TYPES = [
        ('lid_opened', 'Lid Opened'),
        ('button_pressed', 'Button Pressed'),
        ('dose_removed', 'Dose Removed'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='device_events')
    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name='device_events',
        null=True,
        blank=True
    )

    device_id = models.CharField(max_length=100)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    event_datetime = models.DateTimeField()
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.device_id} - {self.event_type}"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username
