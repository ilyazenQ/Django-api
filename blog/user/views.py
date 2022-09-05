from django.shortcuts import render
from requests import Response
from rest_framework.views import APIView

from .models import CustomUser


# Create your views here.
class UserSubAPIAdd(APIView):
    def put(self, request, *args, **kwargs):
        sub_id = kwargs.get("sub_id", None)
        user_id = kwargs.get("user_id", None)
        if not sub_id or not user_id:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = CustomUser.objects.get(id=user_id)
            sub = CustomUser.objects.get(id=sub_id)
        except:
            return Response({"error": "Object does not exists"})
        # serializer = UserSubSerializer
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response({"user": serializer.data})