# Generated by Django 4.2.5 on 2023-11-28 14:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recommendation", "0002_alter_company_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="description",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="title",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
