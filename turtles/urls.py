from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from obs.views import CreateObservationView, ObservationDetailView, \
    CreateObservationPhotoView


urlpatterns = [

    url(r'^add/$', CreateObservationView.as_view()),

    url(r'^ob/(?P<slug>[\w\d]+)/$', ObservationDetailView.as_view(),
        name='ob'),

    url(r'^ob/(?P<slug>[\w\d]+)/add-photo/$',
        CreateObservationPhotoView.as_view(), name="upload"),

    url(r'^admin/', include(admin.site.urls)),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
