from django.db.models import Model, CharField, IntegerField



class Url(Model):

    original_url = CharField(max_length=1000, db_index=True)
    short_url = CharField(max_length=10, db_index=True)
    title = CharField(max_length=100)
    count = IntegerField(default=0)

    def __str__(self):
        return self.long_url


class Counter(Model):

    name = CharField(max_length=100, db_index=True)
    value = IntegerField(default=0)

    def __str__(self):
        return self.url.name
