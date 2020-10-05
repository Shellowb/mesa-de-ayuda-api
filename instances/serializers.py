from rest_framework import serializers
from instances.models import Instance, Steps, News

class InstanceSerializer(serializers.ModelSerializer):

  class Meta:
    model = Instance
    fields = (
      'id',
      'name',
      'published',
      'process',
      'created_at',
      'last_update'
    )

class StepsSerializer(serializers.ModelSerializer):

  class Meta:
    model = Steps
    fields = (
      'id',
      'start_date',
      'end_date',
      'name',
      'description',
      'instance',
      'created_at',
      'last_update'
    )

class NewsSerializer(serializers.ModelSerializer):

  class Meta:
    model = News
    fields = (
      'id',
      'description',
      'instance',
      'created_at',
      'last_update'
    )