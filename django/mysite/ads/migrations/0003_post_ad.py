# Generated by Django 4.0.5 on 2023-10-02 04:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_user_is_advertiser_user_is_influencer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('price', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='adlikes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]