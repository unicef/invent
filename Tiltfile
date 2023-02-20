load('ext://helm_resource', 'helm_resource', 'helm_repo')
load('ext://uibutton', 'cmd_button', 'bool_input', 'text_input', 'location')

# Add PostgreSQL Helm resource (https://artifacthub.io/packages/helm/bitnami/postgresql)
helm_repo('bitnami', 'https://charts.bitnami.com/bitnami',labels=['helm-charts'])
helm_repo('codecentric', 'https://codecentric.github.io/helm-charts',labels=['helm-charts'])
helm_resource(
    resource_deps=['bitnami'],
    name='postgres',
    chart='bitnami/postgresql',
    namespace='default',
    flags=[
        '--set=image.tag=10.4.0',
        '--set=auth.enablePostgresUser=true',
        '--set=auth.postgresPassword=postgres'
    ],
    port_forwards=['30011:5432'],
    labels=['database']
)

local_resource(
    name='import-dump',
    resource_deps=['postgres'],
    cmd=['sh', '-c', """
    kubectl cp $HOME/tilt_files/dump_anon.sql postgres-postgresql-0:/tmp/dump_anon.sql
    kubectl exec postgres-postgresql-0 -- psql -U postgres -d postgres -f /tmp/dump_anon.sql
    """],
    allow_parallel=True,
    labels=['database']
    )

helm_resource(
    resource_deps=['bitnami'],
    name='redis',
    chart='bitnami/redis',
    namespace='default',
    flags=[
        '--set=image.tag=4.0.10',
        '--set=master.count=1',
        '--set=replica.replicaCount=0',
        '--set=auth.enabled=false',
        '--set=auth.sentinel=false',
        '--set=cluster.enabled=standalone',
    ],
    labels=['redis']
)

helm_resource(
    resource_deps=['codecentric'],
    name='mailhog',
    chart='codecentric/mailhog',
    namespace='default',
    flags=[
        '--set=auth.enabled=false',
    ],
    port_forwards=['30012:8025'],
    labels=['mailhog']
)

docker_build(
    'localhost:5001/invent-django',
    './',
    dockerfile='Dockerfile.django',
    # only=['./django'],
    live_update=[
        sync('django/', '/src'),
        run('cd /src && pip install -r requirements.txt',
            trigger=['./django/requirements.txt']),
        run('cd /src && python manage.py migrate',
            trigger=['./django/*/migrations']),
    ],
)

yaml = helm(
  './django/helm',
  # The release name, equivalent to helm --name
  name='invent-django',
  # The namespace to install in, equivalent to helm --namespace
  namespace='default',
  # The values file to substitute into the chart.
  values=['./django/helm/values-dev.yaml'],
  )
k8s_yaml(yaml)
k8s_resource(
    'invent-django',
    objects = ['invent-django:ServiceAccount',"invent-django-translations:PersistentVolumeClaim","invent-django-translations-country:PersistentVolumeClaim","invent-django-locale:PersistentVolumeClaim","invent-django-translations-user:PersistentVolumeClaim"],
    pod_readiness='wait',
    labels='backend'
)
k8s_resource(
    'invent-celery',
    resource_deps = ['redis'],
    labels='backend'
)


# Add a button to quickly run a command in a pod
pod_exec_script = '''
    set -eu
    kubectl exec deployment/$deployment -- $command
'''
# Execute Unit Tests
cmd_button('exec_unit_tests',
    argv=['sh', '-c', pod_exec_script],
    resource='invent-django',
    env=[
        'deployment=invent-django',
        'command=/bin/bash run_unit_tests.sh 100',
    ],
    icon_name='check_circle',
    text='Execute Unit Tests',
)

# Create the Super User in Django
cmd_button('exec_create_super_user',
    argv=['sh', '-c', pod_exec_script],
    resource='invent-django',
    env=[
        'deployment=invent-django',
        'command=echo "from django.contrib.auth.models import User; User.objects.create_superuser(\'admin_test12345\', \'admin_test12345@example.com\', \'12345\')" | python manage.py shell',
    ],
    icon_name='check_circle',
    text='Create the Super User',
)

# Run the django migrations
cmd_button('exec_migrate',
    argv=['sh', '-c', pod_exec_script],
    resource='invent-django',
    env=[
        'deployment=invent-django',
        'command=python manage.py migrate --noinput',
    ],
    icon_name='check_circle',
    text='Run the django migrations',
)

############# FE Tilt Configuration ##################

docker_build(
    'localhost:5001/invent_nginx',
    './',
    dockerfile='Dockerfile.nginx',
)

docker_build(
    'localhost:5001/invent_frontend',
    './',
    dockerfile='Dockerfile.frontend',
)

yaml = helm(
    './frontend/helm',
    # The release name, equivalent to helm --name
    name='invent-frontend',
    # The namespace to install in, equivalent to helm --namespace
    namespace='default',
    # The values file to substitute into the chart.
    values=['./frontend/helm/values-dev.yaml'],
    # Values to set from the command-line
    set=['ingress.enabled=false']
  )
k8s_yaml(yaml)

k8s_resource(
    'invent-frontend',
    port_forwards='30010:80',
    objects = ['invent-frontend:ServiceAccount'],
    pod_readiness='wait',
    labels='frontend'
)

k8s_kind('local')