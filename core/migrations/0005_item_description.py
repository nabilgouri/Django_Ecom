# Generated by Django 2.2 on 2020-12-10 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='descriptions'),
            preserve_default=False,
        ),
    ]
