# Generated by Django 2.2.2 on 2019-07-12 12:07

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户信息', 'verbose_name_plural': '用户信息'},
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(default='avatar/default.png', upload_to='avatar/%Y/%m/%d', verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='user',
            name='website',
            field=models.URLField(blank=True, help_text='必须以http(s)开头的完整形式', null=True, verbose_name='个人网址'),
        ),
    ]