# Generated by Django 2.2.2 on 2019-06-26 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190622_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, '删除'), (1, '正常'), (2, '草稿')], default=1, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, '删除'), (1, '正常')], default=1, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, '删除'), (1, '正常')], default=1, verbose_name='状态'),
        ),
    ]
