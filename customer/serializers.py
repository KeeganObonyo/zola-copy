from rest_framework import serializers
from rest_framework.serializers import EmailField, ModelSerializer

from .models import ( 
    Customer, Employee, 
    Subscription 
)

from review.views import RetrieveGooglePLaceId

class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'username',
            'company_name',
            'phone_number',
            'email',
            'place_id'
        ]

class CustomerCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')

    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'username',
            'company_name',
            'phone_number',
            'email',
            'password',
        ]
        extra_kwargs = {"password":
                        {"write_only": True}
                        }

    def validate(self, value):
        data = self.get_initial()
        email1 = data.get("email1")
        user_qs = Customer.objects.filter(email=email1)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")

        return value

    def create(self, validated_data):
        first_name   = validated_data['first_name']
        last_name    = validated_data['last_name']
        username     = validated_data['username']
        phone_number = validated_data['phone_number']
        company_name = validated_data['company_name']
        email        = validated_data['email']
        password     = validated_data['password']

        customer_obj = Customer(
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
            company_name=phone_number,
            email=email,
            place_id = RetrieveGooglePLaceId.get_place_id(company_name)
        )
        customer_obj.set_password(password)
        customer_obj.save()
        Subscription.objects.create(isactive = False, company = customer_obj)
        return validated_data

class EmployeeSerializer(serializers.ModelSerializer):
    company = CustomerSerializer(read_only=True)

    class Meta:
        model  = Employee
        fields = ('id','username','company')

class SubscriptionSerializer(serializers.ModelSerializer):
    company = CustomerSerializer(read_only=True)

    class Meta:
        model  = Subscription
        fields = ('id','isactive','company')