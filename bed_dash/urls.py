from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.healthDash, name='rural_health'),
    # url(r'^index/', views.ind, name='index'),

    url(r'^coordinator/', views.coord, name='coordinator'),
    url(r'^role_coordinator/', views.role_coord, name='role_coordinator'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^doctor/', views.doc, name='doctor'),
    url(r'^role_doctor/', views.role_doc, name='role_doctor'),
    url(r'^register/', views.register, name='register'),
    url(r'^last_update/', views.last_up, name='last_update'),
    url(r'^role_register/', views.role_reg, name='role_register'),
    url(r'^observer/', views.obsrvr, name='observer'),

    # path('registe6r', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^xyz/', views.xyz, name='xyz'),
    # url(r'^whatsapp/', views.whatsapp, name='whatsapp'),
    # url(r'^admins/', views.ad, name='admin'),
    url(r'^updatecoord/', views.update_coord, name='updatecoord'),
    url(r'^updatedoc/', views.update_doc, name='updatedoc'),
    # path('upload/', views.upload, name='upload'),
    url(r'^upload/', views.simple_upload, name='upload'),
    # url(r'^show/', views.show, name='show'),
    # url(r'^edit/<int:id>', views.edit, name='edit/<int:id>'),
    # url(r'^update/<int:id>', views.update, name='update'),
    # url(r'^delete/<int:id>', views.destroy, name='destroy'),
    path('emp/', views.emp),  

    path('show/',views.show),  
    path('edit/<int:id>', views.edit),  
    path('update/<int:id>', views.update),  
    path('delete/<int:id>', views.destroy),  
    url(r'^after_admin/', views.adafter, name='after_admin'),
    # url(r'^assign_role/', views.assign, name='assign_role'),
    # url(r'^contribute/', views.contribute, name='contribute'),
    # url(r'^urban_health/', views.UrbanHealth, name='urban_health'),
    # path('trail', views.trialDash, name='trail-dash'),

    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)