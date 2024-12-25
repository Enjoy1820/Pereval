from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from .models import  Expense, Coords, Level, PassUser, Images


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    winter = serializers.CharField(required=False)
    spring = serializers.CharField(required=False)
    summer = serializers.CharField(required=False)
    autumn = serializers.CharField(required=False)

    class Meta:
        model = Level
        fields = ['winter', 'spring', 'summer', 'autumn']


class PassUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassUser
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.ImageField(read_only=True)

    class Meta:
        model = Images
        fields = ['data', 'title']


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
            # data = img.pop('data')
            Images.objects.create(title=title, expense=pereval)

        return pereval

    def validate(self, value):
        if self.instance:
            if self.instance.status != 'new':
                raise serializers.ValidationError('Редактировать можно только'
                                                  'записи статуса "new"')

            user_data = value.get('user')

            if user_data:
                user = self.instance.user
                for field in 'email fam name otc phone'.split():
                    if getattr(user, field) != user_data[field]:
                        raise serializers.ValidationError('Данные о пользователе'
                                                          'менять нельзя')
        return value
