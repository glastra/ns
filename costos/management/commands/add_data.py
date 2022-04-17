import pandas as pd
from django.core.management.base import BaseCommand
from costos.models import Ingredient
from sqlalchemy import create_engine
from django.conf import settings


class Command(BaseCommand):
    help = " A command"

    def handle(self, *arg, **options):

        print("hello")
        excel_file = "nsexcel.xlsx"
        df = pd.read_excel(excel_file)

        user = settings.DATABASES['default']['USER']
        password = settings.DATABASE['default']['PASSWORD']
        database_name = settings.DATABASE['default']['NAME']

        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
            user=user,
            password=password,
            database_name=database_name,
        )

        engine = create_engine('database_url', echo=False, index=False)
        df.to_sql(Ingredient._meta.db_table, if_exist='append', con=engine)

