from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from milkapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.service_list, name='service_list'),
    path('product/<int:id>/', views.service_detail, name='service_detail'),
    path('orders/', views.orders, name='orders'),
    path('order/', views.create_order, name='create_order'),
    path('new-product/', views.new_service, name='new_service'),
    path('deactivateService/', views.deactivateService, name='deactivateService'),
    path('findProduct/', views.service_list, name='findProduct'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
