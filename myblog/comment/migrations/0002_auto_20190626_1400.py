# Generated by Django 2.2.2 on 2019-06-26 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, '删除'), (1, '正常')], default=1, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='target',
            field=models.CharField(max_length=100, verbose_name='评论目标'),
        ),
    ]
