from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ContactFormSerializer, GeneralInquirySerializer
from .models import ContactForm, GeneralInquiry

# Create your views here.

class ContactFormView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access
    
    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            # Save the contact form data
            contact = serializer.save()
            
            # Prepare email content
            subject = f'Nueva solicitud de empresa para colaborar: {contact.nombre_empresa}'
            message = f"""
            Nueva solicitud de empresa interesada en colaborar:
            
            Empresa: {contact.nombre_empresa}
            Email: {contact.email}
            Teléfono: {contact.telefono}
            Provincia: {contact.provincia}
            
            Mensaje:
            {contact.mensaje}
            
            Fecha de envío: {contact.fecha_envio}
            """
            
            # Send email
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,  # From email
                    [settings.EMAIL_HOST_USER],  # To email (same as from)
                    fail_silently=False,
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {'error': 'Error al enviar el email'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GeneralInquiryView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access
    
    def post(self, request):
        serializer = GeneralInquirySerializer(data=request.data)
        if serializer.is_valid():
            # Save the inquiry data
            inquiry = serializer.save()
            
            # Prepare email content
            subject = 'Nueva consulta general'
            message = f"""
            Nueva consulta general recibida:
            
            Email: {inquiry.email}
            
            Mensaje:
            {inquiry.mensaje}
            
            Fecha de envío: {inquiry.fecha_envio}
            """
            
            # Send email
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,  # From email
                    [settings.EMAIL_HOST_USER],  # To email (same as from)
                    fail_silently=False,
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {'error': 'Error al enviar el email'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
