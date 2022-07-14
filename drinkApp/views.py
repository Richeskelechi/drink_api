from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import DrinkSerializer
from .models import Drink

# Create your views here.

@api_view(['GET', 'POST'])
def drink_list(request, format=None):
    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return Response({'drink':serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        serializer = DrinkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'drinks':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'err':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def drink_details(request, pk, format=None):
    try:
        drink = Drink.objects.get(pk=pk)
    except Drink.DoesNotExist:
        return Response({'err':'Drink Not Found'},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        return Response({'drink':serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data
        serializer = DrinkSerializer(drink, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'drink':serializer.data}, status=status.HTTP_200_OK)
        return Response({'err':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        data = request.data
        serializer = DrinkSerializer(drink, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'drink':serializer.data}, status=status.HTTP_200_OK)
        return Response({'err':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if drink.delete():
            return Response({'drink':'Drink Deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'err':'Error Deleting Drink'},status=status.HTTP_400_BAD_REQUEST)