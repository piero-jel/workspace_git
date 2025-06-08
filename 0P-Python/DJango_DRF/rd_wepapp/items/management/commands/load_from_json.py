from django.core.management.base import BaseCommand
from items.models import Item,Seller
import json

class Command(BaseCommand):
    help = 'Carga datos desde un archivo JSON (comprende un array de ibjetos), a la Base de datos'

    def add_arguments(self, parser):
        parser.add_argument('--pathfile', type=str, help='Path to the JSON file')
        parser.add_argument('--encoding', action="store_true",help='encoding for JSON file',default='utf-8')

    def handle(self, *args, **options):
        pathfile = options['pathfile']
        encoding = options['encoding']
        try:
            with open(pathfile, 'r',encoding=encoding) as f2r:
                data = json.load(f2r)
            #endwith

            for item in data:
                seller = item.pop('seller')
                
                if(Seller.objects.filter(id=seller['id']).exists()):
                    if(Item.objects.filter(id=item['id']).exists()):
                       continue
                    #endif
                    Item.objects.create(**item,seller=Seller.objects.get(id=seller['id']))
                    continue
                #endif
                reg_seller = Seller.objects.create(**seller)
                Item.objects.create(**item,seller=reg_seller)                
            #endfor                
            self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('JSON file not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {e}'))