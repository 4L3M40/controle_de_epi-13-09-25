from django.urls import path
from .views import EpiListView, EpiCreateView, EpiUpdateView, EpiDeleteView

app_name = "epis"

urlpatterns = [
    path("", EpiListView.as_view(), name="list"),
    path("novo/", EpiCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", EpiUpdateView.as_view(), name="update"),
    path("<int:pk>/excluir/", EpiDeleteView.as_view(), name="delete"),
]
