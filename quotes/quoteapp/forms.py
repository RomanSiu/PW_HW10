from django.forms import ModelForm, CharField, TextInput, DateField, DateInput, ModelChoiceField
from .models import Tag, Quote, Author


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    quote = CharField(min_length=5, max_length=100, required=True, widget=TextInput())
    author = ModelChoiceField(queryset=Author.objects.all())

    class Meta:
        model = Quote
        fields = ['quote', 'author']
        exclude = ['tags']


class AuthorForm(ModelForm):

    fullname = CharField(min_length=3, max_length=30, required=True, widget=TextInput())
    born_date = DateField(required=True, widget=DateInput())
    born_location = CharField(min_length=3, max_length=30, required=True, widget=TextInput())
    description = CharField(min_length=3, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
