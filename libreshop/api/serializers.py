from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import exceptions
from addresses.models import Address
from fulfillment.models import Carrier, Shipment
from orders.models import Order, Purchase, Transaction

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

    drop_shipped = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    sku = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = (
            'url', 'name', 'sku', 'price', 'drop_shipped', 'fulfilled', 'weight'
        )

    def get_drop_shipped(self, obj):
        return bool(obj.variant.suppliers)

    def get_name(self, obj):
        return obj.variant.name

    def get_sku(self, obj):
        return obj.variant.sku

    def get_weight(self, obj):
        return obj.variant.weight


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    shipping_address = AddressSerializer(many=False, read_only=True)
    purchases = PurchaseSerializer(many=True, read_only=True)
    last_4 = serializers.SerializerMethodField()
    payment_method = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'url', 'token', 'shipping_address', 'subtotal', 'sales_tax',
            'shipping_cost', 'total', 'payment_method', 'last_4', 'fulfilled',
            'purchases', 'created', 'modified'
        )
        extra_kwargs = {
            'url': {'lookup_field': 'token'}
        }

    def get_last_4(self, obj):
        transaction = None
        try:
            transaction = obj.transaction_set.first()
        except Transaction.DoesNotExist as e:
            pass
        return transaction.payment_card_last_4 if transaction else None

    def get_payment_method(self, obj):
        transaction = None
        try:
            transaction = obj.transaction_set.first()
        except Transaction.DoesNotExist as e:
            pass
        return transaction.payment_card_type if transaction else None


class ShipmentSerializer(serializers.HyperlinkedModelSerializer):

    order = OrderSerializer(many=False, read_only=True)
    carrier = serializers.SerializerMethodField()

    class Meta:
        model = Shipment
        fields = ('url', 'order', 'carrier', 'tracking_id', 'shipping_cost',
            'created', 'modified')

    def get_carrier(self, obj):
        return obj.carrier.name

    def to_internal_value(self, data): # Similar to Form.clean.
        validated_data = super(ShipmentSerializer, self).to_internal_value(data)

        carrier = None
        try:
            carrier_name = data.get('carrier')
            carrier = Carrier.objects.get(name=carrier_name)
        except Carrier.DoesNotExist as e:
            raise serializers.ValidationError({
                'carrier': 'Invalid carrier specified (%s)!' % carrier_name})

        order = None
        try:
            order_token = data.get('order_token')
            order = Order.objects.get(token=order_token)
        except Order.DoesNotExist as e:
            raise serializers.ValidationError({
                'order': 'Invalid order token specified (%s)!' % order_token})

        validated_data.update({
            'carrier': carrier,
            'order': order
        })
        return validated_data

    def create(self, validated_data):
        shipment = super(ShipmentSerializer, self).create(validated_data)
        shipment.notify_recipient()
        return shipment
