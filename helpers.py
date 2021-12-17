import psycopg2

def resetTables(cur):
    #Suppression des tables si elles sont déjà présentes en base
    cur.execute('''drop table if exists public.games_genre;''')
    cur.execute('''drop table if exists public.game;''')
    cur.execute('''drop table if exists public.genre;''')
    cur.execute('''drop table if exists public.player;''')

    #Création de la table player
    cur.execute('''
        create table "player" (
            id serial primary key,
            first_name text not null,
            last_name text,
            created_at timestamp default current_timestamp
        );''')

    #Création de la table game
    cur.execute('''
        create table "game" (
            id serial primary key,
            title text not null,
            added_at timestamp default current_timestamp,
            metacritic int,
            pegi int,
            release date,
            added_by int references public.player(id)
        );''')

    #Création de la table genre
    cur.execute('''
        create table "genre" (
            id serial primary key,
            name text not null
        );''')

    #Création de la table games_genre
    cur.execute('''
        create table "games_genre" (
            games_id int references public.game(id),
            genre_id int references public.genre(id)
        );''')

    # On ajoute l'autorisation à l'utilisateur sur toutes les tables et les séquences une fois créées
    cur.execute('grant all privileges on all tables in schema public to postgres;')
    cur.execute('grant all privileges on all sequences in schema public to postgres;')