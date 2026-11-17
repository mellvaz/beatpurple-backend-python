from database import GerenciadorBD
from models import Artista, Album, Musica, Playlist
from repository import BeatPurpleRepository
from api_service import ItunesService


def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("⚠️ Entrada inválida! Digite apenas números inteiros.")


def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("⚠️ Este campo não pode ficar vazio.")


def selecionar_itens_api(resultados, nome_entidade="itens"):
    """
    Permite escolher um número (ex: 1), vários separados por vírgula/espaço (ex: 1, 2, 6, 9)
    ou 'todas' para importar toda a lista de uma vez.
    """
    while True:
        entrada = input(
            f"\nDigite os números dos {nome_entidade} (ex: 1, 2, 6, 9), 'todas' ou 0 para cancelar: "
        ).strip().lower()

        if entrada in ("0", "cancelar", "sair"):
            return []

        if entrada in ("todas", "todos", "t", "all"):
            return resultados

        # Troca vírgulas por espaço para aceitar tanto "1, 2, 6" quanto "1 2 6"
        partes = entrada.replace(",", " ").split()
        indices_escolhidos = []
        valido = True

        for parte in partes:
            if not parte.isdigit():
                valido = False
                break
            num = int(parte)
            if 1 <= num <= len(resultados):
                if (num - 1) not in indices_escolhidos:
                    indices_escolhidos.append(num - 1)
            else:
                valido = False
                break

        if valido and indices_escolhidos:
            return [resultados[i] for i in indices_escolhidos]

        print(f"⚠️ Entrada inválida! Escolha números entre 1 e {len(resultados)}, 'todas' ou 0.")


# ================= 1. MENU ARTISTAS =================
def menu_artistas(repo, api):
    while True:
        print("\n--- 🎤 GERENCIAR ARTISTAS ---")
        print("1. 🌐 Buscar e Importar Artista(s) da API")
        print("2. Cadastrar Artista Manualmente")
        print("3. Listar Artistas")
        print("4. Atualizar Artista")
        print("5. Excluir Artista")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            termo = ler_texto("Digite o nome do artista/banda: ")
            print("🔍 Buscando na API da Apple...")
            sucesso, resultados = api.buscar_artistas(termo, limite=10)
            if not sucesso:
                print(f"❌ {resultados}")
                continue
            if not resultados:
                print("📭 Nenhum artista encontrado na API.")
                continue

            print("\n📋 Artistas encontrados:")
            for idx, item in enumerate(resultados, start=1):
                nome = item.get("artistName", "Desconhecido")
                genero = item.get("primaryGenreName", "Geral")
                pais = item.get("country", "Internacional")
                print(f"  {idx}. {nome} | Gênero: {genero} | País: {pais}")
            print("  0. Cancelar")

            selecionados = selecionar_itens_api(resultados, "artistas")
            for item in selecionados:
                resumo = repo.importar_artista_api(item)
                print(f"✅ Artista '{resumo['nome']}' importado! (ID: {resumo['id']})")

        elif opcao == "2":
            nome = ler_texto("Nome do artista/banda: ")
            genero = ler_texto("Gênero musical: ")
            pais = input("País de origem (Enter para 'Não informado'): ").strip() or "Não informado"
            novo_id = repo.criar_artista(Artista(nome, genero, pais))
            print(f"✅ Artista cadastrado com sucesso! ID: {novo_id}")

        elif opcao == "3":
            artistas = repo.listar_artistas()
            if not artistas:
                print("📭 Nenhum artista cadastrado.")
            else:
                print("\n📋 Lista de Artistas:")
                for a in artistas:
                    print(f"  {a}")

        elif opcao == "4":
            id_art = ler_inteiro("ID do artista que deseja atualizar: ")
            nome = ler_texto("Novo nome: ")
            genero = ler_texto("Novo gênero: ")
            pais = ler_texto("Novo país: ")
            if repo.atualizar_artista(id_art, nome, genero, pais):
                print("✅ Artista atualizado com sucesso!")
            else:
                print("❌ Artista não encontrado.")

        elif opcao == "5":
            id_art = ler_inteiro("ID do artista que deseja excluir: ")
            if repo.deletar_artista(id_art):
                print("🗑️ Artista (e seus álbuns/músicas vinculados) excluído!")
            else:
                print("❌ Artista não encontrado.")

        elif opcao == "0":
            break
        else:
            print("⚠️ Opção inválida.")


