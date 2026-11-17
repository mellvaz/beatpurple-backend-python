import json
import urllib.request
import urllib.parse


class ItunesService:
    def __init__(self):
        self.base_url = "https://itunes.apple.com/search"

    def _fazer_requisicao(self, params):
        query = urllib.parse.urlencode(params)
        url = f"{self.base_url}?{query}"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as resposta:
                dados = json.loads(resposta.read().decode("utf-8"))
                return True, dados.get("results", [])
        except Exception as erro:
            return False, f"Falha ao consultar API (verifique sua conexão): {erro}"

    def buscar_artistas(self, termo, limite=10):
        return self._fazer_requisicao({
            "term": termo,
            "limit": limite,
            "entity": "musicArtist"
        })

    def buscar_albuns(self, termo, limite=10):
        return self._fazer_requisicao({
            "term": termo,
            "limit": limite,
            "entity": "album"
        })

    def buscar_musicas(self, termo, limite=10):
        return self._fazer_requisicao({
            "term": termo,
            "limit": limite,
            "entity": "song"
        })