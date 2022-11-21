# Generated by Django 4.1.2 on 2022-11-18 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_organization_count'),
        ('user', '0002_user_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='organization',
            field=models.ManyToManyField(blank=True, related_name='users', to='organization.organization'),
        ),
    ]
