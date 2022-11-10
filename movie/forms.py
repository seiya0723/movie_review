from django import forms

from .models import Review,Product


#TODO:Productのcategoryを検索するためのフォームクラス
class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model   = Product
        fields  = [ "category" ]

#TODO:モデルを使用しないフォームクラス
class ReleaseDateFromForm(forms.Form):
    release_date_from = forms.DateField()

class ReleaseDateToForm(forms.Form):
    release_date_to = forms.DateField()



class ReviewForm(forms.ModelForm):

    class Meta:
        model   = Review
        fields  = [ "comment","spoiler","product","star" ]

