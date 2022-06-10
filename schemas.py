from pydantic import BaseModel
class UserSchema(BaseModel):
    id:int
    name:str
    mob:str

    class Config:
        orm_mode=True

class MovieSchema(BaseModel):
    id:int
    name:str
    timeslot:str

    class Config:
        orm_mode=True

class BookingSchema(BaseModel):
    id:int
    userid:int
    movieid:int
    seatid:int

    class Config:
        orm_mode=True        


