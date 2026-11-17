import sqlite3

class GerenciadorBD:
    def __init__(self, nome_banco="beatpurple.db"):
        self.conexao = sqlite3.connect(nome_banco)
        self.cursor = self.conexao.cursor()
        # Ativa o suporte a chaves estrangeiras no SQLite
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.criar_tabelas()

    def criar_tabelas(self):
        # 1. Tabela de Artistas (Tabela independente)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS artistas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                genero TEXT NOT NULL,
                pais TEXT NOT NULL
            )
        ''')

        # 2. Tabela de Álbuns (Relacionada com Artistas)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS albuns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                ano_lancamento INTEGER NOT NULL,
                artista_id INTEGER NOT NULL,
                FOREIGN KEY (artista_id) REFERENCES artistas(id) ON DELETE CASCADE
            )
        ''')

        # 3. Tabela de Músicas (Relacionada com Álbuns)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS musicas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                duracao_segundos INTEGER NOT NULL,
                album_id INTEGER NOT NULL,
                FOREIGN KEY (album_id) REFERENCES albuns(id) ON DELETE CASCADE
            )
        ''')

        # 4. Tabela de Playlists (Relacionada com Músicas)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_playlist TEXT NOT NULL,
                criador TEXT NOT NULL,
                musica_id INTEGER NOT NULL,
                FOREIGN KEY (musica_id) REFERENCES musicas(id) ON DELETE CASCADE
            )
        ''')

        self.conexao.commit()
        return 'Tabelas criadas com sucesso!'

    def fechar_conexao(self):
        self.conexao.close()