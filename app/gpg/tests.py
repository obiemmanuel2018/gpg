
from rest_framework import status
from django.test import TestCase
import gnupg
from rest_framework import status
import os
from django.urls import reverse
# Create your tests here.


class DecryptMessageTest(TestCase):
    gpg = gnupg.GPG(os.popen("which gpg").read().strip())
    unencrypted_string = 'Who are you? How did you get in my house?'
    email = 'testgpguser@mydomain.com'
    passphrase = 'my passphrase'

    def genKey(self):

        input_data = self.gpg.gen_key_input(
            name_email=self.email,
            passphrase=self.passphrase)
        self.gpg.gen_key(input_data)

    def encryptMessage(self):

        encrypted_data = self.gpg.encrypt(
            self.unencrypted_string, self.email)
        encrypted_string = str(encrypted_data)
        return encrypted_string

    def decryptMessage(self):

        url = reverse('gpg:decryptMessage')
        self.genKey()
        encrypted_string = self.encryptMessage()
        data = {'message': encrypted_string, 'passphrase': self.passphrase}
        response = self.client.post(url, data, format='json')
        return response

    def test_decrypt_message(self):
        response = self.decryptMessage()
        if response.status_code == status.HTTP_200_OK:
            print('pass')
        else:
            print('fail')
            print(response.error)

        assert response.status_code == status.HTTP_200_OK
