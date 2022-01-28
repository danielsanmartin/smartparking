# Generated by Django 3.2.9 on 2021-11-23 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0002_auto_20211123_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='status',
            field=models.IntegerField(choices=[(1, 'Normal'), (2, 'Preferencial')], default=1, verbose_name='Situação'),
        ),
        migrations.AlterField(
            model_name='ocrcameraevent',
            name='type',
            field=models.IntegerField(choices=[(1, 'Entrada'), (2, 'Saída')], default=1, verbose_name='Tipo'),
        ),
    ]
