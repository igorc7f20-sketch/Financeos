
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=100)),
                ("type", models.CharField(
                    choices=[("income", "Income"), ("expense", "Expense")],
                    max_length=10,
                )),
                ("color", models.CharField(default="#6366f1", max_length=7)),
                ("icon", models.CharField(blank=True, default="", max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="categories",
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                "db_table": "categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True)),
                ("title", models.CharField(max_length=200)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("type", models.CharField(
                    choices=[("income", "Income"), ("expense", "Expense")],
                    max_length=10,
                )),
                ("date", models.DateField()),
                ("notes", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name="transactions",
                    to="transactions.category",
                )),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="transactions",
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                "db_table": "transactions",
                "ordering": ["-date", "-created_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(
                fields=["user", "name", "type"],
                name="unique_category_per_user",
            ),
        ),
    ]