from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from .models import  Expense, Coords, Level, PassUser, Images





class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'spring', 'summer', 'autumn']


class PassUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassUser
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [ 'data', 'title']



class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class ExpenseSerializer(WritableNestedModelSerializer):
    add_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    status = serializers.CharField(read_only=True)
    user = PassUserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer(allow_null=True, default=False)
    images = ImagesSerializer(many=True)

    class Meta:

        model = Expense
        fields = [
            'id', 'status', 'beauty_title', 'title', 'other_titles', 'connect',
            'add_time', 'user', 'coords', 'level', 'images'
        ]

    def create(self, validated_data, **kwargs):

        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        user, created = PassUser.objects.get_or_create(**user)

        coords = Coords.objects.create(**coords)
        level = Level.objects.create(**level)
        pereval = Expense.objects.create(**validated_data, user=user, level=level, coords=coords)

        for img in images:
            title = img.pop('title')
            data = img.pop('data')
            Images.objects.create(title=title, data=data, expense=pereval)

        return pereval


