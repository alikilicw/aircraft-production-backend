# Generated by Django 5.1.4 on 2025-01-07 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_team_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='slug',
            field=models.SlugField(choices=[('wing', 'Wing'), ('fuselage', 'Fuselage'), ('tail', 'Tail'), ('avionics', 'Avionics'), ('assembly', 'Assembly')], null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
