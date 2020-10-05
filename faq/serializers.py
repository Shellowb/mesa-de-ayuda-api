from rest_framework import serializers
from faq.models import FAQs

class FAQSerializer(serializers.ModelSerializer):

  class Meta:
    model = FAQs
    fields = (
      'id',
      'question',
      'answer',
      'created_at',
      'last_update',
      'published',
      'process'
    )
