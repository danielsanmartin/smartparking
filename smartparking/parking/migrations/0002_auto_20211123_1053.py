# Generated by Django 3.2.9 on 2021-11-23 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='space',
            options={'verbose_name': 'Vaga', 'verbose_name_plural': 'Vagas'},
        ),
        migrations.AlterField(
            model_name='unity',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone'),
        ),
    ]
