from enum import Enum

from tortoise import fields, models


class StatusEnum(Enum):
    ACTIVE = "Active"
    COMING_SOON = "Coming soon"
    REMOVED = "Removed"
    LEAVING_SOON = "Leaving soon"


class System(models.Model):
    name = fields.CharField(pk=True, max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = fields.CharField(pk=True, max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ESRB(models.Model):
    code = fields.CharField(pk=True, max_length=30)
    description = fields.TextField()

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code


class Game(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=150)
    systems = fields.ManyToManyField("models.System", related_name="games")
    x_cloud = fields.BooleanField(default=False)
    status = fields.CharEnumField(StatusEnum, max_length=50)
    date_added = fields.DateField()
    date_removed = fields.DateField(null=True)
    date_released = fields.DateField()
    genres = fields.ManyToManyField("models.Genre", related_name="games")
    x_exclusive = fields.BooleanField(default=False)
    esrb = fields.ForeignKeyField("models.ESRB", on_delete=fields.SET_NULL, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}: {self.title}"
