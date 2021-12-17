import json
import datetime

#Gestion des potentielles erreurs lorsque l'on rencontre le type date / datetime
class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime) or isinstance(z, datetime.date):
            return (str(z))
        else:
            return super().default(z)

#Création du json games
def game_table(cur):
    cur.execute('''select 
        ga.id,
        ga.title,
        ga.added_at,
        ga.metacritic,
        ga.pegi,
        ga.release,
        ga.added_by,
        ARRAY_AGG (ge.name) genres
        from game ga
        join games_genre gg on gg.games_id = ga.id
        join genre ge on gg.genre_id = ge.id
        group by ga.id''')
    res = cur.fetchall()

    games = list(map(parse_game, res))

    with open(f'./migrations/games.json', 'w') as file:
        file.write(json.dumps(games, cls=DateTimeEncoder))

def parse_game(gametuple):
    (id, title, added_at, metacritic, pegi, release, added_by, genres) = gametuple
    return {
        '_id': id,
        'title': title,
        'added_at': added_at,
        'added_by': added_by,
        'infos': {
            'metacritic': metacritic,
            'pegi': pegi,
            'release': release,
            'genres': genres
        }
    }

#Création du json players
def player_table(cur):
    cur.execute('select * from "player"')
    res = cur.fetchall()

    players = list(map(parse_player, res))

    with open(f'./migrations/players.json', 'w') as file:
        file.write(json.dumps(players, cls=DateTimeEncoder))

def parse_player(playertuple):
    (id, first_name, last_name, created_at) = playertuple
    return {
        '_id': id,
        'first_name': first_name,
        'last_name': last_name,
        'created_at': created_at
    }