# Generated by Django 2.2.2 on 2019-07-05 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_auto_20190627_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidebar',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, '隐藏'), (1, '展示')], default=1, verbose_name='状态'),
        ),
    ]
