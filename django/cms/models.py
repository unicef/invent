import itertools
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from core.models import ExtendedModel
from user.models import UserProfile


class StateManager(models.QuerySet):
    def normal(self):
        return self.filter(state=State.NORMAL)

    def flagged(self):
        return self.filter(state=State.FLAGGED)

    def banned(self):
        return self.filter(state=State.BANNED)

    def showable(self):
        return self.exclude(state=State.BANNED)


class State(ExtendedModel):
    NORMAL = 1
    FLAGGED = 2
    BANNED = 3

    STATE_CHOICES = (
        (NORMAL, _("Normal")),
        (FLAGGED, _("Flagged")),
        (BANNED, _("Banned")),
    )

    state = models.IntegerField(choices=STATE_CHOICES, default=NORMAL)

    objects = StateManager.as_manager()

    class Meta:
        abstract = True

    def flag(self):
        self.state = self.FLAGGED
        self.save()

    def ban(self):
        self.state = self.BANNED
        self.save()

    def normalize(self):
        self.state = self.NORMAL
        self.save()


class Post(State):
    RESOURCE = 1
    LESSON = 2
    EXPERIENCE = 3

    TYPE_CHOICES = (
        (RESOURCE, _("Resources")),
        (LESSON, _("Lessons & Tips")),
        (EXPERIENCE, _("Experiences")),
    )

    DOMAIN_CHOICES = (
        (1, _("Parameters of Scale")),
        (2, _("Contextual Environment")),
        (3, _("Scientific Basis")),
        (4, _("Strategic Engagement")),
        (5, _("Partnership Sustainability")),
        (6, _("Financial Management")),
        (7, _("Financial Model")),
        (8, _("Data")),
        (9, _("Interoperability")),
        (10, _("Adaptability")),
        (11, _("Personnel")),
        (12, _("Training and Support")),
        (13, _("Outreach and Sensitization")),
        (14, _("Contingency Planning")),
        (15, _("Process Monitoring")),
        (16, _("Evaluation Research")),
    )

    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, max_length=140)
    body = models.TextField(max_length=5000)
    type = models.IntegerField(choices=TYPE_CHOICES)
    domain = models.IntegerField(choices=DOMAIN_CHOICES)
    cover = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(UserProfile, null=True, on_delete=models.SET(UserProfile.get_sentinel_user))

    class Meta:
        verbose_name = "Planning & Guidance post"
        verbose_name_plural = "Planning & Guidance posts"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        for counter in itertools.count(1):
            if not Post.objects.filter(slug=self.slug).exists():
                break

            self.slug = '%s--%d' % (self.slug.rsplit('--', 1)[0], counter)

        super(Post, self).save(*args, **kwargs)


class Comment(State):
    text = models.TextField(max_length=5000)
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET(UserProfile.get_sentinel_user))
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text
