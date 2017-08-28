#coding:utf-8
from django.contrib.contenttypes.models import ContentType
from secretballot.models import Vote

from cclikes.signals import likes_enabled_test, can_vote_test
from cclikes.exceptions import LikesNotEnabledException, CannotVoteException

def _votes_enabled(obj):
    return hasattr(obj.__class__, 'votes')

def likes_enabled(obj, request):
    if not _votes_enabled(obj):
        return False
    try:
        likes_enabled_test.send(
            sender=obj.__class__,
            instance=obj,
            request=request
        )
    except LikesNotEnabledException:
        return False
    return True

def can_vote(obj, user, request):
    if not _votes_enabled(obj):
        return False

    if Vote.objects.filter(
            object_id=obj.id,
            content_type=ContentType.objects.get_for_models(obj),
            token=request.secretballot_token
    ).exists():
        return False

    if request.secretballot_token is None:
        return False

    try:
        can_vote_test.send(
            sender=obj.__class__,
            instance=obj,
            user=user,
            request=request
        )
    except CannotVoteException:
        return False
    return True