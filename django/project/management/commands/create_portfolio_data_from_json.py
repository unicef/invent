from __future__ import unicode_literals

from django.core.management.base import BaseCommand
import pprint as pp
import json
from user.models import User, UserProfile, Organisation
from country.models import Donor, Country, CountryOffice
from project.models import Project, Portfolio, ProblemStatement, ProjectPortfolioState, ReviewScore
from project.tests.setup import TestProjectData


class Command(BaseCommand, TestProjectData):
    help = 'Generates test data in the DB based on the input JSON'

    def add_arguments(self, parser):
        parser.add_argument('input_json', type=str)

    @staticmethod
    def read_input_json(input_file):
        with open(input_file, 'r') as f:
            return json.load(f)

    def create_background_data(self, data_dict):
        pp.pprint('Creating background data if needed')
        self.org, _ = Organisation.objects.get_or_create(name=data_dict['organisation'])
        self.d2, _ = Donor.objects.get_or_create(name=data_dict['d1'],
                                                 code=data_dict['d1'].lower().replace(' ', '_'))
        self.d2, _ = Donor.objects.get_or_create(name=data_dict['d2'],
                                                 code=data_dict['d2'].lower().replace(' ', '_'))
        self.country, self.country_office = self.create_new_country_and_office(project_approval=False)

    @staticmethod
    def create_users(users):
        pp.pprint('Creating users if needed')
        profiles_list = []
        for user_data in users:
            user_db, created = User.objects.get_or_create(username=user_data['email'])
            user_db.password = '1234YabbaDabba'
            user_db.save()
            userprofile_db, created = UserProfile.objects.get_or_create(user=user_db)
            userprofile_db.name = user_data['name']
            userprofile_db.global_portfolio_owner = user_data['role'] == "GPO"
            userprofile_db.save()
            pp.pprint(f"{user_data['email']}, created: {created}")
            profiles_list.append(userprofile_db)
        return profiles_list

    def create_projects(self, projects):
        projects_list = []
        for project_data in projects:
            project_gen_data, org, country, country_office, d1, d2 = \
                self.create_test_data(name=project_data['name'], new_country_only=True)

            project_gen_data = project_gen_data['project']
            project_gen_data['date'] = project_gen_data['date'].strftime("%m/%d/%Y, %H:%M:%S")
            country, _ = Country.objects.get_or_create(name=project_data.get('country', "unnamed_country"))
            country_offices = CountryOffice.objects.filter(country=country)

            if country_offices:
                country_office = country_offices[0]
            else:
                CountryOffice.objects.get_or_create(
                    name=f'Test Country Office ({country.name})',
                    region=Country.UNICEF_REGIONS[0][0],
                    country=country
                )

            project_gen_data['country'] = country.id
            project_gen_data['organisation'] = org.id
            project_gen_data['country_office'] = country_office.id

            project, created = Project.objects.get_or_create(name=project_data['name'])
            project_team = UserProfile.objects.filter(name__in=project_data['team'])

            project.team.set(project_team)
            project.data = project_gen_data
            project.make_public_id(self.country.id)
            project.save()

            projects_list.append(project)
            pp.pprint(f"Project: {project}, created: {created}")
        return projects_list

    @staticmethod
    def parse_review_data(portfolio, pps, proj_data, approved=False):
        if 'reviews' in proj_data:
            for review in proj_data['reviews']:
                user = UserProfile.objects.get(name=review['name'])
                user_score, created = ReviewScore.objects.get_or_create(
                    reviewer=user, portfolio_review=pps,
                )
                pp.pprint(f'{user_score}, created: {created}')
                user_score.complete = review['complete'] if 'complete' in review else False
                user_score.rnci = review['rnci'] if 'rnci' in review else None
                user_score.rnci_comment = review['rnci_comment'] if 'rnci_comment' in review else None
                user_score.ratp = review['ratp'] if 'ratp' in review else None
                user_score.ratp_comment = review['ratp_comment'] if 'ratp_comment' in review else None
                user_score.ra = review['ra'] if 'ra' in review else None
                user_score.ra_comment = review['ra_comment'] if 'ra_comment' in review else None
                user_score.ee = review['ee'] if 'ee' in review else None
                user_score.ee_comment = review['ee_comment'] if 'ee_comment' in review else None
                user_score.nst = review['nst'] if 'nst' in review else None
                user_score.nst_comment = review['nst_comment'] if 'nst_comment' in review else None
                user_score.ps = review['ps'] if 'ps' in review else None
                user_score.ps_comment = review['ps_comment'] if 'ps_comment' in review else None
                if 'psa' in review:
                    user_score.psa.set(portfolio.problem_statements.filter(name__in=review['psa']))
                user_score.psa_comment = review['psa_comment'] if 'psa_comment' in review else None
                user_score.save()
        if 'scores' in proj_data:
            pps.psa.set(portfolio.problem_statements.filter(name__in=proj_data['scores']['psa']))
            pps.reviewed = True
            pps.rnci = proj_data['scores']['rnci']
            pps.ratp = proj_data['scores']['ratp']
            pps.nc = proj_data['scores']['nc']
            pps.ra = proj_data['scores']['ra']
            pps.ee = proj_data['scores']['ee']
            pps.nst = proj_data['scores']['nst']
            pps.ps = proj_data['scores']['ps']
            pps.impact = proj_data['scores']['impact']
            pps.scale_phase = proj_data['scores']['scale_phase']
            pps.approved = approved
            pps.save()

    def create_portfolios(self, portfolios):
        for p_data in portfolios:
            portfolio, created = Portfolio.objects.get_or_create(name=p_data['name'])
            pp.pprint(f'{portfolio}, created: {created}')
            portfolio.description = p_data['description']
            portfolio.icon = p_data['icon']
            managers = UserProfile.objects.filter(name__in=p_data['managers'])
            portfolio.managers.set(managers)
            portfolio.status = p_data['status']
            portfolio.save()
            for p_s in p_data['problem_statements']:
                ps, created = ProblemStatement.objects.get_or_create(
                    name=p_s['name'], description=p_s['description'], portfolio=portfolio)
                pp.pprint(f'ProblemStatement: {ps}, created: {created}')
            if 'projects_in_review' in p_data:
                for proj_data in p_data['projects_in_review']:
                    pp_project = Project.objects.get(name=proj_data['name'])
                    pps, created = ProjectPortfolioState.objects.get_or_create(project=pp_project, portfolio=portfolio)
                    pp.pprint(f'ProjectPortfolioState: {pps}, created: {created}')
                    self.parse_review_data(portfolio, pps, proj_data, False)
            if 'projects_approved' in p_data:
                for proj_data in p_data['projects_approved']:
                    pp_project = Project.objects.get(name=proj_data['name'])
                    pps, created = ProjectPortfolioState.objects.get_or_create(project=pp_project, portfolio=portfolio)
                    pp.pprint(f'Approved ProjectPortfolioState: {pps}, created: {created}')
                    self.parse_review_data(portfolio, pps, proj_data, True)

    def handle(self, *args, **options):
        pp.pprint('Parsing input data')

        data = self.read_input_json(options.get('input_json'))
        general = data['general']
        users = data['users']
        projects = data['projects']
        portfolios = data['portfolios']
        self.create_background_data(general)
        self.create_users(users)
        self.create_projects(projects)
        self.create_portfolios(portfolios)
