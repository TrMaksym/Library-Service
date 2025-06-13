
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Library.models import Book
from Library.serializers import UserSerializer, BorrowingSerializer
from user.models import Borrowing


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class BorrowingsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data["Book_id"]

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book does not exist"}, status=400)

        if book.Inventory == 0:
            return Response({"error": "Book inventory is empty"}, status=400)

        book.Inventory -= 1
        book.save()

        borrowing = serializer.save()

        return Response(self.get_serializer(borrowing).data, status=201)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_id = request.query_params.get("user_id", None)
        is_active = request.query_params.get("is_active", None)

        if user_id:
            queryset = queryset.filter(User_id=user_id)
        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(Actual_return__isnull=True)
            elif is_active.lower() == "false":
                queryset = queryset.filter(Actual_return__isnull=False)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.Actual_return is not None:
            return Response({"error": "Book is already returned"}, status=400)
        book = Book.objects.get(id=borrowing.Book_id)
        book.Inventory += 1
        book.save()
        borrowing.Actual_return = request.user
        borrowing.save()
        borrowing.Actual_return = timezone.now().date()
        borrowing.save()
        return Response(self.get_serializer(borrowing).data)


class StripeSuccessView(APIView):
    def get(self, request):
        return Response({"message": "Success!"}, status=200)


class StripeCancelView(APIView):
    def get(self, request):
        return Response({"message": "Cancel!"}, status=200)

