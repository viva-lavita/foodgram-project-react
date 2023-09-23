import csv

from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    """
    Чтобы запустить этот скрипт, необходимо выполнить команду
    'python manage.py load_csv' со следующими обязательными ключами
    (значение после '=' - пример заполнения):
    '--path=/path/to/file.csv' - путь к файлу csv
    '--model_name=YourModelName' - название модели Django
    '--app_name=YourAppName' - название приложение, где находится эта модель.

    Для успешного выполнения команды убедитесь,
    что у вас есть правильные разрешения на чтение файла csv
    и что файл csv содержит данные в правильном формате,
    соответствующем вашей модели.
    """
    help = 'Добавляет данные в модели из .csv файла.'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="путь к файлу")
        parser.add_argument('--model_name', type=str, help="имя модели")
        parser.add_argument('--app_name',
                            type=str,
                            help="название приложения, содержащее эту модель")

    def handle(self, *args, **options):
        app_name, model_name = options['app_name'], options['model_name']
        file_path = options['path']
        _model = apps.get_model(app_name, model_name)
        objects_list = []
        try:
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                print('Данные успешно импортированы')
                for row in reader:
                    if len(row) != 2:
                        print(f'Неправильный формат строки: {row}')
                        continue
                    name, measurement_unit = row
                    objects_list.append(_model(
                        name=name, measurement_unit=measurement_unit
                    ))
        except FileNotFoundError:
            print(f'Файл "{file_path}" не найден, неверный путь к файлу')
        except UnicodeDecodeError:
            print(f'Ошибка декодирования файла "{file_path}",'
                  ' проверьте кодировку')
        except Exception:
            print('Непонятная ошибка, зовите программиста')
        else:
            _model.objects.bulk_create(objects_list)
            self.stdout.write(self.style.SUCCESS(
                f'Данные в модель {model_name} загружены'
            ))
