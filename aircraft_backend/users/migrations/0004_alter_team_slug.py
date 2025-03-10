# Generated by Django 5.1.4 on 2025-01-07 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_team_slug_alter_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='slug',
            field=models.SlugField(choices=[('wing', 'Wing'), ('fuselage', 'Fuselage'), ('tail', 'Tail'), ('avionics', 'Avionics'), ('assembly', 'Assembly')], editable=False, null=True, unique=True),
        ),
    ]
