from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView

from . import forms
from . import models


class CreateObservationView(CreateView):
    model = models.TurtleObservation
    form_class = forms.ObservationForm


class ObservationDetailView(DetailView):
    model = models.TurtleObservation
    slug_field = 'uid'


class CreateObservationPhotoView(CreateView):
    model = models.TurtleObservationPhoto
    form_class = forms.PhotoForm

    def dispatch(self, request, *args, **kwargs):
        self.ob = get_object_or_404(models.TurtleObservation,
                                    uid=self.kwargs['slug'])
        return super(CreateObservationPhotoView, self).dispatch(request, *args,
                                                                **kwargs)

    def form_valid(self, form):
        form.instance.ob = self.ob
        return super(CreateObservationPhotoView, self).form_valid(form)


    def get_success_url(self):
        return self.object.ob.get_absolute_url()
