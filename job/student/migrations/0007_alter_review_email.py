# Generated by Django 4.2 on 2023-04-16 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_alter_review_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='email',
            field=models.CharField(max_length=200),
        ),
    ]
