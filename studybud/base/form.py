from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    Room.host = request.user.username
    class Meta:
        model = Room
        fields = '__all__'
