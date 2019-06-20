from rest_framework import serializers


class MapResultSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField(source="project_id")
    name = serializers.ReadOnlyField(source="project__name")
    organisation = serializers.ReadOnlyField(source="organisation_id")
    country = serializers.ReadOnlyField(source="country_id")
    approved = serializers.ReadOnlyField(source="project__approval__approved")


class ListResultSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField(source="project_id")
    name = serializers.ReadOnlyField(source="project__name")
    organisation = serializers.ReadOnlyField(source="organisation_id")
    country = serializers.ReadOnlyField(source="country_id")
    implementation_overview = serializers.ReadOnlyField(source="project__data__implementation_overview")
    contact_name = serializers.ReadOnlyField(source="project__data__contact_name")
    contact_email = serializers.ReadOnlyField(source="project__data__contact_email")
    platforms = serializers.ReadOnlyField(source="project__data__platforms")
    health_focus_areas = serializers.ReadOnlyField(source="project__data__health_focus_areas")
    hsc_challenges = serializers.ReadOnlyField(source="project__data__hsc_challenges")
    region = serializers.ReadOnlyField(source="country__region")
    donors = serializers.ReadOnlyField()
    approved = serializers.ReadOnlyField(source="project__approval__approved")
    country_custom_answers = serializers.ReadOnlyField(source="project__data__country_custom_answers")
    country_custom_answers_private = serializers.ReadOnlyField(source="project__data__country_custom_answers_private")
    donor_custom_answers = serializers.ReadOnlyField(source="project__data__donor_custom_answers")
    donor_custom_answers_private = serializers.SerializerMethodField()

    def get_donor_custom_answers_private(self, obj):
        private_fields = obj.get("project__data__donor_custom_answers_private")
        if private_fields and self.context['donor']:
            return {donor_id: private_fields[donor_id]
                    for donor_id in private_fields if donor_id == str(self.context['donor'].id)}
