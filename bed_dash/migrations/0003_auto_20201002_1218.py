# Generated by Django 3.1.1 on 2020-10-02 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bed_dash', '0002_auto_20201002_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulk_reg',
            name='from_date',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bulk_reg',
            name='to_date',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
