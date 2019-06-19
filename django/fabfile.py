import time
from fabric.api import local, run, cd, env
from fabric.context_managers import warn_only

# ENVIRONMENTS #
PROD_HOST_STRING = ''


def dev():
    """Configure dev"""
    env.host_string = ''
    env.name = 'dev'
    env.port = 22
    env.branch = "development"
    env.project_root = '/home/tiip/tiip'
    env.backend_root = 'django'
    env.frontend_root = 'frontend'
    env.webpack_options = ''


def production():
    """Configure prod"""
    env.host_string = PROD_HOST_STRING
    env.name = 'production'
    env.port = 22
    env.branch = "tags/3.5.24"
    env.project_root = '/home/tiip/tiip'
    env.backend_root = 'django'
    env.frontend_root = 'frontend'
    env.webpack_options = '-live'


def staging():
    """Configure staging"""
    env.host_string = 'whomaps@157.230.27.132'
    env.name = 'staging'
    env.port = 22
    env.branch = "master"
    env.project_root = '/home/tiip/tiip'
    env.backend_root = 'django'
    env.frontend_root = 'frontend'
    env.webpack_options = ''


# COMMANDS #

def clone_prod_to(server):
    if server not in ['dev', 'staging']:
        print("Error. Valid servers are 'dev', 'staging'.")
        exit(1)
    # Dump prod data and tag
    production()
    with cd(env.project_root):
        # Get current tag
        tag = run('git rev-parse --abbrev-ref HEAD')
        # tag = run('git describe --tags')
        # Backup production database
        run('docker-compose exec postgres pg_dumpall -U postgres -c > ~/backup/dump`date +%d-%m-%Y`.sql')
        run('tar -czvf ~/backup/dump`date +%d-%m-%Y`.sql.tar.gz ~/backup/dump`date +%d-%m-%Y`.sql')
        # Backup production media files
        run('tar -czvf ~/backup/dump`date +%d-%m-%Y`.media.tar.gz django/media')
    # Load prod data and code
    globals()[server]()
    with cd(env.project_root):
        # Deploy as usual, but from the production tag
        # env.branch = 'tags/{}'.format(tag)
        env.branch = '{}'.format(tag)
        deploy()
        # Import production database
        run('scp {}:~/backup/dump`date +%d-%m-%Y`.sql.tar.gz .'.format(PROD_HOST_STRING))
        file = run('tar -xzvf dump`date +%d-%m-%Y`.sql.tar.gz')
        run('mv {} ~/backup/dump`date +%d-%m-%Y`.sql'.format(file))
        _drop_db()
        time.sleep(1)
        _create_db()
        # restore DB
        time.sleep(1)
        _restore_db()
        # Import production media files
        run('scp {}:~/backup/dump`date +%d-%m-%Y`.media.tar.gz .'.format(PROD_HOST_STRING))
        run('tar -xzvf dump`date +%d-%m-%Y`.media.tar.gz django/media/')

        run('docker-compose restart django')


def backup():
    # Backup database
    local('docker-compose exec postgres pg_dumpall -U postgres -c > ~/backup/dump`date +%d-%m-%Y`.sql')
    local('tar -czvf ~/backup/dump`date +%d-%m-%Y`.sql.tar.gz ~/backup/dump`date +%d-%m-%Y`.sql')
    # Backup media files
    local('tar -czvf ~/backup/dump`date +%d-%m-%Y`.media.tar.gz media/')


def deploy():
    db_up = None
    """Updates the server and restarts the apps"""
    with cd(env.project_root):
        # get new stuff from git
        run('git fetch')
        if env.name == 'production':
            with warn_only():
                run('rm ~/tiip/nginx/conf.d/production.conf')
        run('git checkout %s' % env.branch)
        run('git pull origin %s' % env.branch)
        time.sleep(10)

        if env.name == 'dev':
            options = "-f {}/docker-compose.yml -f {}/docker-compose.dev.yml ".format(
                env.project_root, env.project_root)
        elif env.name == 'staging':
            options = "-f {}/docker-compose.yml -f {}/docker-compose.test.yml ".format(
                env.project_root, env.project_root)
        elif env.name == 'production':
            options = "-f {}/docker-compose.yml -f {}/docker-compose.prod.yml ".format(
                env.project_root, env.project_root)
        else:
            options = ""

        ps = run('docker-compose ps')
        running = "".join([l for l in ps.split('\n') if 'Up' in l])

        time.sleep(3)

        if 'django' in running:
            run('docker-compose {}restart django'.format(options))
        if 'celery' in running:
            run('docker-compose {}restart celery'.format(options))
        if 'nginx' in running:
            run('docker-compose {}restart nginx'.format(options))
        if 'postgres' in running:
            db_up = True
            run('docker-compose {}restart postgres'.format(options))
        if 'rabbitmq' in running:
            run('docker-compose {}restart rabbitmq'.format(options))

        time.sleep(5)

        # handle backend
        with cd(env.backend_root):

            # backup DB
            if db_up:
                _backup_db()
            # build
            run('docker-compose {}build'.format(options))
            run('docker-compose {}down'.format(options))
            run("docker-compose {}up -d".format(options))

            # drop & create DB
            time.sleep(20)
            _drop_db()
            time.sleep(1)
            _create_db()
            # restore DB
            time.sleep(1)
            _restore_db()
            # migrate DB
            time.sleep(1)
            _migrate_db()
            time.sleep(1)
            # _import_geodata()

    tear_down()


