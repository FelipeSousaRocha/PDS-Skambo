# Generated by Django 3.2.3 on 2022-03-06 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skambo', '0006_auto_20220306_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='genero',
            field=models.IntegerField(choices=[(1, 'masculino'), (2, 'feminino')], default=1),
        ),
    ]
