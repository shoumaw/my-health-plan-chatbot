import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Creates the PostgreSQL database if it does not already exist"

    def handle(self, *args, **options):
        db = settings.DATABASES["default"]
        db_name = db["NAME"]

        conn = psycopg2.connect(
            dbname="postgres",
            user=db["USER"],
            password=db["PASSWORD"],
            host=db["HOST"],
            port=db["PORT"],
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", [db_name])
        if cursor.fetchone():
            self.stdout.write(f'Database "{db_name}" already exists — skipping.')
        else:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            self.stdout.write(self.style.SUCCESS(f'Database "{db_name}" created.'))

        cursor.close()
        conn.close()
