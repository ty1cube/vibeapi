"""
Import csv data from CSV file to Datababse
"""
import os
import csv
from vibe_user import const_models
from django.core.management.base import BaseCommand
from django.conf import settings 


class Command(BaseCommand):

    def run_main_file_import(self, model, label, path):
        data_folder = os.path.join(settings.BASE_DIR, 'vibe_user', path)
        for data_file in os.listdir(data_folder):
            with open(os.path.join(data_folder, data_file), encoding='utf-8') as data_file:
                data = csv.reader(data_file)
                for data_object in data:
                    id = data_object[0]
                    name = data_object[1]

                    try:
                        object, created = model.objects.get_or_create(
                                id=id,
                                name=name,
                            )
                        if created:
                            object.save()
                            display_format = "\n{}, {}, has been saved."
                            print(display_format.format(label, object))
                    except Exception as ex:
                        print(str(ex))
                        msg = "\n\nSomething went wrong saving this {}: {}\n{}".format(label, id, str(ex))
                        print(msg)

    def import_country_from_file(self):
        data_folder = os.path.join(settings.BASE_DIR, 'vibe_user', 'resources/country_csv')
        for data_file in os.listdir(data_folder):
            with open(os.path.join(data_folder, data_file), encoding='utf-8') as data_file:
                data = csv.reader(data_file)
                for data_object in data:
                    id = data_object[0]
                    name = data_object[1]
                  
 
                    try:
                        country, created = const_models.Country.objects.get_or_create(
                                id=id,
                                name=name,
                              
                            )
                        if created:
                            country.save()
                            display_format = "\nCountry, {}, has been saved."
                            print(display_format.format(country))
                    except Exception as ex:
                        print(str(ex))
                        msg = "\n\nSomething went wrong saving this country: {}\n{}".format(id, str(ex))
                        print(msg)

    def import_state_from_file(self):
        data_folder = os.path.join(settings.BASE_DIR, 'vibe_user', 'resources/state_csv')
        for data_file in os.listdir(data_folder):
            with open(os.path.join(data_folder, data_file), encoding='utf-8') as data_file:
                data = csv.reader(data_file)
                for data_object in data:
                    id = data_object[0]
                    name = data_object[1]
                    country_id = data_object[2]
                  
                    try:
                        state, created = const_models.State.objects.get_or_create(
                                id=id,
                                name=name,
                                country_id=country_id,
                                
                              
                            )
                        if created:
                            state.save()
                            display_format = "\nState, {}, has been saved."
                            print(display_format.format(state))
                    except Exception as ex:
                        print(str(ex))
                        msg = "\n\nSomething went wrong saving this state: {}\n{}".format(id, str(ex))
                        print(msg)

    def import_local_from_file(self):
        data_folder = os.path.join(settings.BASE_DIR, 'vibe_user', 'resources/local_government_csv')
        for data_file in os.listdir(data_folder):
            with open(os.path.join(data_folder, data_file), encoding='utf-8') as data_file:
                data = csv.reader(data_file)
                for data_object in data:
                    id = data_object[0]
                    name = data_object[1]
                    state_id = data_object[2]
                  
                    try:
                        local, created = const_models.LocalArea.objects.get_or_create(
                                id=id,
                                name=name,
                                state_id=state_id,
                              
                            )
                        if created:
                            local.save()
                            display_format = "\nLocal, {}, has been saved."
                            print(display_format.format(local))
                    except Exception as ex:
                        print(str(ex))
                        msg = "\n\nSomething went wrong saving this Local Area: {}\n{}".format(id, str(ex))
                        print(msg)




    def import_member_type_from_file(self):
        self.run_main_file_import(const_models.MemberType, "MemberType", "resources/member_type_csv")


    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.import_member_type_from_file()
        self.import_country_from_file()
        self.import_state_from_file()
        self.import_local_from_file()