# ================= 2. MENU ÁLBUNS =================
def menu_albuns(repo, api):
    while True:
        print("\n--- 💿 GERENCIAR ÁLBUNS ---")
        print("1. 🌐 Buscar e Importar Álbum(ns) da API")
        print("2. Cadastrar Álbum Manualmente")
        print("3. Listar Álbuns")
        print("4. Atualizar Álbum")
        print("5. Excluir Álbum")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            termo = ler_texto("Digite o nome do álbum ou artista: ")
            print("🔍 Buscando álbuns na API da Apple...")
            sucesso, resultados = api.buscar_albuns(termo, limite=10)
            if not sucesso:
                print(f"❌ {resultados}")
                continue
            if not resultados:
                print("📭 Nenhum álbum encontrado na API.")
                continue

            print("\n📋 Álbuns encontrados:")
            for idx, item in enumerate(resultados, start=1):
                titulo = item.get("collectionName", "Single")
                artista = item.get("artistName", "Desconhecido")
                ano = item.get("releaseDate", "----")[:4]
                print(f"  {idx}. {titulo} ({ano}) — {artista}")
            print("  0. Cancelar")

            selecionados = selecionar_itens_api(resultados, "álbuns")
            for item in selecionados:
                resumo = repo.importar_album_api(item)
                print(f"✅ Álbum '{resumo['titulo']}' (Artista: {resumo['artista']}) importado! (ID: {resumo['id']})")

        elif opcao == "2":
            titulo = ler_texto("Título do álbum: ")
            ano = ler_inteiro("Ano de lançamento: ")
            artista_id = ler_inteiro("ID do Artista dono do álbum: ")
            sucesso, resultado = repo.criar_album(Album(titulo, ano, artista_id))
            if sucesso:
                print(f"✅ Álbum cadastrado com sucesso! ID: {resultado}")
            else:
                print(f"❌ {resultado}")

        elif opcao == "3":
            albuns = repo.listar_albuns()
            if not albuns:
                print("📭 Nenhum álbum cadastrado.")
            else:
                print("\n📋 Lista de Álbuns:")
                for al in albuns:
                    print(f"  [{al[0]}] {al[1]} ({al[2]}) — Artista: {al[3]}")

        elif opcao == "4":
            id_al = ler_inteiro("ID do álbum que deseja atualizar: ")
            titulo = ler_texto("Novo título: ")
            ano = ler_inteiro("Novo ano de lançamento: ")
            if repo.atualizar_album(id_al, titulo, ano):
                print("✅ Álbum atualizado com sucesso!")
            else:
                print("❌ Álbum não encontrado.")

        elif opcao == "5":
            id_al = ler_inteiro("ID do álbum que deseja excluir: ")
            if repo.deletar_album(id_al):
                print("🗑️ Álbum excluído com sucesso!")
            else:
                print("❌ Álbum não encontrado.")

        elif opcao == "0":
            break
        else:
            print("⚠️ Opção inválida.")


