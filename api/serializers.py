import os
import csv

from django.conf import settings
from rest_framework import serializers

from .models import Channel, Content


class ContentSerializer(serializers.ModelSerializer):
    content_file = serializers.FileField(required=True)

    def validate(self, data):
        channel_object = Channel.objects.get(pk=data['channel'].id)
        if channel_object.child_channels.count() > 0:
            raise serializers.ValidationError('Channel cannot include contents while having sub-channels.')
        return data

    class Meta:
        model = Content
        fields = ['id', 'title', 'description', 'genre', 'rating', 'channel', 'is_active', 'content_file']


class ChannelSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, required=False)
    child_channels = serializers.SerializerMethodField()
    channel_image = serializers.ImageField(required=True)
    rating = serializers.SerializerMethodField()

    @staticmethod
    def get_child_channels(obj):
        return obj.child_channels.all().values_list('id', flat=True)

    @staticmethod
    def get_rating(obj):
        i_sum, i_len = 0, 0
        static_files_path = os.path.join(settings.BASE_DIR, 'static_files')
        with open('{}/ratings.csv'.format(static_files_path)) as f:
            channel_ratings = [list(row.items()) for row in csv.DictReader(f, skipinitialspace=True)]
            for i in channel_ratings:
                channel_id, channel_rating = int(i[0][1]), float(i[1][1])
                if channel_id in obj.child_channels.all().values_list('id', flat=True) or channel_id == obj.id:
                    i_sum += channel_rating
                    i_len += 1
        if i_len != 0:
            return str(round(i_sum / i_len, 2))
        return None

    def validate(self, data):
        if self.instance:
            if self.instance.child_channels.count() > 0 and 'contents' in data:
                raise serializers.ValidationError('Channel cannot include contents while having sub-channels.')
            elif self.instance.contents.count() > 0 and 'child_channels' in data:
                raise serializers.ValidationError('Channel cannot include sub-channels while having contents.')
        if 'contents' in data and 'child_channels' in data:
            raise serializers.ValidationError('Channel cannot include both contents and sub-channels.')
        return data

    class Meta:
        model = Channel
        fields = ['id', 'title', 'language', 'parent_channel', 'child_channels', 'contents', 'is_active', 'channel_image', 'rating']
