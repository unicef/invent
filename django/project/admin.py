import csv

from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core import mail
from django.utils.html import mark_safe
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from allauth.account.models import EmailAddress
from core.admin import AllObjectsAdmin
from country.models import Country
from .models import TechnologyPlatform, DigitalStrategy, HealthFocusArea, \
    HealthCategory, HSCChallenge, ProjectImport, Project, HSCGroup, \
    ImportRow, UNICEFGoal, UNICEFResultArea, UNICEFCapabilityLevel, UNICEFCapabilityCategory, \
    UNICEFCapabilitySubCategory
from user.models import UserProfile, Organisation

# This has to stay here to use the proper celery instance with the djcelery_email package
import scheduler.celery # noqa


class ViewOnlyPermissionMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



class TechnologyPlatformAdmin(AllObjectsAdmin):
    list_display = [
        'name',
    ]


class ParentFilter(admin.SimpleListFilter):
    title = 'Parent Filter'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        return (
            ('Parent Only', _('Parent Only')),
            ('Children Only', _('Children Only'))
        )
    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        elif self.value() == 'Parent Only':
            return queryset.filter(parent=None)
        else:
            return queryset.exclude(parent=None)

class DigitalStrategyAdmin(ViewOnlyPermissionMixin, AllObjectsAdmin):
    list_filter = [ParentFilter]
    list_display = [
        '__str__'
    ]


class HealthFocusAreaAdmin(ViewOnlyPermissionMixin, AllObjectsAdmin):
    pass


class HealthCategoryAdmin(ViewOnlyPermissionMixin, AllObjectsAdmin):
    pass


class HSCGroupAdmin(ViewOnlyPermissionMixin, AllObjectsAdmin):
    pass


class HSCChallengeAdmin(ViewOnlyPermissionMixin, AllObjectsAdmin):
    pass


def validate_csv_ext(value):
    if not value.name.endswith('.csv'):
        raise forms.ValidationError('Only CSV format is accepted.')


class ProjectImportUploadForm(forms.ModelForm):
    """ Form for first step """
    csv = forms.FileField(validators=[validate_csv_ext])

    class Meta:
        model = ProjectImport
        fields = ['csv']


class ProjectImportFieldMappingForm(forms.ModelForm):
    """ Form for second step """
    project_name = forms.ChoiceField(choices=[])
    owner_name = forms.ChoiceField(choices=[])
    owner_email = forms.ChoiceField(choices=[])
    organisation = forms.ChoiceField(choices=[], required=False)
    country = forms.ChoiceField(choices=[], required=False)
    description = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super(ProjectImportFieldMappingForm, self).__init__(*args, **kwargs)
        # Make choices out of uploaded csv's header
        choices = [('', '',)] + [(index, value) for index, value in enumerate(self.instance.headers)]
        for name, field in self.fields.items():
            field.choices = choices
            field.initial = self.instance.mapping[name] if name in self.instance.mapping else ''

    class Meta:
        model = ProjectImport
        fields = ['project_name', 'owner_name', 'owner_email', 'organisation', 'country', 'description']


class ProjectImportStatusForm(forms.ModelForm):
    """ Form for third step """

    class Meta:
        model = ProjectImport
        fields = ['status', 'imported', 'failed', 'csv']


class ProjectImportAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created', 'status']
    _users_to_notify = {}
    _projects_created = []

    def get_queryset(self, request):
        qs = super(ProjectImportAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        # First step, upload csv
        if not obj:
            kwargs['form'] = ProjectImportUploadForm
            self.readonly_fields = []
        # Second step, map fields
        elif obj.status is None:
            kwargs['form'] = ProjectImportFieldMappingForm
            self.readonly_fields = ['csv']
        # Third step, showing results
        elif obj.status is not None:
            kwargs['form'] = ProjectImportStatusForm
            self.readonly_fields = ['status', 'imported', 'failed', 'csv']
        return super(ProjectImportAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        # Save uploaded CSV and get headers
        if not change:
            obj.user = request.user
            # save the file so that we can read headers
            obj.save()
            with open(obj.csv.path, 'r') as f:
                reader = csv.reader(f)
                obj.headers = next(reader)
            obj.save()
        # Save field mapping and import projects
        elif obj.status is None:
            obj.mapping = form.cleaned_data
            obj.save()
            with open(obj.csv.path, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # skip header
                for line_no, row in enumerate(reader, start=1):  # True line number
                    if self._is_row_valid(row, line_no, obj):
                        self._import_project(row, obj)
            # Set status
            if obj.failed:
                obj.status = False
            else:
                obj.status = True
            obj.save()

            # Notify users
            if self._projects_created:
                self._notify_users()

            # Notify superusers
            self._notify_superusers()

    def _notify_users(self):
        html_template = loader.get_template('email/master-inline.html')
        for user, data in self._users_to_notify.items():
            html_message = html_template.render({'type': 'project_import_notify_owner',
                                                 'email': user.email,
                                                 'data': data,
                                                 'language': user.userprofile.language})
            mail.send_mail(
                subject="You were added to imported projects",
                message="",
                from_email=settings.FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message)

    def _notify_superusers(self):
        superusers_emails = User.objects.filter(is_superuser=True).values_list('email')
        html_template = loader.get_template("email/master-inline.html")
        html_message = html_template.render({'type': 'project_import_notify_admins',
                                             'projects': self._projects_created,
                                             'language': 'en'})

        mail.send_mail(
            subject='New projects have been imported',
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=superusers_emails,
            html_message=html_message,
            fail_silently=True)

    def _is_row_valid(self, row, line_no, project_import):
        valid = True
        # Validate owner email
        owner_email_col = int(project_import.mapping['owner_email'])
        try:
            validate_email(row[owner_email_col])
        except ValidationError as e:
            # Log failure
            project_import.failed += 'Line {}, {}: {}\n'.format(line_no, row[owner_email_col] or '<Empty>', e.message)
            project_import.save()
            valid = False

        # Validate country
        if project_import.mapping['country']:
            country_col = int(project_import.mapping['country'])
            country = Country.objects.get_object_or_none(name=row[country_col])
            if not country:
                project_import.failed += 'Line {}, {}: {}\n'.format(line_no, row[country_col] or '<Empty>',
                                                                    'No such country.')
                project_import.save()
                valid = False

        return valid

    def _import_project(self, row, project_import):
        project_name_col = int(project_import.mapping['project_name'])
        project = Project.objects.create(name=row[project_name_col], draft={'name': row[project_name_col]})

        # Organisation
        if project_import.mapping['organisation']:
            organisation_col = int(project_import.mapping['organisation'])
            organisation, _ = Organisation.objects.get_or_create(name=row[organisation_col])
            project.draft.update(organisation=organisation.id, organisation_name=organisation.name)
        else:
            organisation = None

        # Country
        if project_import.mapping['country']:
            country_col = int(project_import.mapping['country'])
            country = Country.objects.get(name=row[country_col])
            project.draft.update(country=country.id, country_name=country.name)
        else:
            country = None

        # Description
        if project_import.mapping['description']:
            description_col = int(project_import.mapping['description'])
            project.draft.update(implementation_overview=row[description_col])

        # Add user, assign to team
        owner_name_col = int(project_import.mapping['owner_name'])
        owner_email_col = int(project_import.mapping['owner_email'])
        user_qs = User.objects.filter(email=row[owner_email_col])
        user = user_qs.first() if user_qs.exists() else None
        password = None
        if not user:
            user, password = self._create_user(row[owner_email_col], row[owner_name_col], country, organisation)
        project.team.add(user.userprofile)

        project.save()

        # Log success
        project_import.imported += '{}\n'.format(project.name)
        project_import.save()

        # Append to projects created
        self._projects_created.append(project)

        # Gather notification data
        if user in self._users_to_notify:
            self._users_to_notify[user]['projects'].append(project)
        else:
            self._users_to_notify[user] = {
                'password': password,
                'projects': [project]
            }

    def _create_user(self, email, name, country=None, organisation=None):
        user = User.objects.create(username=email, email=email, is_active=True)
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)
        UserProfile.objects.create(account_type=UserProfile.IMPLEMENTER, user=user, name=name,
                                   organisation=organisation, country=country)
        user.refresh_from_db()
        return user, password


class ProjectAdmin(AllObjectsAdmin):
    list_display = ['__str__', 'created', 'get_country', 'get_team', 'get_published', 'is_active']
    readonly_fields = ['name', 'team', 'viewers', 'link', 'odk_etag', 'odk_id', 'odk_extra_data']
    fields = ['is_active', 'name', 'team', 'viewers', 'link', 'odk_etag', 'odk_id', 'odk_extra_data']
    search_fields = ['name']

    def get_country(self, obj):
        return obj.get_country() if obj.public_id else obj.get_country(draft_mode=True)
    get_country.short_description = "Country"

    def get_team(self, obj):
        return ", ".join([str(p) for p in obj.team.all()])
    get_team.short_description = 'Team members'

    def get_published(self, obj):
        return True if obj.public_id else False
    get_published.short_description = "Is published?"
    get_published.boolean = True

    def link(self, obj):
        if obj.id is None:
            return '-'
        version = 'publish' if obj.public_id else 'draft'
        return mark_safe("<a target='_blank' href='/app/{}/edit-project/{}/'>See project</a>"
                         .format(obj.id, version))

    def get_queryset(self, request):
        qs = super(ProjectAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            country_id_qs = Country.objects.filter(users=request.user.userprofile).values_list('id', flat=True)
            qs = qs.filter(Q(data__country__contained_by=list(country_id_qs)) |
                           Q(draft__country__contained_by=list(country_id_qs)))
        return qs

    def has_add_permission(self, request):
        return False


class ImportRowInline(admin.StackedInline):
    model = ImportRow
    readonly_fields = ('data',)


class ProjectImportV2Admin(admin.ModelAdmin):
    inlines = (ImportRowInline,)


class UNICEFGoalAdmin(admin.ModelAdmin):
    pass


class UNICEFResultAreaAdmin(admin.ModelAdmin):
    ordering = search_fields = ['goal_area__name', 'name']


class UNICEFCapabilityLevelAdmin(admin.ModelAdmin):
    ordering = search_fields = ['goal_area__name', 'name']


class UNICEFCapabilityCategoryAdmin(admin.ModelAdmin):
    ordering = search_fields = ['goal_area__name', 'name']


class UNICEFCapabilitySubCategoryAdmin(admin.ModelAdmin):
    ordering = search_fields = ['goal_area__name', 'name']


admin.site.register(TechnologyPlatform, TechnologyPlatformAdmin)
admin.site.register(DigitalStrategy, DigitalStrategyAdmin)
admin.site.register(HealthFocusArea, HealthFocusAreaAdmin)
admin.site.register(HealthCategory, HealthCategoryAdmin)
admin.site.register(HSCGroup, HSCGroupAdmin)
admin.site.register(HSCChallenge, HSCChallengeAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(UNICEFGoal, UNICEFGoalAdmin)
admin.site.register(UNICEFResultArea, UNICEFResultAreaAdmin)
admin.site.register(UNICEFCapabilityLevel, UNICEFCapabilityLevelAdmin)
admin.site.register(UNICEFCapabilityCategory, UNICEFCapabilityCategoryAdmin)
admin.site.register(UNICEFCapabilitySubCategory, UNICEFCapabilitySubCategoryAdmin)
