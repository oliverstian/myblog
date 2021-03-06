# Generated by Django 2.2.2 on 2019-07-16 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20190716_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='is_top',
            field=models.PositiveIntegerField(choices=[(3, '普通栏'), (1, '凑数置顶栏'), (0, '海报栏'), (2, '置顶栏')], default=3, verbose_name='置顶'),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, '正常'), (0, '删除'), (2, '草稿')], default=1, verbose_name='状态'),
        ),
    ]
