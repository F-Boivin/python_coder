from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .models import Libro
from .forms import LibroForm


class LibroCreateView(CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro_form.html'
    success_url = reverse_lazy('libro-list')

    def form_valid(self, form):
        return super().form_valid(form)


class LibroUpdateView(UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libro_form.html'
    success_url = reverse_lazy('libro-list')

    def form_valid(self, form):
        return super().form_valid(form)
