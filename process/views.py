from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from process.models import Process
from process.serializers import ProcessSerializer, ProcessRetriveSerializer

@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def process_list(request):
  """
    GET list of process
    POST a new process
    DELETE all process
  """
  if request.method == 'GET':
    processes = Process.objects.all().order_by('-created_at')
    
    processes_serializer = ProcessRetriveSerializer(processes, many=True)
    return JsonResponse(processes_serializer.data, safe=False)

  elif request.method == 'POST':
    process_data = JSONParser().parse(request)
    process_data['created_by'] = request.user.id
    process_data['updated_by'] = request.user.id

    process_serializer = ProcessSerializer(data=process_data)
    if process_serializer.is_valid():
      process_serializer.save()
      return JsonResponse(process_serializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(process_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  elif request.method == 'DELETE':
    count = Process.objects.all().delete()
    return JsonResponse({'message': '{} Processes were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def process_detail(request, id_process):
  """
    GET a process
    PUT a new process
    DELETE a process
  """

  # Find a process by pk (id)
  try: 
    process = Process.objects.get(pk=id_process)
  except Process.DoesNotExist:
    return JsonResponse({'message': 'The process does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET': 
    process_serializer = ProcessRetriveSerializer(process) 
    return JsonResponse(process_serializer.data) 
  
  elif request.method == 'PUT': 
    process_data = JSONParser().parse(request) 
    process_data['updated_by'] = request.user.id
    process_serializer = ProcessSerializer(process, data=process_data) 
    if process_serializer.is_valid(): 
      process_serializer.save() 
      return JsonResponse(process_serializer.data) 
    return JsonResponse(process_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

  elif request.method == 'DELETE': 
    process.delete() 
    return JsonResponse({'message': 'Process was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
  
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def process_list_published(request):
  """
    GET all published process
  """
  processes = Process.objects.filter(published=True).order_by('-created_at')
        
  if request.method == 'GET': 
    processes_serializer = ProcessSerializer(processes, many=True)
    return JsonResponse(processes_serializer.data, safe=False)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def process_detail_published(request, id_process):
  """
    GET a process
  """

  # Find a process by pk (id)
  try: 
    process = Process.objects.get(pk=id_process)
  except Process.DoesNotExist:
    return JsonResponse({'message': 'The process does not exist'}, status=status.HTTP_404_NOT_FOUND)

  process_serializer = ProcessSerializer(process) 
  if (process_serializer.data['published']):
    return JsonResponse(process_serializer.data) 
  return JsonResponse({'message': 'The process does not exist'}, status=status.HTTP_404_NOT_FOUND)
