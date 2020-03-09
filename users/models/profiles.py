'''profile model'''

from django.db import models

# cuando se usa un directorio solo se llama la aplicacion
from users import CRideModel

class Profile(CRideModel):
    '''Profile Model'''

    user = models.OneToOneField('users.User',on_delete=models.CASCADE)

    picture = models.ImageField(
        'profile_picture',
        upload_to='users/pictures/',
        blank=True,
        null=True,
    )
    biography = models.TextField(max_length=500, blank=True)

    # stats

    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)
    reputation = models.FloatField(
        default = 5.0,
        help_text = 'Reputacion del usuario',
    )

    def __str__(self):
        '''Regresa user str'''
        return str(self.user)