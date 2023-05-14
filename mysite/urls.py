"""mysite URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static

from personal.views import(
    home_screen_view,
    grouped_screen_view,
    statistic_screen_view,
)

from account.views import(
    logout_view,
    login_view,
)

from documentation.views import(
    documentation_view,
)

from employee.views import(
    profile_screen_view,
)

from playground.views import(
    playground_view,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name = "home"),
    path('grouped/', grouped_screen_view, name = "grouped"),
    path('statistic/', statistic_screen_view, name = "statistic"),
    path('statistic/<str:start_date>/<str:end_date>/<str:group>/<str:chart>/', statistic_screen_view, name = "statistic"),
    path('logout/', logout_view,name = "logout"),
    path('login/', login_view,name = "login"),
    path('documentation/', documentation_view,name = "documentation"),
    path('employee/<int:id>/', profile_screen_view,name = "profile"),
    path(r'^celery-progress/', include('celery_progress.urls')),
    path('playground/', playground_view,name = "playground"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)