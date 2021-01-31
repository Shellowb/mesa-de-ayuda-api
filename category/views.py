from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from category.models import Category
from faq.models import FAQs
from category.serializers import CategorySerializer

@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def category_list(request):
  """
    GET list of categories
    POST a new categories
    DELETE all categories
  """
  if request.method == 'GET':
    categories = Category.objects.all().order_by('-created_at')
    
    categories_serializer = CategorySerializer(categories, many=True)
    return JsonResponse(categories_serializer.data, safe=False)

  elif request.method == 'POST':
    categories_data = JSONParser().parse(request)
    categories_serializer = CategorySerializer(data=categories_data)
    if categories_serializer.is_valid():
      categories_serializer.save()
      return JsonResponse(categories_serializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(categories_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  elif request.method == 'DELETE':
    count = Category.objects.all().delete()
    return JsonResponse({'message': '{} Categories were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def category_detail(request, id_category):
  """
    GET a category
    PUTT a new category
    DELETE a category
  """

  # Find a category by pk (id)
  try: 
    category = Category.objects.get(pk=id_category)
  except Category.DoesNotExist:
    return JsonResponse({'message': 'The category does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET': 
    category_serializer = CategorySerializer(category) 
    return JsonResponse(category_serializer.data) 
  
  elif request.method == 'PUT': 
    category_data = JSONParser().parse(request) 
    category_serializer = CategorySerializer(category, data=category_data) 
    if category_serializer.is_valid(): 
      category_serializer.save() 
      return JsonResponse(category_serializer.data) 
    return JsonResponse(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

  elif request.method == 'DELETE': 
    faqs = FAQs.objects.filter(category=id_category)
    if (len(faqs) == 0):
      category.delete() 
      return JsonResponse({'message': 'category was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({'message': 'The category has questions asociated'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def process_list_categories(request, id_process):
  """
    GET a category process
    DELETE all categories from a process
  """

  # Find a category by process
  try: 
    categories = Category.objects.filter(process=id_process).order_by('-created_at')
  except Category.DoesNotExist:
    return JsonResponse({'message': 'The category does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET': 
    categories_serializer = CategorySerializer(categories, many=True) 
    return JsonResponse(categories_serializer.data, safe=False) 

