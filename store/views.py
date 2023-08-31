from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes , authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AdminBoxSerializer
from .models import Box
from .serializers import AdminBoxSerializer , UserBoxSerializer , UserRegistrationSerializer
from .filters import BoxFilter
from .validation import checkValidity



# Register a user(Staff)
@api_view(['POST'])
@permission_classes([AllowAny])
def userRegistration(request):
    serializer = UserRegistrationSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Staff member can make a box
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createBox(request):
    box = Box(createdBy = request.user)
    data = JSONParser().parse(request)
    serializer = AdminBoxSerializer(box, data=data,partial=True)
    if serializer.is_valid() and checkValidity(request.user):
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Anyone can view Boxes
@api_view(['GET'])
@permission_classes([AllowAny])
def getAllBoxes(request):
    box_queryset = Box.objects.all()
    boxes = BoxFilter(request.GET,queryset=box_queryset).qs
    serializer = UserBoxSerializer(boxes, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)



# Only Staff can look at their Boxes
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUserBox(request):
    box_queryset = Box.objects.filter(createdBy=request.user)
    boxes = BoxFilter(request.GET,queryset=box_queryset).qs
    serializer = AdminBoxSerializer(boxes, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)



@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateBox(request,pk):
    try:
        box = Box.objects.get(pk=pk)
    except Box.DoesNotExist:
        return Response({"error": f"Box does not exist with ID: {pk}"}, status=status.HTTP_404_NOT_FOUND)

    data = JSONParser().parse(request)
    serializer = AdminBoxSerializer(box, data=data,partial=True)
    if serializer.is_valid() and checkValidity(request.user) :
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteBox(request,pk):
    try:
        box = Box.objects.get(pk=pk)
        if request.user == box.createdBy :
            box.delete()
            return Response({"message" : f"Item Deleted Successfully with ID : {pk}"},status=status.HTTP_200_OK)
        else:
            return Response({"error": f"Only Owner can Delete Their Box"}, status=status.HTTP_403_FORBIDDEN)
    except Box.DoesNotExist:
        return Response({"error": f"Box does not exist with ID: {pk}"}, status=status.HTTP_404_NOT_FOUND)
    