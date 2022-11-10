from django.db import models
from django.utils import timezone

#validatorsフィールドオプションで使用する。最小と最大の制約を追加で課すことができる
from django.core.validators import MinValueValidator,MaxValueValidator

#映画作品のカテゴリ
class Category(models.Model):

    dt      = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    name    = models.CharField(verbose_name="カテゴリ名",max_length=10)

    #オブジェクトをそのまま表示させる時、カテゴリ名を表示させる
    def __str__(self):
        return self.name

    #TODO:idを文字列型に直すメソッドを作る
    def str_id(self):
        return str(self.id)


#TODO:映画に出演している俳優・女優、声優のモデル(Productモデルと多対多で繋がる)

#映画作品のモデル
class Product(models.Model):

    dt              = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    title           = models.CharField(verbose_name="タイトル",max_length=100)
    release_date    = models.DateField(verbose_name="公開日")

    #TODO:映画の紹介文とタイトルの両方で検索したい場合は
    #introduction   = models.CharField(verbose_name="紹介文",max_length=500)


    #1対多のフィールド
    #https://noauto-nolife.com/post/django-models-foreignkey/
    category        = models.ForeignKey(Category, verbose_name="カテゴリ", on_delete=models.CASCADE)

    #画像のフィールド
    #https://noauto-nolife.com/post/django-fileupload/

    #映画のジャケットが公開されていない場合、null=True,blank=Trueに仕立てるべき
    jacket          = models.ImageField(verbose_name="ジャケット画像",upload_to="movie/product/jacket/",null=True,blank=True)


    #レビュー数がどれだけあるか調べるメソッド
    def amount_review(self):
        #モデルは別のモデルを読み込み、検索する事ができる
        return Review.objects.filter(product=self.id).count()




class Review(models.Model):

    dt      = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    comment = models.CharField(verbose_name="コメント",max_length=300)
    spoiler = models.BooleanField(verbose_name="ネタバレ")

    #Productとの1対多フィールド(後から追加。マイグレーションの警告が出る←この対処法はマイグレーションファイルを全て削除する)
    """
    前提:ForeignKeyは関連するモデルのテーブルに実在するidを指定する必要がある。
    makemigraitons実行時の警告が出た時、実在しないidを指定する事はできない
    
    対処法1: マイグレーションファイルとDBを削除して、作り直す(開発中の段階では有効)
    対処法2: null=True,blank=Trueを入れる
    対処法3: 追加するモデルを一旦コメントアウトしてmakemigrations、フィールドを追加、コメントアウトを消してmakemigrationsを実行する
    """
    product = models.ForeignKey(Product, verbose_name="映画作品", on_delete=models.CASCADE)

    #TODO:評価のフィールド(1~5までの5段階)
    #https://noauto-nolife.com/post/django-star-review/
    #星の数値は最小で1、最大で5を指定。これ以外はバリデーションエラーになる。validatorsで追加の制約を課す
    star = models.IntegerField(verbose_name="星",validators=[MinValueValidator(1),MaxValueValidator(5)])

