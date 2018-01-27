"""roadmap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # матрица компетенции
    url(r'^(?P<course_id>[0-9]+)/matrix/', views.matrix, name="matrix"),
    # карта траекторий
    url(r'^(?P<course_id>[0-9]+)/graph/', views.graph, name="graph"),
    # ввод данных
    url(r'^create/', views.skill, name="create"),
    url(r'^/', views.index, name="index"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
