from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Channel, Content
from .serializers import ChannelSerializer, ContentSerializer


class ChannelList(APIView):
    @staticmethod
    def get(request):
        objects = Channel.objects.all()
        serializer = ChannelSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        serializer = ChannelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChannelDetail(APIView):
    @staticmethod
    def get_object(channel_pk: int):
        try:
            return Channel.objects.get(pk=channel_pk)
        except Channel.DoesNotExist:
            raise Http404

    def get(self, request, channel_pk: int):
        snippet = self.get_object(channel_pk)
        serializer = ChannelSerializer(snippet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, channel_pk: int):
        snippet = self.get_object(channel_pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentList(APIView):
    @staticmethod
    def get(request, channel_pk: int):
        objects = Content.objects.filter(channel__id=channel_pk).all()
        serializer = ContentSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, channel_pk: int):
        request.data.update({'channel': channel_pk})
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentDetail(APIView):
    @staticmethod
    def get_object(channel_pk: int, content_pk: int):
        try:
            return Content.objects.filter(channel__id=channel_pk).get(pk=content_pk)
        except Content.DoesNotExist:
            raise Http404

    def get(self, request, channel_pk: int, content_pk: int):
        snippet = self.get_object(channel_pk, content_pk)
        serializer = ContentSerializer(snippet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, channel_pk: int, content_pk: int):
        snippet = self.get_object(channel_pk, content_pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
