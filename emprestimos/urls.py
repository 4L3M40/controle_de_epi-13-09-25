from django.urls import path
from .views import EmprestimoListView, EmprestimoCreateView, EmprestimoUpdateView, EmprestimoDeleteView

app_name = "emprestimos"

urlpatterns = [
    path("", EmprestimoListView.as_view(), name="list"),
    path("novo/", EmprestimoCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", EmprestimoUpdateView.as_view(), name="update"),
    path("<int:pk>/excluir/", EmprestimoDeleteView.as_view(), name="delete"),
]