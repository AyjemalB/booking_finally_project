from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Добавим безопасную обработку
        if self.user:
            data['username'] = self.user.username
            data['email'] = self.user.email
            data['role'] = getattr(self.user, 'role', None)
        return data

