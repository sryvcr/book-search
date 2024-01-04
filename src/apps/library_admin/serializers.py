from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.ReadOnlyField()
    subtitle = serializers.ReadOnlyField()
    authors = serializers.ReadOnlyField()
    categories = serializers.ReadOnlyField()
    publication_date = serializers.ReadOnlyField()
    editor = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()
    image = serializers.ReadOnlyField()
    source = serializers.ReadOnlyField()
