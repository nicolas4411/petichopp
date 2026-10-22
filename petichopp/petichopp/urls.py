from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('petis.urls')),  # Inclui as rotas do app petis
    path('financeiro/', include(('financeiro.urls', 'financeiro'), namespace='financeiro')),
]