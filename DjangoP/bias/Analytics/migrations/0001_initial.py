# Generated by Django 4.2.4 on 2023-10-29 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Analytics.account')),
            ],
        ),
    ]