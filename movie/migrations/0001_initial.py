# Generated by Django 3.2.14 on 2022-09-30 05:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('name', models.CharField(max_length=10, verbose_name='カテゴリ名')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('title', models.CharField(max_length=100, verbose_name='タイトル')),
                ('release_date', models.DateField(verbose_name='公開日')),
                ('jacket', models.ImageField(upload_to='movie/product/jacket/', verbose_name='ジャケット画像')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.category', verbose_name='カテゴリ')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('comment', models.CharField(max_length=300, verbose_name='コメント')),
                ('spoiler', models.BooleanField(verbose_name='ネタバレ')),
                ('star', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='星')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.product', verbose_name='映画作品')),
            ],
        ),
    ]
