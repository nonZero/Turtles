from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.http.response import HttpResponse
from reports.views import CreateReportView, ReportView, CreateReportPhotoView

urlpatterns = [
                  url(r'^add/$', CreateReportView.as_view()),
                  url(r'^report/(?P<slug>[a-z\d]+)/$',
                      ReportView.as_view(), name='report'),
                  url(r'^report/(?P<slug>[a-z\d]+)/add-photo/$',
                      CreateReportPhotoView.as_view(), name="upload"),


                  url(r'^admin/', include(admin.site.urls)),
              ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)
