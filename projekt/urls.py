from django.urls import path, include
from django.contrib.auth import views as django_auth_views
from .views.auth_views import MyLoginView
from .views.facilitator_views import ScenarioView, CreateScenarioView, ScenarioDetailView, CreateCriteriaView
from .views import index as views

new_urls = [
    path("", views.index, name="index"),
    path("accounts/login/", MyLoginView.as_view(), name="login"),
    path('logout/', django_auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('scenarios/', ScenarioView.as_view(), name='scenarios'),
    path('scenarios/add', CreateScenarioView.as_view(), name='add_scenario'),
    path('scenarios/view/<pk>', ScenarioDetailView.as_view(), name='scenario-detail'),
    path('scenarios/<pk>/modify', CreateCriteriaView.as_view(), name='modify-criteria')
]
urlpatterns = new_urls