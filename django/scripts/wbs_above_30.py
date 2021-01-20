from project.models import Project


def run():
    print('Scanning for projects that have WBS longer than 30 characters')
    for p in Project.objects.all():
        if 'wbs' in p.data and len(p.data['wbs']) > 30:
            print(p.id)
        if 'wbs' in p.draft and len(p.draft['wbs']) > 30:
            print(f'draft ID: {p.id}')
    print('Scanning finished')
