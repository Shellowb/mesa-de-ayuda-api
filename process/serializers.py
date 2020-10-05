from rest_framework import serializers
from process.models import Process

class ProcessSerializer(serializers.ModelSerializer):

  class Meta:
    model = Process
    fields = (
      'id',
      'name',
      'description',
      'published',
      'created_at',
      'last_update'
    )