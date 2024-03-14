# Generated by Django 5.0.3 on 2024-03-13 11:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('from_account', models.BigIntegerField()),
                ('to_account', models.BigIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(choices=[('T', 'Transfer'), ('D', 'Deposit'), ('W', 'Withdraw')], max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('CA', 'Canceled'), ('P', 'Pending'), ('CO', 'Completed')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('account_type', models.CharField(choices=[('S', 'Saving'), ('C', 'Checking')], max_length=20)),
                ('account_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account_holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]