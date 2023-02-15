load('ext://helm_resource', 'helm_resource', 'helm_repo')

# Add PostgreSQL Helm resource (https://artifacthub.io/packages/helm/bitnami/postgresql)
helm_repo('bitnami', 'https://charts.bitnami.com/bitnami',labels=['helm-charts'])
helm_repo('codecentric', 'https://codecentric.github.io/helm-charts',labels=['helm-charts'])
helm_resource(
    name='postgres',
    chart='bitnami/postgresql',
    namespace='default',
    flags=[
        '--set=image.tag=10.4.0',
        '--set=auth.enablePostgresUser=true',
        '--set=auth.postgresPassword=postgres'
    ],
    labels=['database']
)

local_resource(
  name='import-dump',
  resource_deps=['postgres'],
  cmd=['sh', '-c', """
kubectl cp $HOME/tilt_files/dump_anon.sql postgres-postgresql-0:/tmp/dump_anon.sql
kubectl exec postgres-postgresql-0 -- psql -U postgres -d postgres -f /tmp/dump_anon.sql
"""],
labels=['database'])

helm_resource(
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
    name='mailhog',
    chart='codecentric/mailhog',
    namespace='default',
    flags=[
        '--set=auth.enabled=false',
    ],
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
  # Values to set from the command-line
  set=['service.port=1234', 'ingress.enabled=false']
  )
k8s_yaml(yaml)

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

k8s_resource('invent-frontend', port_forwards='8080:80')

k8s_kind('local')