# ================= 3. MENU MÚSICAS =================
def menu_musicas(repo, api):
    while True:
        print("\n--- 🎵 GERENCIAR MÚSICAS ---")
        print("1. 🌐 Buscar e Importar Música(s) da API")
        print("2. Cadastrar Música Manualmente")
        print("3. Listar Músicas")
        print("4. Atualizar Música")
        print("5. Excluir Música")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            termo = ler_texto("Digite o nome da música ou artista: ")
            print("🔍 Buscando músicas na API da Apple...")
            sucesso, resultados = api.buscar_musicas(termo, limite=10)
            if not sucesso:
                print(f"❌ {resultados}")
                continue
            if not resultados:
                print("📭 Nenhuma música encontrada na API.")
                continue

            print("\n📋 Músicas encontradas:")
            for idx, item in enumerate(resultados, start=1):
                nome = item.get("trackName", "Sem título")
                artista = item.get("artistName", "Desconhecido")
                album = item.get("collectionName", "Single")
                print(f"  {idx}. {nome} — {artista} (Álbum: {album})")
            print("  0. Cancelar")

            selecionados = selecionar_itens_api(resultados, "músicas")
            for item in selecionados:
                resumo = repo.importar_musica_api(item)
                print(f"✅ Música '{resumo['musica']}' ({resumo['artista']}) importada! (ID: {resumo['musica_id']})")

        elif opcao == "2":
            titulo = ler_texto("Título da música: ")
            duracao = ler_inteiro("Duração em segundos (ex: 210): ")
            album_id = ler_inteiro("ID do Álbum da música: ")
            sucesso, resultado = repo.criar_musica(Musica(titulo, duracao, album_id))
            if sucesso:
                print(f"✅ Música cadastrada com sucesso! ID: {resultado}")
            else:
                print(f"❌ {resultado}")

        elif opcao == "3":
            musicas = repo.listar_musicas()
            if not musicas:
                print("📭 Nenhuma música cadastrada.")
            else:
                print("\n📋 Lista de Músicas:")
                for m in musicas:
                    minutos = m[2] // 60
                    segundos = m[2] % 60
                    print(f"  [{m[0]}] {m[1]} ({minutos}:{segundos:02d}) — Álbum: {m[3]} | Artista: {m[4]}")

        elif opcao == "4":
            id_m = ler_inteiro("ID da música que deseja atualizar: ")
            titulo = ler_texto("Novo título: ")
            duracao = ler_inteiro("Nova duração em segundos: ")
            if repo.atualizar_musica(id_m, titulo, duracao):
                print("✅ Música atualizada com sucesso!")
            else:
                print("❌ Música não encontrada.")

        elif opcao == "5":
            id_m = ler_inteiro("ID da música que deseja excluir: ")
            if repo.deletar_musica(id_m):
                print("🗑️ Música excluída com sucesso!")
            else:
                print("❌ Música não encontrada.")

        elif opcao == "0":
            break
        else:
            print("⚠️ Opção inválida.")


