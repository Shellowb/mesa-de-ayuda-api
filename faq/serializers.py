from rest_framework import serializers
from faq.models import FAQs
from Profile.serializers import UserSerializer
from category.serializers import CategorySerializer

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
      'process',
      'likes',
      'dislikes',
      'category',
      'created_by',
      'updated_by'
    )

class FAQRetriveSerializer(serializers.ModelSerializer):
  created_by = UserSerializer(read_only=True)
  updated_by = UserSerializer(read_only=True)
  category = CategorySerializer(read_only=True)

  class Meta:
    model = FAQs
    fields = (
      'id',
      'question',
      'answer',
      'created_at',
      'last_update',
      'published',
      'likes',
      'dislikes',
      'process',
      'category',
      'created_by',
      'updated_by'
    )
