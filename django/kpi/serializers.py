from rest_framework import serializers

from kpi.models import SolutionLog, CountryInclusionLog
from project.models import Portfolio, Solution
from project.serializers import SolutionSerializer


class SolutionKPISerializer(SolutionSerializer):
    class Meta:
        model = Solution
        fields = ('id', 'people_reached', 'phase', 'regions', 'countries', 'problem_statements',
                  'open_source_frontier_tech', 'learning_investment', 'portfolios')


class PortfolioKPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id', 'investment_to_date', 'innovation_hub', 'landscape_review',
                  'problem_statements',  'solutions', 'status')


class SolutionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionLog
        fields = ('id', 'date', 'modified', 'data')


class SolutionLogDataSerializer(serializers.Serializer):
    portfolios = PortfolioKPISerializer(many=True)
    solutions = SolutionKPISerializer(many=True)


class SolutionLogVerboseSerializer(SolutionLogSerializer):
    data = SolutionLogDataSerializer()


class CountryInclusionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryInclusionLog
        fields = ('id', 'date', 'modified', 'data')


class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    countries = serializers.IntegerField()
    max_countries = serializers.IntegerField()


class CountryInclusionDataSerializer(serializers.Serializer):
    regions = RegionSerializer(many=True)
    countries = serializers.IntegerField()
    max_countries = serializers.IntegerField()


class CountryInclusionVerboseSerializer(CountryInclusionLogSerializer):
    data = CountryInclusionDataSerializer()