# ================= 4. MENU PLAYLISTS =================
def submenu_editar_playlist(repo, api):
    playlists = repo.listar_playlists()
    if not playlists:
        print("📭 Nenhuma playlist cadastrada para editar.")
        return

    # Agrupa os nomes únicos das playlists existentes
    nomes_unicos = []
    criadores_por_playlist = {}
    for p in playlists:
        if p[1] not in nomes_unicos:
            nomes_unicos.append(p[1])
            criadores_por_playlist[p[1]] = p[2]

    print("\n📋 Playlists disponíveis:")
    for idx, nome in enumerate(nomes_unicos, start=1):
        print(f"  {idx}. {nome} (por {criadores_por_playlist[nome]})")
    print("  0. Voltar")

    escolha_pl = ler_inteiro("\nEscolha o número da playlist que deseja editar: ")
    if escolha_pl == 0 or not (1 <= escolha_pl <= len(nomes_unicos)):
        return

    nome_atual = nomes_unicos[escolha_pl - 1]
    criador_atual = criadores_por_playlist[nome_atual]

    while True:
        print(f"\n--- ✏️ EDITANDO PLAYLIST: '{nome_atual}' (por {criador_atual}) ---")
        print("1. Atualizar Nome da Playlist")
        print("2. Atualizar Autor/Criador")
        print("3. Trocar uma Música da Playlist")
        print("4. Adicionar Mais Músicas à Playlist")
        print("0. Voltar")

        sub_opcao = input("Escolha o que deseja editar: ").strip()

        if sub_opcao == "1":
            novo_nome = ler_texto("Novo nome para a playlist: ")
            if repo.atualizar_nome_playlist(nome_atual, novo_nome):
                print(f"✅ Nome alterado de '{nome_atual}' para '{novo_nome}'!")
                nome_atual = novo_nome
            else:
                print("❌ Não foi possível atualizar o nome.")

        elif sub_opcao == "2":
            novo_criador = ler_texto("Novo nome do autor/criador: ")
            if repo.atualizar_autor_playlist(nome_atual, novo_criador):
                print(f"✅ Autor alterado para '{novo_criador}'!")
                criador_atual = novo_criador
            else:
                print("❌ Não foi possível atualizar o autor.")

        elif sub_opcao == "3":
            itens_da_playlist = [p for p in repo.listar_playlists() if p[1] == nome_atual]
            print(f"\n🎵 Músicas atuais em '{nome_atual}':")
            for item in itens_da_playlist:
                print(f"  [Registro ID: {item[0]}] {item[3]} ({item[4]})")

            musicas_banco = repo.listar_musicas()
            print("\n📋 Músicas disponíveis no banco para troca:")
            for m in musicas_banco:
                print(f"  [Música ID: {m[0]}] {m[1]} — {m[4]}")

            id_reg = ler_inteiro("\nDigite o Registro ID da faixa que quer substituir: ")
            nova_m_id = ler_inteiro("Digite o Música ID que vai entrar no lugar: ")
            _, msg = repo.trocar_musica_playlist(id_reg, nova_m_id)
            print(msg)

        elif sub_opcao == "4":
            print("\nComo deseja adicionar músicas?")
            print("  1. 🌐 Buscar na API do iTunes")
            print("  2. Escolher das músicas já salvas no banco (por ID)")
            modo = input("Escolha (1 ou 2): ").strip()

            if modo == "1":
                termo = ler_texto("Digite o nome da música ou artista: ")
                sucesso, resultados = api.buscar_musicas(termo, limite=10)
                if not sucesso or not resultados:
                    print("📭 Nenhuma música encontrada.")
                    continue
                for idx, item in enumerate(resultados, start=1):
                    print(f"  {idx}. {item.get('trackName')} — {item.get('artistName')}")
                selecionados = selecionar_itens_api(resultados, "músicas")
                for item in selecionados:
                    resumo = repo.importar_musica_api(item)
                    repo.criar_playlist(Playlist(nome_atual, criador_atual, resumo["musica_id"]))
                    print(f"✅ '{resumo['musica']}' adicionada à '{nome_atual}'!")

            elif modo == "2":
                musicas_banco = repo.listar_musicas()
                for m in musicas_banco:
                    print(f"  [{m[0]}] {m[1]} — {m[4]}")
                entrada = input("Digite os IDs (ex: 1, 2, 3) ou 'todas': ").strip().lower()
                if entrada in ("todas", "todos", "t"):
                    ids = [m[0] for m in musicas_banco]
                else:
                    ids = [int(p) for p in entrada.replace(",", " ").split() if p.isdigit()]
                for m_id in ids:
                    ok, res = repo.criar_playlist(Playlist(nome_atual, criador_atual, m_id))
                    print(f"✅ Música ID {m_id} adicionada!" if ok else f"❌ ID {m_id}: {res}")

        elif sub_opcao == "0":
            break
        else:
            print("⚠️ Opção inválida.")


