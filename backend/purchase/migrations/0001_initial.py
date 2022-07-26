# Generated by Django 3.2.15 on 2022-08-12 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='goodsReceivingNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('purchaser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods_receiving_note_purchaser', to='authentication.user')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods_receiving_note_supplier', to='inventory.supplier')),
            ],
            options={
                'verbose_name': 'goods_receiving_note',
                'verbose_name_plural': 'goods_receiving_notes',
            },
        ),
        migrations.CreateModel(
            name='purchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order_approved_by', to='authentication.user')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order_created_by', to='authentication.user')),
            ],
        ),
        migrations.CreateModel(
            name='purchaseOrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_order_item', to='inventory.item')),
                ('purchaseOrder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.purchaseorder')),
            ],
        ),
        migrations.CreateModel(
            name='goodsReceivingNoteItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('goodsReceivingNote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.goodsreceivingnote')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods_receiving_note_item', to='inventory.item')),
            ],
        ),
    ]
