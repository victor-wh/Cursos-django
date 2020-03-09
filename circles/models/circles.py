from django.db import models

# utils
from users.models.users import CRideModel

class Circle(CRideModel):
    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)

    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)

    # status
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(
        'verified circle',
        default=False,
    )

    is_public = models.BooleanField(
        default=True,
    )
    is_limited = models.BooleanField(
        'limited',
        default=False,
        help_text='limited circles'
    )
    members_limit = models.PositiveIntegerField(
        default=0,
        help_text='Si el circulo tiene limite',
    )

    def __str__(self):
        return self.name

    class Meta(CRideModel.Meta):
        ordering = ['-rides_taken','-rides_offered']
