from peewee import * 

database = SqliteDatabase('dirlist.sqlite')

class BaseModel(Model):
	class Meta:
		database = database


class DirListInfo(BaseModel):
	computer_id = CharField()
	entity_id = IntegerField()
	entity_drive = CharField()
	entity_root_path = CharField()
	entity_type = CharField()
	entity_date = DateTimeField()
	entity_name = CharField()
	entity_size = BigIntegerField()

def create_tables():
    with database:
        database.create_tables([DirListInfo])

if __name__ == '__main__':
	create_tables()