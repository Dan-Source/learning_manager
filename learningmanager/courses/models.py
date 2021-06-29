from autoslug import AutoSlugField

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.template.loader import render_to_string

from model_utils.models import TimeStampedModel
from .fields import OrderField


User = get_user_model()


class Subject(models.Model):
    title = models.CharField('Titulo', max_length=200)
    slug = AutoSlugField(
        unique=True, always_update=False, populate_from="title"
    )

    class Meta:
        verbose_name = 'Assunto'
        verbose_name_plural = 'Assuntos'
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"


class Course(TimeStampedModel):
    owner = models.ForeignKey(
        User, related_name='courses_created', on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject, related_name='courses', on_delete=models.CASCADE,
        verbose_name='Assunto'
    )
    title = models.CharField('Titulo', max_length=200)
    slug = AutoSlugField(
        unique=True, always_update=False, populate_from="title")
    overview = models.TextField()
    students = models.ManyToManyField(
        User, related_name='courses_joined', blank=True
    )

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['title']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': (
            'text',
            'video',
            'image',
            'file',
        )})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(TimeStampedModel):
    owner = models.ForeignKey(
        User, related_name='%(class)s_related', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html', {'item': self})


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    url = models.URLField()


class Video(ItemBase):
    url = models.URLField()
