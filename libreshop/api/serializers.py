from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework import exceptions
from addresses.models import Address
from orders.models import Order, Purchase

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'password')
        non_native_fields = ('token', 'captcha')
        write_only_fields = ('password',)
        read_only_fields = (
            'is_staff', 'is_superuser', 'is_active', 'date_joined'
        )


    def to_internal_value(self, data): # Similar to Form.clean.
        native_fields = self.Meta.fields
        non_native_fields = self.Meta.non_native_fields
        allowed_fields = (
            native_fields + non_native_fields + ('csrfmiddlewaretoken',)
        )

        unallowed_fields = [
            field for field in data if field not in allowed_fields
        ]
        for field in unallowed_fields:
            error = {
                '%s' % field: ['Field is not recognized.'],
                'description': ['The `%s` field is not permitted.' % field]
            }
            raise exceptions.ValidationError(error)

        native_data = {
            key:value for (key, value) in data.items() if key in native_fields
        }
        validated_data = (
            super(UserSerializer, self).to_internal_value(native_data)
        )

        password = validated_data['password']
        validated_data['password'] = make_password(password)

        return validated_data


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class RegistrationTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    image = serializers.CharField()
    audio = serializers.CharField()


class AddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Address
        fields = (
            'recipient_name', 'street_address', 'locality', 'region',
            'postal_code', 'country')


class PurchaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Purchase
        fields = ('url', 'name', 'sku', 'price', 'fulfilled')


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    shipping_address = AddressSerializer(many=False, read_only=True)
    purchases = PurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'url', 'token', 'shipping_address', 'subtotal', 'sales_tax',
            'shipping_cost', 'total', 'fulfilled', 'purchases'
        )
        extra_kwargs = {
            'url': {'lookup_field': 'token'}
        }
