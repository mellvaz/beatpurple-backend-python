import sqlite3
from models import Artista, Album, Musica, Playlist


class BeatPurpleRepository:
    def __init__(self, db):
        self.db = db

    # ================= CRUD ARTISTAS =================
    def criar_artista(self, artista: Artista):
        self.db.cursor.execute(
            "INSERT INTO artistas (nome, genero, pais) VALUES (?, ?, ?)",
            (artista.nome, artista.genero, artista.pais)
        )
        self.db.conexao.commit()
        return self.db.cursor.lastrowid

    def obter_ou_criar_artista(self, nome, genero, pais):
        self.db.cursor.execute("SELECT id FROM artistas WHERE nome = ?", (nome,))
        existente = self.db.cursor.fetchone()
        if existente:
            return existente[0]
        return self.criar_artista(Artista(nome, genero, pais))

    def listar_artistas(self):
        self.db.cursor.execute("SELECT id, nome, genero, pais FROM artistas")
        linhas = self.db.cursor.fetchall()
        return [Artista(nome=l[1], genero=l[2], pais=l[3], id=l[0]) for l in linhas]

    def atualizar_artista(self, id_artista, novo_nome, novo_genero, novo_pais):
        self.db.cursor.execute(
            "UPDATE artistas SET nome = ?, genero = ?, pais = ? WHERE id = ?",
            (novo_nome, novo_genero, novo_pais, id_artista)
        )
        self.db.conexao.commit()
        return self.db.cursor.rowcount > 0

    def deletar_artista(self, id_artista):
        self.db.cursor.execute("DELETE FROM artistas WHERE id = ?", (id_artista,))
        self.db.conexao.commit()
        return self.db.cursor.rowcount > 0

    # ================= CRUD ÁLBUNS =================
    def criar_album(self, album: Album):
        try:
            self.db.cursor.execute(
                "INSERT INTO albuns (titulo, ano_lancamento, artista_id) VALUES (?, ?, ?)",
                (album.titulo, album.ano_lancamento, album.artista_id)
            )
            self.db.conexao.commit()
            return True, self.db.cursor.lastrowid
        except sqlite3.IntegrityError:
            return False, "Erro: O ID do artista informado não existe."

    def obter_ou_criar_album(self, titulo, ano_lancamento, artista_id):
        self.db.cursor.execute(
            "SELECT id FROM albuns WHERE titulo = ? AND artista_id = ?",
            (titulo, artista_id)
        )
        existente = self.db.cursor.fetchone()
        if existente:
            return existente[0]
        _, novo_id = self.criar_album(Album(titulo, ano_lancamento, artista_id))
        return novo_id

    def listar_albuns(self):
        self.db.cursor.execute('''
            SELECT albuns.id, albuns.titulo, albuns.ano_lancamento, artistas.nome
            FROM albuns
            INNER JOIN artistas ON albuns.artista_id = artistas.id
        ''')
        return self.db.cursor.fetchall()

    def atualizar_album(self, id_album, novo_titulo, novo_ano):
        self.db.cursor.execute(
            "UPDATE albuns SET titulo = ?, ano_lancamento = ? WHERE id = ?",
            (novo_titulo, novo_ano, id_album)
        )
        self.db.conexao.commit()
        return self.db.cursor.rowcount > 0

    def deletar_album(self, id_album):
        self.db.cursor.execute("DELETE FROM albuns WHERE id = ?", (id_album,))
        self.db.conexao.commit()
        return self.db.cursor.rowcount > 0

    # ================= CRUD MÚSICAS =================
    def criar_musica(self, musica: Musica):
        try:
            self.db.cursor.execute(
                "INSERT INTO musicas (titulo, duracao_segundos, album_id) VALUES (?, ?, ?)",
                (musica.titulo, musica.duracao_segundos, musica.album_id)
            )
            self.db.conexao.commit()
            return True, self.db.cursor.lastrowid
        except sqlite3.IntegrityError:
            return False, "Erro: O ID do álbum informado não existe."

    def listar_musicas(self):
        self.db.cursor.execute('''
            SELECT musicas.id, musicas.titulo, musicas.duracao_segundos, albuns.titulo, artistas.nome
            FROM musicas
            INNER JOIN albuns ON musicas.album_id = albuns.id
            INNER JOIN artistas ON albuns.artista_id = artistas.id
        ''')
        return self.db.cursor.fetchall()

    def atualizar_musica(self, id_musica, novo_titulo, nova_duracao):
        self.db.cursor.execute(
            "UPDATE musicas SET titulo = ?, duracao_segundos = ? WHERE id = ?",
            (novo_titulo, nova_duracao, id_musica)
        )
        self.db.conexao.commit()
        return self.db.cursor.rowcount > 0

    def deletar_musica(self, id_musica):
        self.db.cursor.execute("DELETE FROM musicas WHERE id = ?", (id_musica,))
        self.db.conexao.commit()
        return self.db.cursor.rowcount > 0

    # ================= CRUD PLAYLISTS =================
    def criar_playlist(self, playlist: Playlist):
        try:
            self.db.cursor.execute(
                "INSERT INTO playlists (nome_playlist, criador, musica_id) VALUES (?, ?, ?)",
                (playlist.nome_playlist, playlist.criador, playlist.musica_id)
            )
            self.db.conexao.commit()
            return True, self.db.cursor.lastrowid
        except sqlite3.IntegrityError:
            return False, "Erro: O ID da música informada não existe."

    def listar_playlists(self):
        self.db.cursor.execute('''
            SELECT playlists.id, playlists.nome_playlist, playlists.criador, musicas.titulo, artistas.nome
            FROM playlists
            INNER JOIN musicas ON playlists.musica_id = musicas.id
            INNER JOIN albuns ON musicas.album_id = albuns.id
            INNER JOIN artistas ON albuns.artista_id = artistas.id
        ''')
        return self.db.cursor.fetchall()

    def atualizar_nome_playlist(self, nome_antigo, novo_nome):
        self.db.cursor.execute(
            "UPDATE playlists SET nome_playlist = ? WHERE nome_playlist = ?",
            (novo_nome, nome_antigo)
        )
        self.db.conexao.commit()
        return self.db.cursor.rowcount > 0

    def atualizar_autor_playlist(self, nome_playlist, novo_criador):
        self.db.cursor.execute(
            "UPDATE playlists SET criador = ? WHERE nome_playlist = ?",
            (novo_criador, nome_playlist)
        )
        self.db.conexao.commit()
        return self.db.cursor.rowcount > 0

    def trocar_musica_playlist(self, id_registro, nova_musica_id):
        try:
            self.db.cursor.execute(
                "UPDATE playlists SET musica_id = ? WHERE id = ?",
                (nova_musica_id, id_registro)
            )
            self.db.conexao.commit()
            if self.db.cursor.rowcount > 0:
                return True, "✅ Música substituída na playlist com sucesso!"
            return False, "❌ Registro não encontrado."
        except sqlite3.IntegrityError:
            return False, "❌ Erro: O ID da nova música informada não existe."

    def deletar_playlist(self, id_playlist):
        self.db.cursor.execute("DELETE FROM playlists WHERE id = ?", (id_playlist,))
        self.db.conexao.commit()
        return self.db.cursor.rowcount > 0

    # ================= IMPORTAÇÕES AUTOMÁTICAS VIA API =================
    def importar_artista_api(self, dados_artista):
        nome = dados_artista.get("artistName", "Desconhecido")
        genero = dados_artista.get("primaryGenreName", "Geral")
        pais = dados_artista.get("country", "Internacional")
        artista_id = self.obter_ou_criar_artista(nome, genero, pais)
        return {"id": artista_id, "nome": nome, "genero": genero, "pais": pais}

    def importar_album_api(self, dados_album):
        nome_artista = dados_album.get("artistName", "Desconhecido")
        genero = dados_album.get("primaryGenreName", "Geral")
        pais = dados_album.get("country", "Internacional")

        titulo_album = dados_album.get("collectionName", "Single")
        data_lancamento = dados_album.get("releaseDate", "2024")
        ano_lancamento = int(data_lancamento[:4]) if data_lancamento[:4].isdigit() else 2024

        artista_id = self.obter_ou_criar_artista(nome_artista, genero, pais)
        album_id = self.obter_ou_criar_album(titulo_album, ano_lancamento, artista_id)

        return {"id": album_id, "titulo": titulo_album, "ano": ano_lancamento, "artista": nome_artista}

    def importar_musica_api(self, dados_faixa):
        nome_artista = dados_faixa.get("artistName", "Desconhecido")
        genero = dados_faixa.get("primaryGenreName", "Geral")
        pais = dados_faixa.get("country", "Internacional")

        titulo_album = dados_faixa.get("collectionName", "Single")
        data_lancamento = dados_faixa.get("releaseDate", "2024")
        ano_lancamento = int(data_lancamento[:4]) if data_lancamento[:4].isdigit() else 2024

        titulo_musica = dados_faixa.get("trackName", "Sem Título")
        duracao_segundos = dados_faixa.get("trackTimeMillis", 0) // 1000

        artista_id = self.obter_ou_criar_artista(nome_artista, genero, pais)
        album_id = self.obter_ou_criar_album(titulo_album, ano_lancamento, artista_id)
        musica_id = self.obter_ou_criar_musica(titulo_musica, duracao_segundos, album_id)

        return {
            "artista": nome_artista,
            "album": titulo_album,
            "musica": titulo_musica,
            "musica_id": musica_id
        }

    # ================= MELHORIAS DE DUPLICIDADE E ESTATÍSTICAS =================
    def obter_ou_criar_musica(self, titulo, duracao_segundos, album_id):
        self.db.cursor.execute(
            "SELECT id FROM musicas WHERE titulo = ? AND album_id = ?",
            (titulo, album_id)
        )
        existente = self.db.cursor.fetchone()
        if existente:
            return existente[0]
        _, novo_id = self.criar_musica(Musica(titulo, duracao_segundos, album_id))
        return novo_id

    def obter_estatisticas(self):
        self.db.cursor.execute("SELECT COUNT(*) FROM artistas")
        total_artistas = self.db.cursor.fetchone()[0]

        self.db.cursor.execute("SELECT COUNT(*) FROM albuns")
        total_albuns = self.db.cursor.fetchone()[0]

        self.db.cursor.execute("SELECT COUNT(*), COALESCE(SUM(duracao_segundos), 0) FROM musicas")
        total_musicas, segundos_totais = self.db.cursor.fetchone()

        self.db.cursor.execute("SELECT COUNT(DISTINCT nome_playlist) FROM playlists")
        total_playlists = self.db.cursor.fetchone()[0]

        return {
            "artistas": total_artistas,
            "albuns": total_albuns,
            "musicas": total_musicas,
            "playlists": total_playlists,
            "segundos_totais": segundos_totais
        }