from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
    bio = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='profile_images')

    def __str__(self):
        return self.user.username


class Poems(models.Model):
    user = models.ForeignKey(User, related_name="poems", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=140)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.title[:30]}..."
        )

    def get_absolute_url(self):
        return reverse('profile_view', kwargs={'pk': self.pk})



def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])  # when logged in, the user has to follow himself also
        user_profile.save()


# Create a Profile for each new user.

post_save.connect(create_profile, sender=User)
