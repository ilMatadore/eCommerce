# Generated by Django 3.1.3 on 2020-11-28 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='bids_in_the_product', to='auctions.Bid'),
        ),
        migrations.AddField(
            model_name='product',
            name='last_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_bid_for_the_auction', to='auctions.bid'),
        ),
    ]
