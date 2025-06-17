from django.urls import include, path
from rest_framework.routers import DefaultRouter

from Library.views import BookViewSet, PaymentsViewSet
from user.views import BorrowingsViewSet, StripeSuccessView, StripeCancelView

app_name = "Library"

router = DefaultRouter()
router.register("Book", BookViewSet)
router.register("Borrowing", BorrowingsViewSet)
router.register("Payments", PaymentsViewSet)

urlpatterns = [path("", include(router.urls)),
               path("payments/success/", StripeSuccessView.as_view(), name="stripe-success"),
               path("payments/cancel/", StripeCancelView.as_view(), name="stripe-cancel"),
]
