# Generated by Django 4.2.4 on 2023-11-21 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Offer', '0003_offer_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='analyzed',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='offer',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
