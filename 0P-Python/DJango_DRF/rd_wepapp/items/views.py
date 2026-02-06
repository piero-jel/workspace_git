'''
Docstring for rd_wepapp.items.views
'''
import json
# from django.shortcuts import render
from django.http import HttpResponse,Http404   # type: ignore pylint: disable=import-error
from django.template import loader             # type: ignore pylint: disable=import-error
import polars as pl                            # type: ignore pylint: disable=import-error

from rest_framework.views import APIView       # type: ignore pylint: disable=import-error
from rest_framework.response import Response   # type: ignore pylint: disable=import-error
from rest_framework import status              # type: ignore pylint: disable=import-error
from .models import Item,Seller
from .serializers import ItemSerializer

def index(request):
    '''  [url] ip:port/ ex: http://localhost:8080/
    '''

    context:dict = {
            "titulo": "Home, lista de links",
            "link" :[
                {'title': 'Listado de items mas caros','url': 'items/'},
                {'title': 'Listado de items vs seller','url': 'items_vs_seller/'},
                {'title': 'APIs Test', 'url': 'api/items/'},
                {'title': 'APIs Get offset=25 limit=10', 'url': 'api/items/?offset=25&limit=10'}
            ]
        }
    template = loader.get_template("items/home.html")
    return HttpResponse(template.render(context, request))


def items(request):
    ''' [url] ip:port/items http://127.0.0.1:8080/items
        data frame como base y conversion a dict
    '''
    try:
        nitem:int = 20
        queryset = Item.objects.all().values('title','price','thumbnail').order_by('-price') # pylint: disable=no-member
        if len(queryset) == 0:
            lst_seller = Seller.objects.all() # pylint: disable=no-member
            if len(lst_seller) == 0 :
                raise Seller.DoesNotExist # pylint: disable=no-member

            raise Item.DoesNotExist # pylint: disable=no-member

        template = loader.get_template("items/table_item.html")
        context:dict = {
                        "titulo": f"Lista de los {nitem} items mas caros",
                        "list_item" : queryset[:nitem]
                    }
        return HttpResponse(template.render(context, request))
    except Item.DoesNotExist as e: # pylint: disable=no-member
        raise Http404("Items does not exist") from e
    except Seller.DoesNotExist as e: # pylint: disable=no-member
        raise Http404("without seller") from e



def items_vs_seller(request):
    ''' [url] ip:port/items_vs_seller 'http://127.0.0.1:8080/items_vs_seller'
        data frame como base y conversion a dict
    '''
    try:
        queryset = Item.objects.all().values('id','price','listing_type_id', # pylint: disable=no-member
                                            'seller__id','seller__nickname') 
        if len(queryset) == 0:
            lst_seller = Seller.objects.all() # pylint: disable=no-member
            if len(lst_seller) == 0:
                raise Seller.DoesNotExist # pylint: disable=no-member

            raise Item.DoesNotExist # pylint: disable=no-member

        df = pl.from_dicts(list(queryset))

        df_items = df.group_by('seller__id').agg(
            pl.count('id').alias('Nro Publicaciones'),
            pl.first('seller__nickname').alias('Seller Nickname'),
            pl.mean('price').alias('Mean Price'),
            (pl.col('listing_type_id') == 'gold_special').sum().alias('Nro gold_special'),
            (pl.col('listing_type_id') == 'gold_pro').sum().alias('Nro gold_pro'),
        )
        df_items = df_items.rename({
                "seller__id": "Id Seller",                
            }
        )

        ## sort por 'nro_publicaciones'
        df_items = df_items.sort("Nro Publicaciones",descending=True,nulls_last=True)
        template = loader.get_template("items/table.html")
        context:dict = {
                        "titulo": "Lista de item vs sellers",
                        "table_head" : df_items.columns,
                        "table_rows" : df_items.rows(),
                        "head_with" : (100/len(df_items.columns))
                    }
        return HttpResponse(template.render(context, request))
    except Item.DoesNotExist as e: # pylint: disable=no-member
        raise Http404("Items does not exist") from e
    except Seller.DoesNotExist as e: # pylint: disable=no-member
        raise Http404("without seller") from e



class ItemsView(APIView):
    ''' Para el test de las apis http://127.0.0.1:8080/api/items/
    '''
    queryset = Item.objects.all() # pylint: disable=no-member
    serializer_class = ItemSerializer

    def get(self, request):
        ''' GET http://127.0.0.1:8080/api/items/?offset=10&limit=50

            request:<rest_framework.request.Request: GET '/api/items/?offset=10&limit=50'>
        '''
        try:
            offset = int(request.query_params.get('offset',0))
            limit  = int(request.query_params.get('limit',50))
            lst_items = Item.objects.all() # pylint: disable=no-member
            nitem = len(lst_items)
            if nitem == 0:
                lst_seller = Seller.objects.all() # pylint: disable=no-member
                if len(lst_seller) == 0:
                    raise Seller.DoesNotExist # pylint: disable=no-member
                raise Item.DoesNotExist # pylint: disable=no-member

            if offset>nitem:
                offset = 0

            serializer = None
            limit += offset
            if limit > nitem:
                serializer = ItemSerializer(lst_items[offset:], many=True)
            else:
                serializer = ItemSerializer(lst_items[offset:limit], many=True)
            return Response(serializer.data)

        except Seller.DoesNotExist as e: # pylint: disable=no-member
            raise Http404("without seller") from e
        except Item.DoesNotExist as e: # pylint: disable=no-member
            raise Http404("Items does not exist") from e

        except (ValueError,Exception) as e: # pylint: disable=broad-exception-caught
            data = {'mesage':f"Error {e} in request."}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        '''
        Metodo POST

        :param request: Description
        '''
        try:
            body_data:str = json.dumps(request.data)
            Item.json2object(body_data).save()
            data = {"message": "Success!"}
            return Response(data, status=status.HTTP_200_OK)
        except TypeError as e:
            ## error en el request, error en los valores
            data = {'mesage':f"Error {e} in request, value type error"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            ## error en el request, error en los valores
            data = {'mesage':f"Error {e} in request."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e: # pylint: disable=broad-exception-caught
            data = {'mesage':f"Error {e}"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
