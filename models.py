class Artista:
    def __init__(self, nome, genero, pais, id=None):
        self.id = id
        self.nome = nome
        self.genero = genero
        self.pais = pais

    def __str__(self):
        return f"[{self.id}] {self.nome} | Gênero: {self.genero} | País: {self.pais}"


class Album:
    def __init__(self, titulo, ano_lancamento, artista_id, id=None):
        self.id = id
        self.titulo = titulo
        self.ano_lancamento = ano_lancamento
        self.artista_id = artista_id

    def __str__(self):
        return f"[{self.id}] {self.titulo} ({self.ano_lancamento}) | Artista ID: {self.artista_id}"


class Musica:
    def __init__(self, titulo, duracao_segundos, album_id, id=None):
        self.id = id
        self.titulo = titulo
        self.duracao_segundos = duracao_segundos
        self.album_id = album_id

    def duracao_formatada(self):
        minutos = self.duracao_segundos // 60
        segundos = self.duracao_segundos % 60
        return f"{minutos}:{segundos:02d}"

    def __str__(self):
        return f"[{self.id}] {self.titulo} ({self.duracao_formatada()}) | Álbum ID: {self.album_id}"


class Playlist:
    def __init__(self, nome_playlist, criador, musica_id, id=None):
        self.id = id
        self.nome_playlist = nome_playlist
        self.criador = criador
        self.musica_id = musica_id

    def __str__(self):
        return f"[{self.id}] Playlist: {self.nome_playlist} (por {self.criador}) | Música ID: {self.musica_id}"