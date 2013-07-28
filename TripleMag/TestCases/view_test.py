#coding=utf-8
from django.test import TestCase,Client
from TripleMag.apps.member.models import *

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse

from TripleMag.apps.views import *


class TestSqlView(TestCase):
    def test1(self):
        response = self.client.get(reverse("test"))
        self.assertEquals(response.status_code,302)
