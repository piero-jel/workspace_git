from rest_framework import serializers
from .models import Item,Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'
    #endclass
#endclass

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
    #endclass
#endclass