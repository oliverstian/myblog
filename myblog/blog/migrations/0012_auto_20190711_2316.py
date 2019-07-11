# Generated by Django 2.2.2 on 2019-07-11 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20190710_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_md',
            field=models.BooleanField(default=False, verbose_name='markdown'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content_toc',
            field=models.TextField(blank=True, editable=False, null=True, verbose_name='文章目录'),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.PositiveIntegerField(choices=[(2, '草稿'), (1, '正常'), (0, '删除')], default=1, verbose_name='状态'),
        ),
    ]