def tear_down():
    if 'tear_down' in env:
        env.tear_down()


def _drop_db():
    run('docker-compose exec postgres dropdb -U postgres postgres')


def _create_db():
    run('docker-compose exec postgres createdb -U postgres postgres')


def _backup_db():
    run('docker-compose exec postgres pg_dumpall -U postgres -c > ~/backup/dump`date +%d-%m-%Y`.sql')


def _restore_db():
    run('cat ~/backup/dump`date +%d-%m-%Y`.sql | docker exec -i $(docker-compose ps -q postgres) psql -Upostgres')
    # run('cat ../dump.json | docker exec -i tip_django_1 python manage.py loaddata_stdin')


def _migrate_db():
    run('docker-compose exec django python manage.py migrate --noinput')


def _import_geodata():
    run('python geodata_import.py')


# LOCAL STUFF #


def test(app=""):
    local("docker-compose exec django ptw -- {} -s --testmon".format(app))


def cov():
    local(
        "docker-compose exec django py.test --cov --cov-report html --cov-fail-under 100 --cov-report term-missing"
        " --cov-config .coveragerc"
    )


def lint():
    local('docker-compose exec django flake8')


def makemigrations():
    local('docker-compose exec django python manage.py makemigrations')


def migrate():
    local("docker-compose exec django python manage.py migrate --noinput")


def import_geodata():
    local("python geodata_import.py prod")


def rebuild_db():
    local("docker-compose exec postgres dropdb -U postgres postgres")
    local("docker-compose exec postgres createdb -U postgres postgres")
    local("cat ./dump.sql | docker exec -i $(docker-compose ps -q postgres) psql -Upostgres")


def backup_db():
    local("docker-compose exec postgres pg_dumpall -U postgres -c > ./dump.sql")


def down():
    backup_db()
    local("docker-compose down")


def up():
    local("docker-compose up -d")


def up_debug():
    up()
    time.sleep(2)
    local("docker stop $(docker-compose ps -q django)")
    local("docker-compose run --service-ports django python manage.py runserver 0.0.0.0:8000")


def update_translations():
    local("docker-compose exec django python manage.py update_translations master.pot")


def shell():
    local("docker-compose exec django python manage.py shell")


def log():
    local("docker-compose logs -f django")


def single_coverage(folder, test_to_run):
    local("touch .lcoveragerc")
    local("printf '[run]\nsource = {}' > .lcoveragerc".format(folder))
    local("docker-compose exec django py.test --cov --cov-report term-missing -k"
          " '{}' --cov-config .lcoveragerc".format(test_to_run))


def send_test_email(type, email, **kwargs):
    params = ""
    for key, value in kwargs.items():
        params += '--{} {} '.format(key, value)
    local("docker-compose exec django python manage.py send_html_email {} {} {}".format(type, email, params) +
          "--settings=tiip.settings_email_test")


def dump_model_translations():
    local("docker-compose exec django python manage.py dumpdata country.country > Country.json")
    local("docker-compose exec django python manage.py dumpdata project.digitalstrategy > DigitalStrategy.json")
    local("docker-compose exec django python manage.py dumpdata project.healthcategory > HealthCategory.json")
    local("docker-compose exec django python manage.py dumpdata project.healthfocusarea > HealthFocusArea.json")
    local("docker-compose exec django python manage.py dumpdata project.hisbucket > HISBucket.json")
    local("docker-compose exec django python manage.py dumpdata project.hscchallenge > HSCChallenge.json")
    local("docker-compose exec django python manage.py dumpdata project.hscgroup > HSCGroup.json")
    local(
        "docker-compose exec django python manage.py dumpdata project.interoperabilitylink > InteroperabilityLink.json")
    local(
        "docker-compose exec django python manage.py dumpdata "
        "project.interoperabilitystandard > InteroperabilityStandard.json")
    local("docker-compose exec django python manage.py dumpdata project.licence > Licence.json")
    local("docker-compose exec django python manage.py dumpdata project.technologyplatform > TechnologyPlatform.json")
    local("tar -czvf translation_dumps_`date +%d-%m-%Y`.tar.gz *.json")
    local("rm *.json")
