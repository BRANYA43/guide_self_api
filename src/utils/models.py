from uuid import uuid4

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(
        verbose_name='UUID',
        primary_key=True,
        default=uuid4,
        db_index=True,
        editable=False,
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=100,
        unique=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='Updated at',
        auto_now=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Created at',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
