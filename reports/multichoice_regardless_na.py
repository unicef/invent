from core.models import CustomNameOrderedQuerySet
from project.models import Project, UNICEFSector, CPD, TechnologyPlatform, HardwarePlatform, NontechPlatform, PlatformFunction


special_names = CustomNameOrderedQuerySet.special_names
fields = {
    'unicef_sector': UNICEFSector,
    'cpd': CPD,
    'platforms': TechnologyPlatform,
    'hardware': HardwarePlatform,
    'nontech': NontechPlatform,
    'functions': PlatformFunction
}
json_fields = [
    'data',
    'draft'
]

for p in Project.objects.all():
    for data_or_draft in json_fields:
        for field, klass in fields.items():
            if field in getattr(p, data_or_draft) and len(getattr(p, data_or_draft)[field]) > 2:
                for item in getattr(p, data_or_draft)[field]:
                    special_ids = klass.objects.filter(name__in=special_names).values_list('id', flat=True)
                    if item in special_ids:
                        print(p.id, p.name, ' | ', field, data_or_draft)
