from django import forms  
from .models import bulk_reg  
class bulkreg(forms.ModelForm):  
    class Meta:  
        model = bulk_reg  
        fields = "__all__"  