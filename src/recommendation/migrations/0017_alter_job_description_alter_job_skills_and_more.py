# Generated by Django 4.2.5 on 2024-03-24 14:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recommendation", "0016_alter_job_experience_alter_job_skills"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="description",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="skills",
            field=models.CharField(db_index=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name="job",
            name="title",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
    ]
