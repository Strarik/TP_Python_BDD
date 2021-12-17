#Récupération des jeux ayant eu la note la plus élevée sur Metacritic pour chaque année
def executeRequestBestGames(cur) :
    cur.execute(
        '''select
            g.title,
            g.metacritic,
            date_part('year', g."release") as release_year
        from game g
        where
            g.metacritic = (
                select max(metacritic)
                from game
                where date_part('year', "release") = date_part('year', g."release")
            )
        order by release_year'''
    )

    data = cur.fetchall()
    header = [('title', 'metacritic', 'release_year')]
    data = header + data
    return data

#Récupération des jeux ayant eu la note la plus basse sur Metacritic pour chaque année
def executeRequestWorstGames(cur) :
    cur.execute(
        '''select
            g.title,
            g.metacritic,
            date_part('year', g."release") as release_year
        from game g
        where
            g.metacritic = (
                select min(metacritic)
                from game
                where date_part('year', "release") = date_part('year', g."release")
            )
        order by release_year'''
    )

    data = cur.fetchall()
    header = [('title', 'metacritic', 'release_year')]
    data = header + data
    return data

#Récupération du nombre de jeu rajouté par chaque utilisateur ainsi que la note moyenne de ces derniers
def executeRequestPlayerGames(cur) :
    cur.execute(
        '''select(
            p.id,
            p.first_name,
            p.last_name,
            count(g.id),
            avg(g.metacritic)::numeric(10,2))
        from player p
        right join game g on g.added_by = p.id
        group by p.id
        order by p.id'''
    )

    data = cur.fetchall()
    header = [('player id', 'first name', 'last name', 'number of games', 'average game\'s score')]
    data = header + data
    return data

#Récupération pour chaque genre du nombre de jeux qui le contiennent
def executeRequestGamesGenre(cur) :
    cur.execute(
        '''select
            g.id,
            g.name,
            count(gg.games_id)
        from genre g
        join games_genre gg on gg.genre_id = g.id
        group by g.id
        order by g.id'''
    )

    data = cur.fetchall()
    header = [('genre id', 'genre','number of games')]
    data = header + data
    return data