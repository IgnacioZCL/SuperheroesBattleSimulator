"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import BattleSimulatorTest, GenerateTeams, SimulateBattle, csrf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('simulate_battle/', SimulateBattle.as_view(), name="simulate_battle"),
    path('battle_simulator_test/', BattleSimulatorTest.as_view(),
         name="battle_simulator_test"),
    path('generate_teams/', GenerateTeams.as_view(), name="generate_teams"),
    path('get_csrf/', csrf, name="get_csrf")
]
