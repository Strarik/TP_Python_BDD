from faker import Faker
import random

faker = Faker()

#Définition des champs de la table player
def player_first_name():
    return faker.first_name()

def player_last_name():
    return faker.last_name()

def player_created_at():
    return faker.date()
    
def player():
    return (player_first_name(), player_last_name(), player_created_at())


#Définition des champs de la table game

def game_name():
    return ' '.join(faker.words())

def game_metacritic():
    return faker.random_int(min=0, max=100)

def game_pegi():
    return random.choice([3,7,12,16,18])

def game_date():
    return faker.date()

def game_created_at():
    return faker.date()

def game_added_by(player_count):
    intrandom = random.randrange(0,100)

    if intrandom <= (100/(player_count+1)) or player_count == 0:
        return None
    else :
        return random.randrange(1,player_count+1)

def game(player_count):
    return (game_name(), game_metacritic(), game_created_at(), game_pegi(), game_date(), game_added_by(player_count))


#Définition des champs de la table genre

def genre():
    return [faker.word()]

#Définition des genres d'un jeu

def games_genre(game_id, genre_count):
    genre_id = random.randrange(1,genre_count+1)
    return (game_id, genre_id)