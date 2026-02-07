from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Stream, StreamView
from .serializers import StreamSerializer, StreamViewSerializer


class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Stream.objects.all()
        status_filter = self.request.query_params.get("status", None)
        category_filter = self.request.query_params.get("category", None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if category_filter:
            queryset = queryset.filter(category_id=category_filter)
        return queryset

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        stream = self.get_object()
        stream.status = "live"
        stream.save()
        return Response({"status": "Stream started"})

    @action(detail=True, methods=["post"])
    def end(self, request, pk=None):
        stream = self.get_object()
        stream.status = "ended"
        stream.save()
        return Response({"status": "Stream ended"})

    @action(detail=True, methods=["post"])
    def view(self, request, pk=None):
        stream = self.get_object()
        StreamView.objects.create(
            stream=stream,
            user_id=request.data.get("user_id"),
            ip_address=request.META.get("REMOTE_ADDR"),
        )
        stream.viewer_count += 1
        stream.save()
        return Response({"viewer_count": stream.viewer_count})


class StreamViewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StreamView.objects.all()
    serializer_class = StreamViewSerializer
    permission_classes = [AllowAny]