def menu_playlists(repo, api):
    while True:
        print("\n--- 🎧 GERENCIAR PLAYLISTS ---")
        print("1. 🌐 Buscar Música(s) na API e Criar/Adicionar à Playlist")
        print("2. Adicionar Música(s) já Cadastrada(s) (por ID)")
        print("3. Listar Playlists")
        print("4. ✏️ Editar Playlist (Nome, Autor, Trocar ou Adicionar Músicas)")
        print("5. Remover Item da Playlist")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome_pl = ler_texto("Nome da playlist: ")
            criador = ler_texto("Nome do criador: ")
            termo = ler_texto("Buscar música na API para adicionar: ")
            print("🔍 Buscando músicas na API da Apple...")
            sucesso, resultados = api.buscar_musicas(termo, limite=10)
            if not sucesso:
                print(f"❌ {resultados}")
                continue
            if not resultados:
                print("📭 Nenhuma música encontrada na API.")
                continue

            print("\n📋 Músicas encontradas:")
            for idx, item in enumerate(resultados, start=1):
                nome = item.get("trackName", "Sem título")
                artista = item.get("artistName", "Desconhecido")
                print(f"  {idx}. {nome} — {artista}")
            print("  0. Cancelar")

            selecionados = selecionar_itens_api(resultados, "músicas")
            for item in selecionados:
                resumo = repo.importar_musica_api(item)
                ok, pl_id = repo.criar_playlist(Playlist(nome_pl, criador, resumo["musica_id"]))
                if ok:
                    print(f"✅ '{resumo['musica']}' adicionada à playlist '{nome_pl}'! (ID: {pl_id})")

        elif opcao == "2":
            musicas_cadastradas = repo.listar_musicas()
            if not musicas_cadastradas:
                print("📭 Nenhuma música cadastrada no banco ainda.")
                continue

            print("\n📋 Músicas disponíveis no banco:")
            for m in musicas_cadastradas:
                print(f"  [{m[0]}] {m[1]} — {m[4]}")

            nome_pl = ler_texto("\nNome da playlist: ")
            criador = ler_texto("Nome do criador: ")

            while True:
                entrada = input(
                    "Digite os IDs das músicas (ex: 1, 2, 3), 'todas' ou 0 para cancelar: "
                ).strip().lower()

                if entrada in ("0", "cancelar"):
                    break

                if entrada in ("todas", "todos", "t"):
                    ids_escolhidos = [m[0] for m in musicas_cadastradas]
                else:
                    partes = entrada.replace(",", " ").split()
                    if not partes or not all(p.isdigit() for p in partes):
                        print("⚠️ Entrada inválida! Digite IDs separados por vírgula (ex: 1, 2, 3) ou 'todas'.")
                        continue
                    ids_escolhidos = [int(p) for p in partes]

                for m_id in ids_escolhidos:
                    sucesso, resultado = repo.criar_playlist(Playlist(nome_pl, criador, m_id))
                    if sucesso:
                        print(f"✅ Música ID {m_id} adicionada à playlist '{nome_pl}'! (Registro ID: {resultado})")
                    else:
                        print(f"❌ Música ID {m_id}: {resultado}")
                break

        elif opcao == "3":
            playlists = repo.listar_playlists()
            if not playlists:
                print("📭 Nenhuma playlist cadastrada.")
            else:
                agrupadas = {}
                for p in playlists:
                    chave = (p[1], p[2])
                    agrupadas.setdefault(chave, []).append((p[0], p[3], p[4]))

                print("\n📋 Playlists Cadastradas:")
                for (nome_pl, criador), faixas in agrupadas.items():
                    print(f"\n  🎧 {nome_pl} (Criador: {criador}) — {len(faixas)} música(s):")
                    for reg_id, faixa, artista in faixas:
                        print(f"     • [Reg ID: {reg_id}] {faixa} — {artista}")

        elif opcao == "4":
            submenu_editar_playlist(repo, api)

        elif opcao == "5":
            id_p = ler_inteiro("ID do registro da playlist para excluir: ")
            if repo.deletar_playlist(id_p):
                print("🗑️ Registro removido da playlist!")
            else:
                print("❌ Registro não encontrado.")

        elif opcao == "0":
            break
        else:
            print("⚠️ Opção inválida.")

# ================= MENU PRINCIPAL =================
def main():
    db = GerenciadorBD("beatpurple.db")
    repo = BeatPurpleRepository(db)
    api = ItunesService()

    try:
        while True:
            print("\n=========================================")
            print("   🔮 BEATPURPLE BACKEND - SISTEMA OO    ")
            print("=========================================")
            print("1. Gerenciar Artistas")
            print("2. Gerenciar Álbuns")
            print("3. Gerenciar Músicas")
            print("4. Gerenciar Playlists")
            print("5. Estatísticas do Acervo")
            print("0. Sair")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                menu_artistas(repo, api)
            elif opcao == "2":
                menu_albuns(repo, api)
            elif opcao == "3":
                menu_musicas(repo, api)
            elif opcao == "4":
                menu_playlists(repo, api)
            elif opcao == "5":
                stats = repo.obter_estatisticas()
                mins = stats["segundos_totais"] // 60
                segs = stats["segundos_totais"] % 60
                print("\n--- 📊 VISÃO GERAL DO ACERVO BEATPURPLE ---")
                print(f"  🎤 Artistas cadastrados:  {stats['artistas']}")
                print(f"  💿 Álbuns cadastrados:    {stats['albuns']}")
                print(f"  🎵 Músicas cadastradas:   {stats['musicas']}")
                print(f"  🎧 Playlists criadas:     {stats['playlists']}")
                print(f"  ⏱️ Tempo total de áudio:  {mins} min e {segs:02d} seg")
            elif opcao == "0":
                print("\n👋 Encerrando o BeatPurple Backend. Até logo!")
                break
            else:
                print("⚠️ Opção inválida! Escolha entre 0 e 4.")
    finally:
        db.fechar_conexao()


if __name__ == "__main__":
    main()