from django.shortcuts import render,redirect
from django.views import View

from .models import Category,Product,Review
from .forms import ReviewForm,ProductCategoryForm,ReleaseDateFromForm,ReleaseDateToForm

from django.db.models import Q


class IndexView(View):
    def get(self, request, *args, **kwargs):

        context = {}

        #order_byのdt は古いものが上に表示、以降新しくなっていく
        context["categories"]   = Category.objects.order_by("dt")

        #クエリを初期化しておく。
        query   = Q()

        #searchが存在するかチェック
        if "search" in request.GET:

            #検索時に指定したキーワードの取得をする
            print(request.GET["search"])
            search  = request.GET["search"]

            #ここで検索の処理を実装させる

            #このtitle=searchでは完全一致しないと出てきてくれない
            #context["products"] = Product.objects.filter(title=search).order_by("dt")

            #searchを含むtitleを検索する(スペース区切りで検索をしてくれない)
            #context["products"] = Product.objects.filter(title__icontains=search).order_by("dt")

            #スペース区切りでそれぞれの単語を含むタイトルを検索する
            #半角スペースで区切ってリスト型に直す
            words = search.replace("　"," ").split(" ")

            #スペース区切りを1つずつ取り出す
            for word in words:
                #空文字列の場合は次のループへ
                if word == "":
                    continue

                #AND検索
                query &= Q(title__icontains=word)
                #OR検索
                #query |= Q(title__icontains=word)

        """
            #生成したqueryを実行する
            context["products"] = Product.objects.filter(query).order_by("dt")
        else:
            context["products"] = Product.objects.order_by("dt")
        """
        #TODO:ここでカテゴリによる絞り込みを行う

        """
        if "category" in request.GET:
            # 正常に指定されていれば"3"取れる。だが、存在しないCategoryのidだったり、数値に変換できない文字列が送信されることもある
            # バリデーションを行うことで、存在するCategoryのidであることをチェックする
            print(request.GET["category"])
        """

        # Categoryの存在確認、指定した型へ変換
        form = ProductCategoryForm(request.GET)
        if form.is_valid():
            # name属性categoryがあり、その値はCategoryに実在するidである
            #formオブジェクトのcleanメソッドを使って、入力された値を適宜型変換する
            cleaned = form.clean()
            query &= Q(category=cleaned["category"].id)
            print("バリデーションOK")
            print("これはCategoryモデルのidです")
        else:
            print("バリデーションNG")
            print("これはCategoryモデルのidではありません")


        #release_dateによる絞り込み
        form = ReleaseDateFromForm(request.GET)
        if form.is_valid():
            print("バリデーションOK")
            print("日付フォーマットである")
            cleaned = form.clean()
            # greater than or equale 略して gte 右辺以上のデータを取り出す
            # less than or queale 略して lte 右辺以下のデータを取り出す
            #　より上は gt 未満は lt で検索できる
            query &= Q(release_date__gte=cleaned["release_date_from"])
        else:
            print("バリデーションNG")
            print("日付フォーマットではない")

        #release_dateによる絞り込み
        form = ReleaseDateToForm(request.GET)
        if form.is_valid():
            print("バリデーションOK")
            print("日付フォーマットである")
            cleaned = form.clean()
            # greater than or equale 略して gte 右辺以上のデータを取り出す
            # less than or queale 略して lte 右辺以下のデータを取り出す
            #　より上は gt 未満は lt で検索できる
            query &= Q(release_date__lte=cleaned["release_date_to"])
        else:
            print("バリデーションNG")
            print("日付フォーマットではない")



        #TODO:ここに他にも絞り込みの条件を書く



        #TODO:queryの実行は、ユーザーによって指定された条件の追加を全て終えてから行う。
        context["products"] = Product.objects.filter(query).order_by("dt")


        return render(request, "movie/index.html", context)

index   = IndexView.as_view()



#映画作品個別ページ
class ProductView(View):
    #pk primary keyの略(idのこと)。
    def get(self, request, pk, *args, **kwargs):
        context = {}

        #映画を特定する。(.first()を実行すると最初の1つ分のデータだけ取り出せる。これはテンプレートでforループをする必要はなくなる)
        context["product"]      = Product.objects.filter(id=pk).first()
        #存在しないpkにアクセスした場合、存在しない旨をテンプレートに表示させるか、リダイレクトさせる

        #この映画に紐づくレビューを取り出す。(新しい順にレビューを取り出したい場合、-dtとする)
        context["reviews"]      = Review.objects.filter(product=pk).order_by("-dt")

        return render(request, "movie/product.html", context)

    def post(self, request, pk, *args, **kwargs):
        #requestオブジェクトはイミュータブルなオブジェクト(書き換えができない)。下記はエラーになる
        #request.POST["product"] = pk

        #受け取ったデータをコピーをした上で、データの追加をする
        copied              = request.POST.copy()
        copied["product"]   = pk

        form = ReviewForm(copied)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print(form.errors)

        #URL引数がある場合、redirectの第二引数にURL引数をセットする
        return redirect("movie:product",pk)

product = ProductView.as_view()


class RankingView(View):

    def get(self, request, *args, **kwargs):

        context             = {}

        #レビュー数に応じて、ランキングを作る(filterで日時を指定したほうがよいかも)
        products            = Product.objects.all()

        #前もってメソッド実行用のoperatorを用意する
        import operator

        #sorted関数で productsをループし、operatorを使ってamount_reviewを実行して並び替える
        context["products"] = sorted(products, key=operator.methodcaller('amount_review'), reverse=True)

        #モデルメソッドを使用してランキングを作る
        #https://noauto-nolife.com/post/django-attr-method-sort/


        return render(request, "movie/ranking.html", context)

ranking = RankingView.as_view()


