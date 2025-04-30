import os
from pymongo import MongoClient
from .GetReviews import get_reviews
from .mongo_client import get_mongo_client

genres = ['Acción',
 'Aventura',
 'Animación',
 'Comedia',
 'Crimen',
 'Documental',
 'Drama',
 'Familia',
 'Fantasía',
 'Historia',
 'Terror',
 'Música',
 'Misterio',
 'Romance',
 'Ciencia ficción',
 'Película de TV',
 'Suspense',
 'Bélica',
 'Western']

emotions = 

def InsertReview(MoviesCollection:object):
    '''Insert movie and their corresponding emotion 
       into a MongoDB collection'''
    for review in GetReviews()
