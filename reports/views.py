from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, DetailView
from reports.forms import ReportForm, ReportPhotoForm
from reports.models import TurtleReport, TurtleReportPhoto


class CreateReportView(CreateView):
    model = TurtleReport
    form_class = ReportForm

    def get_success_url(self):
        return reverse('report', args=(self.object.uid,))


class ReportView(DetailView):
    model = TurtleReport
    slug_field = 'uid'


class CreateReportPhotoView(CreateView):
    model = TurtleReportPhoto
    form_class = ReportPhotoForm

    def dispatch(self, request, *args, **kwargs):
        self.report = get_object_or_404(TurtleReport, uid=self.kwargs['slug'])
        return super(CreateReportPhotoView, self).dispatch(request, *args,
                                                           **kwargs)

    def form_valid(self, form):
        form.instance.report = self.report
        return super(CreateReportPhotoView, self).form_valid(form)


    def get_success_url(self):
        return reverse('report', args=(self.object.report.uid,))


