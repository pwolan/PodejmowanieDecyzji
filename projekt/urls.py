from django.urls import path
from django.contrib.auth import views as django_auth_views
from .views.auth_views import MyLoginView, MyRegisterView
from .views.facilitator.criterias import CreateCriteriaView, DeleteCriteriaView
from .views.facilitator.scenario import ScenarioView, CreateScenarioView, ScenarioDetailView, ScenarioSubmitView, ScenarioEndView, generate_json
from .views.facilitator.alternatives import CreateAlternativesView, DeleteAlternativesView
from .views.expert.index import QuestionareView, QuestionareCriteriumView, QuestionareEndView
from .views.expert.panel import ExpertPanel
from .views import index as views



new_urls = [
    path("", views.index, name="index"),
    path("accounts/login/", MyLoginView.as_view(), name="login"),
    path("accounts/register/", MyRegisterView.as_view(), name="register"),
    path('logout/', django_auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('scenarios/', ScenarioView.as_view(), name='scenarios'),
    path('scenarios/add', CreateScenarioView.as_view(), name='add_scenario'),
    path('scenarios/view/<pk>', ScenarioDetailView.as_view(), name='scenario-detail'),
    path('scenarios/view/<pk>/generate_json_file', generate_json, name='generate_json_file'),
    path('scenarios/<pk>/criterias/modify', CreateCriteriaView.as_view(), name='modify-criteria'),
    path('scenarios/<scenarioId>/criterias/modify/<pk>/delete', DeleteCriteriaView.as_view(), name='delete-criteria'),
    path('scenarios/<pk>/alternatives/modify', CreateAlternativesView.as_view(), name='modify-alternatives'),
    path('scenarios/<scenarioId>/alternatives/modify/<pk>/delete', DeleteAlternativesView.as_view(), name='delete-alternatives'),
    path('scenarios/<pk>/submit', ScenarioSubmitView.as_view(), name='scenario-submit'),
    path('scenarios/<pk>/end', ScenarioEndView.as_view(), name='scenario-end'),
    path('panel/', ExpertPanel.as_view(), name='expert-panel'),
    path('questionare/<str:url>', QuestionareView.as_view(), name='questionare'),
    path('questionare/end/<str:url>', QuestionareEndView.as_view(), name='questionare-end'),
    path('questionare/<url>/<pk>', QuestionareCriteriumView.as_view(), name='questionare-criterium'),
]
urlpatterns = new_urls