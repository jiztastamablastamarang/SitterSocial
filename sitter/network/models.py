from django.db import models
from django.utils import timezone
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Post(models.Model):
    text = models.TextField(max_length=512)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='author')

    def __str__(self):
        return str(self.text)


class VoteManager(models.Manager):

    def get_likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def get_dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def test(self, *args, **kwargs):
        return self.get_queryset().filter(**kwargs)


class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = [
        (LIKE, 'like'),
        (DISLIKE, 'dislike')
    ]
    vote = models.SmallIntegerField(choices=VOTES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')

    objects = VoteManager()

