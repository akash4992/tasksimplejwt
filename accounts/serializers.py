from rest_framework import serializers
from accounts.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','username','email','salary','department')

class UserSalarySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('salary','department')
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'password']


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','salary','department')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self,value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('User with this email already exists')
        return value
    def validate_username(self,value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError('User with this username already exists')
        return value
    def create(self, validated_data):
        user = User(username= validated_data['username'], email=validated_data['email'],salary=validated_data['salary'],department=validated_data['department'],)
        user.set_password(validated_data['password'])
        user.save()
        return user