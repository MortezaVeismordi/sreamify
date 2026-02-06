from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Notification
from .serializers import NotificationSerializer
from .tasks import send_email_notification, send_push_notification


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Notification.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        is_read = self.request.query_params.get('is_read', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notification = serializer.save()

        # Send notification asynchronously
        if notification.notification_type == 'email':
            send_email_notification.delay(notification.id)
        elif notification.notification_type == 'push':
            send_push_notification.delay(notification.id)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['put'])
    def read(self, request, pk=None):
        notification = self.get_object()
        notification.mark_as_read()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
