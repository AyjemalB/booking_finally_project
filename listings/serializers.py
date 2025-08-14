from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'location', 'price',
            'rooms', 'housing_type', 'owner', 'created_at'
        ]
        read_only_fields = ['owner', 'created_at']
