from django.db import models
from django.utils.text import slugify
from django import template

import misaka
# Create your models here.

from django.contrib.auth import get_user_model

User = get_user_model()

register = template.Library()


class Org(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']

class OrgMember(models.Model):
    org = models.ForeignKey(Org, related_name='memberships')
    user = models.ForeignKey(User, related_name='user_orgs')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
