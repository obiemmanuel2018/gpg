from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import GpgSerializer
import gnupg
import os
# Create your views here.


@api_view(['POST'])
def decryptMessage(request):
    gpg = gnupg.GPG(os.popen("which gpg").read().strip())
    if not request.data.get('message') and not request.data.get('passphrase'):
        return Response({
            'error': "please provide a message and a passphrase"
        }, status=status.HTTP_400_BAD_REQUEST)
    if not request.data.get('message'):
        return Response({
            'error': "please provide a message"
        }, status=status.HTTP_400_BAD_REQUEST)
    if not request.data.get('passphrase'):
        return Response({
            'error': "please provide a passphrase"
        }, status=status.HTTP_400_BAD_REQUEST)

    gpgserializer_data = GpgSerializer(request.data)

    if gpgserializer_data.is_valid:
        message = gpgserializer_data.data.get('message')
        passphrase = gpgserializer_data.data.get('passphrase')

        decrypted_data = gpg.decrypt(str(message), passphrase=passphrase)
        if decrypted_data.ok:
            decrypted_string = str(decrypted_data)
            return Response({
                "DecryptedMessage": "The given message '{}', decrypted using GPG and the given passphrase '{}'".format(decrypted_string, passphrase)
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': decrypted_data.stderr,
                'message': message,
                'passphrase': passphrase
            }, status=status.HTTP_403_FORBIDDEN)
