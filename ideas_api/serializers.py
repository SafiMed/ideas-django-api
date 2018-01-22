from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    """A serializer for our user objects."""

    class Meta:
        model = models.User
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user = models.User(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])

        user.save()

        return user


class IdeaSerializer(serializers.ModelSerializer):
    """A serializer for ideas."""

    class Meta:
        model = models.Idea
        fields = ('id', 'user_id', 'idea_text', 'creation_date', 'modification_date')
        extra_kwargs = {
                        'user_id': {'read_only': True},
                        'modification_date': {'read_only': True}
                    }
                    
