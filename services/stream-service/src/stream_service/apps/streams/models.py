from django.db import models
from django.conf import settings


class Stream(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("live", "Live"),
        ("ended", "Ended"),
        ("scheduled", "Scheduled"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user_id = models.IntegerField()
    category = models.ForeignKey(
        "categories.Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    viewer_count = models.IntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "streams"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class StreamView(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name="views")
    user_id = models.IntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "stream_views"
        ordering = ["-viewed_at"]
