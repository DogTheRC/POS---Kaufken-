from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from app.reportes.forms import ReportForm
# Create your views here.
class reportVentaView(TemplateView):
    template_name = 'report_venta.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Ventas'
        context['entity'] = "Reportes"
        context['list_url'] = reverse_lazy('reportes:reporteVenta')
        context['form'] = ReportForm()
        return context