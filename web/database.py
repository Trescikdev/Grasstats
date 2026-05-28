import sqlite3

DB_NAME = 'grastats.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # USERS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # FACILITIES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facilities (
            facility_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            name TEXT NOT NULL, 
            city TEXT,
            street TEXT,
            floor_type TEXT CHECK(floor_type IN ('teraflex', 'wood', 'rubber', 'other')),
            FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # TEAMS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            logo TEXT,
            colour TEXT,
            contact_person INTEGER,
            contact_person_2 INTEGER,
            location INTEGER,
            FOREIGN KEY (contact_person) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (contact_person_2) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (location) REFERENCES facilities(facility_id) ON DELETE SET NULL
        )
    ''')

    # MEMBERS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            user_id INTEGER,
            date_of_birth TEXT,
            team_id INTEGER,
            photo TEXT,
            nickname TEXT,
            role TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL
        )
    ''')

    # PLAYERS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            member_id INTEGER PRIMARY KEY,
            jersey_number INTEGER,
            position TEXT CHECK(position IN ('GK', 'D', 'C', 'F')),
            left_handed INTEGER, 
            height_cm INTEGER,
            weight_kg INTEGER,
            szfb_link TEXT,
            FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE       
        ) 
    ''')

    # MATCHES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_keeper INTEGER,
            home_team INTEGER,
            away_team INTEGER,
            date_time TEXT,
            facility INTEGER,
            season_round INTEGER,
            first_period_end TEXT,
            second_period_end TEXT,
            FOREIGN KEY (home_team) REFERENCES teams(team_id) ON DELETE SET NULL,
            FOREIGN KEY (away_team) REFERENCES teams(team_id) ON DELETE SET NULL,
            FOREIGN KEY (facility) REFERENCES facilities(facility_id) ON DELETE SET NULL
            FOREIGN KEY (match_keeper) REFERENCES teams(team_id) ON DELETE SET NULL
        )
    ''')

    # LINEUPS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS match_lineups (
            match_id INTEGER,
            player_id INTEGER,
            team_side INT,
            PRIMARY KEY (match_id, player_id),
            FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
            FOREIGN KEY (player_id) REFERENCES members(member_id) ON DELETE CASCADE,
            FOREIGN KEY (team_side) REFERENCES teams(team_id) ON DELETE CASCADE
        )
    ''')

    # SHOTS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shots (
            shot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER,
            x_coords REAL,
            y_coords REAL,
            date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            player_id INTEGER,
            FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
            FOREIGN KEY (player_id) REFERENCES members(member_id) ON DELETE SET NULL
        )
    ''')

    # SHOTS ON GOAL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shots_on_goal (
            shot_id INTEGER PRIMARY KEY,
            goalie_id INTEGER,
            FOREIGN KEY (shot_id) REFERENCES shots(shot_id) ON DELETE CASCADE,
            FOREIGN KEY (goalie_id) REFERENCES members(member_id) ON DELETE SET NULL
        )
    ''')

    # GOALS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            shot_id INTEGER PRIMARY KEY,
            assist_player_id INTEGER,
            situation TEXT CHECK (situation IN ('normal', 'powerplay', 'shorthanded', 'penalty')),
            players_on_ice TEXT,
            FOREIGN KEY (shot_id) REFERENCES shots_on_goal(shot_id) ON DELETE CASCADE,
            FOREIGN KEY (assist_player_id) REFERENCES members(member_id) ON DELETE SET NULL
        )
    ''')

    # BLOCKS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocks (
            block_id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER,
            player_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
            FOREIGN KEY (player_id) REFERENCES members(member_id) ON DELETE SET NULL
        )
    ''')

    # ROSTERS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rosters (
            team_id INTEGER,
            player_id INTEGER,
            FOREIGN KEY (team_id) REFERENCES teams(team_id) on DELETE CASCADE,
            FOREIGN KEY (player_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # INVITATION
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invitations (
        invitation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id INTEGER,
        sender_id INTEGER,
        receiver_id INTEGER,
        status TEXT DEFAULT 'pending', -- 'pending', 'accepted', 'declined'
        sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
        FOREIGN KEY (sender_id) REFERENCES users(id),
        FOREIGN KEY (receiver_id) REFERENCES users(id)
    )
    ''')

    # SETTINGS TABLE LATER (PREFERENCES LIKE LANGUAGES)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        user_id INTEGER,
        language TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()

