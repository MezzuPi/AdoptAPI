from django.urls import path
from .views import ContactFormView, GeneralInquiryView

urlpatterns = [
    path('empresa/', ContactFormView.as_view(), name='contacto-empresa'),
    path('consulta/', GeneralInquiryView.as_view(), name='consulta-general'),
] 