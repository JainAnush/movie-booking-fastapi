
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from database import SessionLocal, db_engine,Base
from models import Movie, User, bookings,Seats
from schemas import UserSchema,MovieSchema,BookingSchema
from sqlalchemy.orm import sessionmaker,Session
from typing import Optional,List
from fastapi.responses import JSONResponse
import random
from sqlalchemy import and_,desc,or_



app=FastAPI()

Base.metadata.create_all(db_engine)  
session=sessionmaker(bind=db_engine) 

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/test')
def test():
    return {'data':'test'}

@app.post('/register')
def register(userdetails:UserSchema,db:Session=Depends(get_db)):
    user=User(userid=userdetails.id,name=userdetails.name,mob=userdetails.mob)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post('/addmovie')
def addMovie(movie:MovieSchema,db:Session=Depends(get_db)):
    moviepresent=db.query(Movie).filter((Movie.movieid==movie.id)).first()
    if moviepresent!= None:
        return {'error':'THIS MOVIE ID ALREADY EXISTS TRY A DIFFERENT MOVIE ID'}
    moviefound=db.query(Movie).filter(and_(Movie.moviename==movie.name,Movie.timeslot==movie.timeslot)).first()
    if moviefound==None:
        obj=Movie(movieid=movie.id,moviename=movie.name,timeslot=movie.timeslot)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    return {'error ':f'MOVIE {movie.name} ALREADY PRESENT AT TIMESLOT {movie.timeslot}'}    


@app.post('/bookmovie')
def bookMovie(bookingdetails:BookingSchema,db:Session=Depends(get_db)):
    try:
        record=db.query(bookings).filter(and_(bookings.seatid==bookingdetails.seatid,bookings.movieid==bookingdetails.movieid)).first()
        userfound=db.query(User).filter(User.userid==bookingdetails.userid).first()
        moviefound=db.query(Movie).filter(Movie.movieid==bookingdetails.movieid).first()
        if userfound==None:
            return {'error':'USER NOT REGISTERED'}
        if record!=None:
            return {"error":'THIS SEAT HAS ALREADY BEEN BOOKED'}
        if moviefound == None:
            return {"error":"INVALID MOVIE ID"}        
    except:
        return {'error':'server error'}      
    if bookingdetails.seatid>40:
        return {'error':"THERE ARE ONLY 40 SEATS AVAILABLE, PLEASE ENTER SEAT NUMBER BETWEEN 1 TO 40 ONLY"}    
    newseat=Seats(seatid=bookingdetails.seatid,movieid=bookingdetails.movieid) 
    currseatavailable=db.query(Seats).filter(Seats.movieid==bookingdetails.movieid).order_by(Seats.seatsavailable).first()
    if currseatavailable==None:
        newseat.seatsavailable=39;
    elif currseatavailable.seatsavailable==0:
        return {'HOUSEFULL':"ALL SEATS BOOKED"}
    else:    
        newseat.seatsavailable=currseatavailable.seatsavailable-1
    db.add(newseat)
    db.commit()
    print("seat added")            
    booking=bookings(bookingid=random.randint(34521,46484),userid=bookingdetails.userid,movieid=bookingdetails.movieid,seatid=bookingdetails.seatid)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking    

@app.get('/getdetails/{user_id}/{booking_id}')
def getDetails(user_id,booking_id,db:Session=Depends(get_db)):
    bookingdetails=db.query(bookings).filter(bookings.bookingid==booking_id).first()
    if bookingdetails==None:
        return {'error':f'NO BOOKING FOUND FOR BOOKING ID {booking_id}'}
    movie_id=bookingdetails.movieid;
    seat_id=bookingdetails.seatid;
    moviedetails=db.query(Movie).filter(Movie.movieid==movie_id).first()
    movie_name=moviedetails.moviename
    timeslot=moviedetails.timeslot;
    return {'booking id':booking_id,'movie id':movie_id,'movie name':movie_name,'show time':timeslot,'seat id':seat_id}

@app.get('/showallmovies')
def getAllMovies(db:Session=Depends(get_db)):
    all_movies=db.query(Movie).all()
    res=[]
    if all_movies==None:
        return {'movie list':'NO MOVIE AVAILBALE AT THIS MOMENT'}
    for movie in all_movies:
        res.append({'movie id':movie.movieid,'movie name':movie.moviename,'timing':movie.timeslot})
    return res 

@app.get('/showavailableseats/{movie_id}')
def getAvailableSeats(movie_id:int,db:Session=Depends(get_db)):
    available=db.query(Seats).filter(Seats.movieid==movie_id).order_by(Seats.seatsavailable).first()
    if available==None:
        return {'error':"INVALID MOVIE ID"}
    movie=db.query(Movie).filter(Movie.movieid==movie_id).first()    
    return {'seats available':f'{available.seatsavailable} SEAT(s) ARE AVAILABLE FOR THE MOVIE {movie.moviename} AT {movie.timeslot}'}    
         
