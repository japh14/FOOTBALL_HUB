# from django.shortcuts import render
# from django.http import HttpResponse
from rest_framework.views import APIView # Base class for creating API endpoints
from rest_framework.response import Response # Standard response object for APIs; Returns JSON data to the client
from rest_framework.permissions import IsAuthenticated, AllowAny # Permission classes to control access to views


class HelloUserView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def get(self, request):
        user = request.user  # Get the authenticated user
        return Response({
            'message': f'Hello, {user.first_name} {user.last_name}!',
            'email': user.email,
            'feedback': f'Congratulations {user.username}, you have successfully accessed your protected endpoint! Now you can start building more complex features.'
        })
    

class PublicView(APIView):
    permission_classes = [AllowAny] # Overrides the default authentication requirement, making this endpoint accessible without a token.
    
    def get(self, request):
        return Response({'message': 'This is a public endpoint!'})
    