from django.http import JsonResponse
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(["GET", "POST"])
def get_profiles(request):
    if request.method == "GET":
        # get all profiles data 
        profiles = Profile.objects.all()
        # serialize profiles
        serializer = ProfileSerializer(profiles, many=True) # many=True for returning al list of objects
        # return serialized profiles
        return JsonResponse(serializer.data, safe=False) # safe=False for non-dict objects
    
    if request.method == "POST":
        deserializer = ProfileSerializer(data=request.data) # do the opposite by deserializing
        if deserializer.is_valid():
            deserializer.save()
            return Response(deserializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'PUT', 'DELETE'])
def get_profile(request, id):
    # Check if profile exists
    try:
        drink = Profile.objects.get(pk=id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET": 
        serializer = ProfileSerializer(drink)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT": 
        serializer = ProfileSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE": 
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)