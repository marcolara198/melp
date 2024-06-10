import os

from tqdm import tqdm
import pandas as pd

from django.contrib.gis.geos import Point


class Importer:
    def get_filepath(self):
        restaurants_file = 'restaurantes.csv'

        base_path = os.path.dirname(os.path.abspath(__file__))
        abs_filepath = os.path.join(base_path, 'data/', restaurants_file)
        return abs_filepath

    def delete_all(self):
        from api.models import Restaurant

        Restaurant.objects.all().delete()

    def import_all(self):
        self.delete_all()

        self.import_restaurants()

    def import_restaurants(self):
        from api.models import Restaurant

        df = pd.read_csv(self.get_filepath(), keep_default_na=False)

        print('Importing Restaurants...')
        data_to_import = []
        for index, row in tqdm(df.iterrows(), total=df.shape[0]):
            data_to_import.append(
                Restaurant(
                    rating=row.rating,
                    name=row['name'],
                    site=row.site,
                    email=row.email,
                    phone=row.phone,
                    street=row.street,
                    city=row.city,
                    state=row.state,
                    lat=row.lat,
                    lng=row.lng,
                    location=Point(row.lat, row.lng),
                )
            )
        Restaurant.objects.bulk_create(data_to_import, ignore_conflicts=False)
