# Generated by Django 3.0.6 on 2020-05-30 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Platform', '0002_geekinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
