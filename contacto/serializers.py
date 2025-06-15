from rest_framework import serializers
from .models import ContactForm, GeneralInquiry

class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = ['nombre_empresa', 'email', 'telefono', 'provincia', 'mensaje']

class GeneralInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralInquiry
        fields = ['email', 'mensaje'] 