from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from tutorial.quickstart.serializers import UserSerializer
import redis

from example.models import User, Todo


# Create your views here.
class AddUser(APIView):
    def post(self, request):
        print(request.data)
        age = request.data.get('age')
        if age is None:
            return Response({'error': 'age is required'}, status=status.HTTP_400_BAD_REQUEST)

        name = request.data.get('name')
        if name is None:
            return Response({'error': 'name is required'}, status=status.HTTP_400_BAD_REQUEST)

        print("here")
        user = User(name=name, age=age)
        user.save()

        r = redis.Redis(
            host='redis-11483.c212.ap-south-1-1.ec2.redns.redis-cloud.com',
            port=11483,
            decode_responses=True,
            username="default",
            password="P4zWn9Lb6DXx5saJ2aIFTGFbhSJ60x3Q",
        )

        r.set('foo', 'bar')
        # True

        result = r.get('foo')
        print(result)
        # >>> bar

        print("there")

        return Response({'message': 'success'}, status=status.HTTP_200_OK)


class AddTodo(APIView):
    def post(self, request):
        title = request.data.get('title')
        if title is None:
            return Response({'error': 'title is required'}, status=status.HTTP_400_BAD_REQUEST)

        content = request.data.get('content')
        if content is None:
            return Response({'error': 'content is required'}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.data.get('user_id')
        if user_id is None:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        if user is None:
            return Response({'error': 'invalid user'}, status=status.HTTP_404_NOT_FOUND)

        todo = Todo(title=title, content=content, user=user)

        todo.save()

        return Response(data={'message': 'success'}, status=status.HTTP_200_OK)


class GetAllUsers(APIView):
    def get(self, request):
        users = User.objects.all().values('id', 'name', 'age')
        data = {}
        user_list = []
        for user in users:
            user_list.append(user)

        data['users'] = user_list
        return Response(data=data, status=status.HTTP_200_OK)


class GetUserTodos(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        if user_id is None:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        if user is None:
            return Response({'error': 'invalid user'}, status=status.HTTP_404_NOT_FOUND)

        todos = Todo.objects.filter(user_id=user_id).all().values('title', 'content')

        data = {}
        todo_list = []

        for todo in todos:
            todo_list.append(todo)

        data["todo_list"] = todo_list

        return Response(data={'message': 'success', 'data': data}, status=status.HTTP_200_OK)
