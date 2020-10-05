from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from faq.models import FAQs
from faq.serializers import FAQSerializer

@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def faq_list(request):
  """
    GET list of questions
    POST a new question
    DELETE all questions
  """
  if request.method == 'GET':
    faqs = FAQs.objects.all().order_by('-created_at')
    
    faqs_serializer = FAQSerializer(faqs, many=True)
    return JsonResponse(faqs_serializer.data, safe=False)

  elif request.method == 'POST':
    faq_data = JSONParser().parse(request)
    faq_serializer = FAQSerializer(data=faq_data)
    if faq_serializer.is_valid():
      faq_serializer.save()
      return JsonResponse(faq_serializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(faq_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  elif request.method == 'DELETE':
    count = FAQs.objects.all().delete()
    return JsonResponse({'message': '{} Questions were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def faq_list_published(request):
  """
    GET all published FAQs
  """
  faqs = FAQscess.objects.filter(published=True).order_by('-created_at')
        
  if request.method == 'GET': 
    faqs_serializer = FAQSerializer(faqs, many=True)
    return JsonResponse(faqs_serializer.data, safe=False)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def faq_detail(request, id_faq):
  """
    GET a FAQ
    PUT a new FAQ
    DELETE a FAQ
  """

  # Find a question by pk (id)
  try: 
    faq = FAQs.objects.get(pk=id_faq)
  except FAQs.DoesNotExist:
    return JsonResponse({'message': 'The question does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET': 
    faq_serializer = FAQSerializer(faq) 
    return JsonResponse(faq_serializer.data) 
  
  elif request.method == 'PUT': 
    faq_data = JSONParser().parse(request) 
    faq_serializer = FAQSerializer(faq, data=faq_data) 
    if faq_serializer.is_valid(): 
      faq_serializer.save() 
      return JsonResponse(faq_serializer.data) 
    return JsonResponse(faq_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

  elif request.method == 'DELETE': 
    faq.delete() 
    return JsonResponse({'message': 'Question was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def process_list_faq(request, id_process):
  """
    GET a FAQ asociated to a process
  """
  faqs = FAQs.objects.filter(process=id_process).order_by('-created_at')
        
  if request.method == 'GET': 
    faqs_serializer = FAQSerializer(faqs, many=True)
    return JsonResponse(faqs_serializer.data, safe=False)

