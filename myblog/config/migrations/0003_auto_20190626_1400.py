# Generated by Django 2.2.2 on 2019-06-26 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_auto_20190622_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, '删除'), (1, '正常')], default=1, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='sidebar',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, '隐藏'), (1, '展示')], default=1, verbose_name='状态'),
        ),
    ]
