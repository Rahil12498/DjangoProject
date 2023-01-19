from django.forms import ModelForm

from apps.product.models import Product

class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            self.fields['category'].widget.attrs['class']= 'select'
            self.fields['title'].widget.attrs['class']= 'input'
            self.fields['description'].widget.attrs['class']= 'textarea'
            self.fields['price'].widget.attrs['class']= 'input'
            self.fields['image'].widget.attrs['class']= 'file'
            self.fields['num_available'].widget.attrs['class']= 'file'
    class Meta:
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price', 'num_available']