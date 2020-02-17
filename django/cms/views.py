from collections import defaultdict
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from cms.models import Post, Comment, State
from cms.permissions import IsOwnerOrReadOnly, OnlyAdminForLessons
from cms.serializers import CmsSerializer, CommentSerializer

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery # noqa
from core.utils import send_mail_wrapper


class FlagMixin(object):
    def partial_update(self, request, *args, **kwargs):
        """
        PATCH endpoint used for flagging content (eg: post, comment)
        """
        instance = self.get_object()
        if instance.state == State.NORMAL:
            instance.flag()
            self._notify_admins(instance)
        return Response(dict(detail="Content flagged."), status=status.HTTP_202_ACCEPTED)

    @staticmethod
    def _notify_admins(instance):
        change_url = reverse('admin:cms_{}_change'.format(instance._meta.model_name), args=(instance.id,))

        admins = User.objects.filter(is_superuser=True)
        if admins:
            email_mapping = defaultdict(list)
            for admin in admins:
                try:
                    email_mapping[admin.userprofile.language].append(admin.email)
                except ObjectDoesNotExist:
                    email_mapping[settings.LANGUAGE_CODE].append(admin.email)

            for language, email_list in email_mapping.items():
                send_mail_wrapper(subject="Content has been flagged.",
                                  email_type="flag_content",
                                  to=email_list,
                                  language=language,
                                  context={'change_url': change_url})


class CmsViewSet(FlagMixin, ModelViewSet):
    queryset = Post.objects.showable().order_by('-id')
    serializer_class = CmsSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, OnlyAdminForLessons)

    def perform_create(self, serializer):
        obj = Post()
        for key, value in serializer.validated_data.items():
            setattr(obj, key, value)
        self.check_object_permissions(self.request, obj)
        super(CmsViewSet, self).perform_create(serializer)


class CommentViewSet(FlagMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.showable().order_by('-id')
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
