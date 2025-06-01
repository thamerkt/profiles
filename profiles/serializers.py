from rest_framework import serializers
from .models import Address, DocumentType, Profil, Document, ProfilMoral, PhysicalProfil
from django.http import QueryDict

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'country', 'postal_code']

class ProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer(allow_null=True, required=False)

    class Meta:
        model = Profil
        fields = '__all__'

    def to_internal_value(self, data):
        if isinstance(data, QueryDict):
            formatted_data = {}
            address_data = {}

            # Extract regular fields
            for key in data.keys():
                if key.startswith('address['):
                    field_name = key.split('[')[1].rstrip(']')
                    address_data[field_name] = data.get(key)
                else:
                    formatted_data[key] = data.get(key)

            if address_data:
                formatted_data['address'] = address_data

            return super().to_internal_value(formatted_data)

        return super().to_internal_value(data)

    def create(self, validated_data):
        # Extract address data
        address_data = validated_data.pop('address', None)
        profile_picture = self.context['request'].FILES.get('profile_picture') if 'request' in self.context else None

        # Clean or reject bad profil values
        if validated_data.get('profil') == 'undefined':
            validated_data.pop('profil')

        # Create address if provided
        address = Address.objects.create(**address_data) if address_data else None

        profile = Profil.objects.create(address=address, **validated_data)

        # Handle profile_picture upload
        if profile_picture:
            profile.profile_picture = profile_picture
            profile.save()

        return profile

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        profile_picture = self.context['request'].FILES.get('profile_picture') if 'request' in self.context else None

        if validated_data.get('profil') == 'undefined':
            validated_data.pop('profil')

        # Update or create address
        if address_data:
            if instance.address:
                address_serializer = AddressSerializer(instance.address, data=address_data, partial=True)
                address_serializer.is_valid(raise_exception=True)
                address_serializer.save()
            else:
                instance.address = Address.objects.create(**address_data)

        # Update fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if profile_picture:
            instance.profile_picture = profile_picture

        instance.save()
        return instance

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    uploadedBy = ProfileSerializer(read_only=True)
    type = DocumentTypeSerializer(read_only=True)

    class Meta:
        model = Document
        fields = '__all__'

class ProfilMoralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilMoral
        fields = '__all__'

class PhysicalProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalProfil
        fields = '__all__'

    def create(self, validated_data):
        profile_picture = self.context['request'].FILES.get('profile_picture') if 'request' in self.context else None
        instance = PhysicalProfil.objects.create(**validated_data)

        if profile_picture:
            instance.profile_picture = profile_picture
            instance.save()

        return instance
