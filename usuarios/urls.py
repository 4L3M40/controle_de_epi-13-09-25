from django.urls import path
from . import views
from .views import ColaboradorCreateView, ColaboradorListView, UsuarioLoginView, UsuarioLogoutView, dashboard_view, ColaboradorUpdateView, ColaboradorDeleteView

app_name = "usuarios"

urlpatterns = [
    path("login/", UsuarioLoginView.as_view(), name="login"),
    path("logout/", UsuarioLogoutView.as_view(), name="logout"),
    path("", ColaboradorListView.as_view(), name="list"),
    path("novo/", ColaboradorCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", ColaboradorUpdateView.as_view(), name="update"),
    path("<int:pk>/excluir/", ColaboradorDeleteView.as_view(), name="delete"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path('perfil/editar/', views.perfil_editar_view, name='perfil_editar'),
]