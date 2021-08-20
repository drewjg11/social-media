from django.db import models
from django.urls import reverse
from django.conf import settings

import misaka

from orgs.models import Org
# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()

class Project(models.Model):
    user = models.ForeignKey(User, related_name='projects')
    created_at = models.DateTimeField(auto_now=True)
    item = models.TextField()
    item_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True)

    def __str__(self):
        return self.item

    def save(self, *args, **kwargs):
        self.item_html = misaka.html(self.item)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username':self.user.username, 'pk':self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']
