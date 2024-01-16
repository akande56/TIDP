import random
from django.utils.text import slugify
from django.conf import settings
from django.template.response import TemplateResponse
import datetime


def slugify_instance_unit(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        # auto generate new slug
        rand_int = random.randint(300_000, 500_000)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_unit(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance



def suglify_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_unit(instance, save=False)


def suglify_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_unit(instance, save=True)


