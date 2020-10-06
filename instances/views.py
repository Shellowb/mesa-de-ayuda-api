from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from instances.models import Instance, Steps, News
from instances.serializers import InstanceSerializer, StepsSerializer, NewsSerializer

@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def instance_list(request):
  """
    GET list of instances
    POST a new instances
    DELETE all instances
  """
  if request.method == 'GET':
    instances = Instance.objects.all().order_by('-created_at')
    
    instances_serializer = InstanceSerializer(instances, many=True)
    return JsonResponse(instances_serializer.data, safe=False)

  elif request.method == 'POST':
    instance_data = JSONParser().parse(request)
    instance_serializer = InstanceSerializer(data=instance_data)
    if instance_serializer.is_valid():
      print(instance_serializer)
      instance_serializer.save()
      return JsonResponse(instance_serializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(instance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  elif request.method == 'DELETE':
    count = Instance.objects.all().delete()
    return JsonResponse({'message': '{} Instances were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def instance_detail(request, id_instance):
  """
    GET a instance
    PUTT a new instance
    DELETE a instance
  """

  # Find a instance by pk (id)
  try: 
    instance = Instance.objects.get(pk=id_instance)
  except Instance.DoesNotExist:
    return JsonResponse({'message': 'The instance does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET': 
    instance_serializer = InstanceSerializer(instance) 
    return JsonResponse(instance_serializer.data) 
  
  elif request.method == 'PUT': 
    instance_data = JSONParser().parse(request) 
    instance_serializer = InstanceSerializer(instance, data=instance_data) 
    if instance_serializer.is_valid(): 
      instance_serializer.save() 
      return JsonResponse(instance_serializer.data) 
    return JsonResponse(instance_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

  elif request.method == 'DELETE': 
    instance.delete() 
    return JsonResponse({'message': 'Instance was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
  
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def instance_list_published(request):
  """
    GET all published instance
  """
  instances = Instance.objects.filter(published=True).order_by('-created_at')
        
  if request.method == 'GET': 
    instances_serializer = InstanceSerializer(instances, many=True)
    return JsonResponse(instances_serializer.data, safe=False)


@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def steps_list(request):
  """
    GET list of steps
    POST a new step
    DELETE all steps
  """
  if request.method == 'GET':
    steps = Steps.objects.all().order_by('-created_at')
    
    name = request.GET.get('name', None)
    if name is not None:
      steps = Steps.filter(name__icontains=name)
    
    steps_serializer = StepsSerializer(steps, many=True)
    return JsonResponse(steps_serializer.data, safe=False)

  elif request.method == 'POST':
    steps_data = JSONParser().parse(request)
    steps_serializer = StepsSerializer(data=steps_data)
    if steps_serializer.is_valid():
      steps_serializer.save()
      return JsonResponse(steps_serializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(steps_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  elif request.method == 'DELETE':
    count = Steps.objects.all().delete()
    return JsonResponse({'message': '{} Steps were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def steps_detail(request, id_step):
  """
    GET a step
    PUTT a new step
    DELETE a step
  """

  # Find a process by pk (id)
  try: 
    step = Steps.objects.get(pk=id_step)
  except Steps.DoesNotExist:
    return JsonResponse({'message': 'The step does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET': 
    step_serializer = StepsSerializer(step) 
    return JsonResponse(step_serializer.data) 
  
  elif request.method == 'PUT': 
    step_data = JSONParser().parse(request) 
    step_serializer = StepsSerializer(step, data=step_data) 
    if step_serializer.is_valid(): 
      step_serializer.save() 
      return JsonResponse(step_serializer.data) 
    return JsonResponse(step_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

  elif request.method == 'DELETE': 
    step.delete() 
    return JsonResponse({'message': 'Step was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def instance_list_steps(request, id_instance):
  """
    GET a step instance
    DELETE all step instances from a instance
  """

  # Find a instance by pk (id)
  try: 
    steps = Steps.objects.filter(instance=id_instance).order_by('start_date')
  except Steps.DoesNotExist:
    return JsonResponse({'message': 'The step does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET': 
    steps_serializer = StepsSerializer(steps, many=True) 
    return JsonResponse(steps_serializer.data, safe=False) 

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def process_list_instances(request, id_process):
  """
    GET a instance process
    DELETE all instances from a process
  """

  # Find a instance by process
  try: 
    instances = Instance.objects.filter(process=id_process).order_by('-created_at')
  except Instance.DoesNotExist:
    return JsonResponse({'message': 'The instance does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET': 
    instances_serializer = InstanceSerializer(instances, many=True) 
    return JsonResponse(instances_serializer.data, safe=False) 

@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def news_list(request):
  """
    GET list of news
    POST a new news
    DELETE all news
  """
  if request.method == 'GET':
    news = News.objects.all().order_by('-created_at')
    
    name = request.GET.get('name', None)
    if name is not None:
      news = News.filter(name__icontains=name)
    
    news_serializer = NewsSerializer(news, many=True)
    return JsonResponse(news_serializer.data, safe=False)

  elif request.method == 'POST':
    news_data = JSONParser().parse(request)
    news_serializer = NewsSerializer(data=news_data)
    if news_serializer.is_valid():
      news_serializer.save()
      return JsonResponse(news_serializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(news_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  elif request.method == 'DELETE':
    count = News.objects.all().delete()
    return JsonResponse({'message': '{} News were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def news_detail(request, id_news):
  """
    GET a news
    PUTT a new news
    DELETE a news
  """

  # Find a process by pk (id)
  try: 
    news = News.objects.get(pk=id_news)
  except News.DoesNotExist:
    return JsonResponse({'message': 'The news does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET': 
    news_serializer = NewsSerializer(news) 
    return JsonResponse(news_serializer.data) 
  
  elif request.method == 'PUT': 
    news_data = JSONParser().parse(request) 
    news_serializer = NewsSerializer(news, data=news_data) 
    if news_serializer.is_valid(): 
      news_serializer.save() 
      return JsonResponse(news_serializer.data) 
    return JsonResponse(news_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

  elif request.method == 'DELETE': 
    news.delete() 
    return JsonResponse({'message': 'News was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def instance_list_news(request, id_instance):
  """
    GET a news instance
    DELETE all news instances from a instance
  """

  # Find a instance by pk (id)
  try: 
    news = News.objects.filter(instance=id_instance).order_by('-created_at')
  except News.DoesNotExist:
    return JsonResponse({'message': 'The news does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET': 
    news_serializer = NewsSerializer(news, many=True) 
    return JsonResponse(news_serializer.data, safe=False) 