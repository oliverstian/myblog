# Generated by Django 2.2.2 on 2019-07-16 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0008_auto_20190713_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecomment',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, '正常'), (0, '删除')], default=1, verbose_name='状态'),
        ),
    ]
