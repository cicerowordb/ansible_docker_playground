import datetime

from redis_om import (
    Field,
    HashModel,
    Migrator,
)
# Index=True allow search
class AncientGod(HashModel):
    greek_name: str = Field(index=True)
    roman_name: str = Field(index=True)
    gender: str = Field(index=True)
    description: str = Field(index=True)
    image_url: str = Field(index=True)
    created_at: datetime.date
    updated_at: datetime.date

class AccessHistory(HashModel):
    ancientgod_pk: str = Field(index=True)
    action: str = Field(index=True)
    accessed_at: datetime.date

Migrator().run()
