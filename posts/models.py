# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings

class posts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    body = models.TextField()



    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("detail", kwargs={"id": self.id})
