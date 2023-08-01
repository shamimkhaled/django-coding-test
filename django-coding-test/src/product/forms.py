from django.forms import forms, ModelForm,  CharField, TextInput, Textarea, BooleanField, CheckboxInput
from django import forms
from product.models import Variant, Product


class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'active': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'active'})
        }




class CreateProductForm(ModelForm):
    model = Product
    fields = '__all__'
    widgets = {
            'product_name': TextInput(attrs={'class': 'form-control'}),
            'product_sku': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            

            
        }

    images= forms.ClearableFileInput(attrs={'class': 'form-control'})
    variants = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}))