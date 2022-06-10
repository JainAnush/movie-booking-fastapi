from database import Base
from sqlalchemy import Column, Integer, String,Boolean,ForeignKey
class User(Base):
    __tablename__='users'
    userid = Column(Integer, primary_key=True)
    name=Column(String(30))
    mob=Column(String(13))

class Movie(Base):
    __tablename__='movies'
    movieid=Column(Integer,primary_key=True)
    moviename=Column(String(30))
    timeslot=Column(String(10))

class Seats(Base):
    __tablename__='seats'
    seatid=Column(Integer,primary_key=True)
    movieid=Column(Integer,ForeignKey("movies.movieid"),primary_key=True)
    totalseats=Column(Integer,default=40)
    seatsavailable=Column(Integer,default=40)

class bookings(Base):
    __tablename__='bookings'
    bookingid=Column(Integer,primary_key=True)
    userid=Column(Integer,ForeignKey("users.userid"))
    movieid=Column(Integer,ForeignKey("movies.movieid"))  
    seatid=Column(Integer,ForeignKey("seats.seatid"))  
