import os
from subprocess import call
from shutil import copyfile
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = """
    updates translation files for all languages based on a master PO template.
    usage: update_translations <master_file>
    eg: update_translations master.pot
    """

    def add_arguments(self, parser):
        parser.add_argument('pot')

    def handle(self, *args, **options):
        self.stdout.write("-- Updating translations")
        pot_name = options['pot']
        pot_file = os.path.join(settings.LOCALE_PATHS[0], pot_name)

        for language in settings.LANGUAGES:
            po_file = os.path.join(settings.LOCALE_PATHS[0], '{}/LC_MESSAGES/djangojs.po'.format(language[0]))
            if not os.path.exists(po_file):
                copyfile(pot_file, po_file)
            call(["msgmerge", "-U", "-N", po_file, pot_file])
