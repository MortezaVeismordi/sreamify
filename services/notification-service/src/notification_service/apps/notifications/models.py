from django.db import models


class Notification(models.Model):
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('push', 'Push'),
        ('in_app', 'In-App'),
    ]

    user_id = models.IntegerField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.user_id}'

    def mark_as_read(self):
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save()
