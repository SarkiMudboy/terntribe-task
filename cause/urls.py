from django.urls import path
from .views import CauseView

cause_list = CauseView.as_view({"get": "list", "post": "create"})
cause_detail = CauseView.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "delete": "destroy",
    }
)
cause_contribution = CauseView.as_view({"post": "contribute"})


urlpatterns = [
    path("", cause_list, name="cause-list"),
    path("<str:id>/", cause_detail, name="cause_detail"),
    path("<str:id>/contribute/", cause_contribution, name="cause_contribute"),
]
