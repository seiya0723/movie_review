from django.urls import path 
from . import views 

app_name    = "movie"
urlpatterns = [
    path("", views.index, name="index"),

    #個別ページ(<int:pk>の部分はURL引数。product/3/というページにアクセスした時、pkに3が与えられ、views.productが実行される )
    #
    #URL引数のメリット
    #1 個別ページを表示する時に対象となるproductをidで特定する時、数値でなければならない(バリデーションが必要)。だが、URL引数ならバリデーションは不要
    #2 個別ページを表示する対象がURLに含まれるので、ログで確認を取りやすい。(product/だと何を見ているのかわからない)
    path("product/<int:pk>/", views.product, name="product"),
    #product/2/ product/5/

    path("ranking/", views.ranking, name="ranking"),
]


