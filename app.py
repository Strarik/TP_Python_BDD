#Import des modules
import psycopg2
import helpers
import generate
import random
import export
import requests
import migrate

with psycopg2.connect(dbname="postgres", user="postgres", password="tppythondatabasesql", host="db.rltdxzahimmyfdhgzxek.supabase.co", port="5432") as conn:
    with conn.cursor() as cur:
        #Reset des bases de données afin d'avoir un jeu de données propre
        helpers.resetTables(cur)

        # On ajoute 10 utilsateurs
        for i in range(10):
            cur.execute('insert into "player" (first_name, last_name, created_at) values (%s, %s, %s);', generate.player())

        # Calcul du nombre de joueurs dans la base de données
        cur.execute('select count(*) from "player";')
        player_count = cur.fetchone()[0]

        # On ajoute 100 jeux
        for i in range(100):
            cur.execute('''
                insert into "game" (title, metacritic, added_at, pegi, release, added_by) values (%s, %s, %s, %s, %s, %s);''', generate.game(player_count))

        # On génère 20 genres
        for i in range(20):
            cur.execute('insert into "genre" (name) values (%s);', generate.genre())

        # On compte le nombre de jeux présents en base
        cur.execute('select count(*) from "game";')
        game_count = cur.fetchone()[0]

        # On compte le nombre de genres présents en base
        cur.execute('select count(*) from "genre";')
        genre_count = cur.fetchone()[0]

        # On associe à chaque jeu de 1 à 3 genres
        for game_id in range (game_count) :
            nbGenres = random.randrange(1,3)
            for i in range (nbGenres+1) :
                cur.execute('insert into "games_genre" (games_id, genre_id) values (%s, %s);', generate.games_genre(game_id + 1, genre_count))

        #Fin des opération d'ajout / modification, donc commit des modifications
        conn.commit()

        #Export des meilleurs jeux par année en fichier .csv
        data = requests.executeRequestBestGames(cur)
        export.export(data, './exports/stats_best_games.csv')

        #Export des pires jeux par année en fichier .csv
        data = requests.executeRequestWorstGames(cur)
        export.export(data, './exports/stats_worst_games.csv')

        #Export du nombre de jeu rajouté par chaque utilisateur ainsi que la note moyenne de ces derniers
        data = requests.executeRequestPlayerGames(cur)
        export.export(data, './exports/stats_players.csv')

        #Export du nombre de jeux pour chaque genre
        data = requests.executeRequestGamesGenre(cur)
        export.export(data, './exports/stats_genre.csv')

        #Création du JSON games
        migrate.game_table(cur)

        #Création du JSON players
        migrate.player_table(cur)