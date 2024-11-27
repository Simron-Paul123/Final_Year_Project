# Generated by Django 5.1.3 on 2024-11-27 15:51

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "icon_class",
                    models.CharField(
                        help_text="CSS class for icon, e.g., 'ri-pencil-ruler-2-fill'",
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "profile_pic",
                    models.ImageField(blank=True, null=True, upload_to="profile_pics/"),
                ),
                ("cv", models.FileField(blank=True, null=True, upload_to="cv/")),
                ("education", models.TextField(blank=True, null=True)),
                ("skills", models.TextField(blank=True, null=True)),
                ("phone_no", models.CharField(blank=True, max_length=15, null=True)),
                (
                    "usertype",
                    models.CharField(
                        choices=[
                            ("recruiter", "Recruiter"),
                            ("job_seeker", "Job Seeker"),
                        ],
                        max_length=10,
                    ),
                ),
                ("is_approved", models.BooleanField()),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_logo",
                    models.ImageField(
                        default="company_logos/default.png", upload_to="company_logos/"
                    ),
                ),
                (
                    "company_name",
                    models.CharField(default="Default Company Name", max_length=100),
                ),
                (
                    "location",
                    models.CharField(default="Unknown Location", max_length=100),
                ),
                ("title", models.CharField(default="Job Title", max_length=100)),
                (
                    "description",
                    models.TextField(default="Job Description not provided."),
                ),
                ("positions", models.IntegerField(default=1)),
                (
                    "employment_type",
                    models.CharField(default="Full Time", max_length=50),
                ),
                (
                    "salary",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="jobs",
                        to="skill.category",
                    ),
                ),
            ],
        ),
    ]