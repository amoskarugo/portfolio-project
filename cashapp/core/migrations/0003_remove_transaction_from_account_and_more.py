# Generated by Django 5.0.3 on 2024-03-20 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_account_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='from_account',
        ),
        migrations.AddField(
            model_name='transaction',
            name='from_account',
            field=models.BigIntegerField(default=0),
        ),
    ]
