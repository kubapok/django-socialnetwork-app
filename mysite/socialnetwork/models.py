from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Friendship(models.Model):
    friends = models.ManyToManyField(User)

    def create_friendship(user1, user2):
        friendship = Friendship()
        friendship.save()
        friendship.friends.add(user1.pk,user2.pk)

    def are_friends(user1, user2):
        return Friendship.objects.filter(friends=user1).filter(friends=user2).exists()

    def friends_of(user1):
        return [u.friends.exclude(username =user1.username).get() for u in user1.friendship_set.all()]



class FriendshipRequest(models.Model):
    creator = models.ForeignKey(User, related_name="friendship_created")
    requested = models.ForeignKey(User, related_name="friendship_requested")
    answer = models.NullBooleanField(default=True)

    def is_already_asked_by(user1,user2):
        return FriendshipRequest.objects.filter(creator=user1, requested=user2, answer=None).exists()

    def unanswered_requests_of(user1):
        return FriendshipRequest.objects.filter(requested=user1, answer=None,)

    def is_any_unanswered(user1):
        return True if len(FriendshipRequest.unanswered_requests_of(user1)) else False
