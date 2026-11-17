# 🔮 BeatPurple Backend — Sistema de Gerenciamento Musical (OO + SQLite3)

Aplicação back-end desenvolvida em **Python** seguindo o paradigma de **Orientação a Objetos (OO)**, integrada a um banco de dados relacional **SQLite3** e à **iTunes Search API** para busca e importação automática de artistas, álbuns, músicas e playlists.

---

## ✨ Funcionalidades

- **CRUD Completo (Create, Read, Update, Delete):** Gerenciamento completo via terminal para **Artistas**, **Álbuns**, **Músicas** e **Playlists**.
- **Banco de Dados Relacional (4 Tabelas):** Integridade referencial garantida com chaves estrangeiras (`FOREIGN KEY`), exclusão em cascata (`ON DELETE CASCADE`) e consultas cruzadas com `INNER JOIN`.
- **Integração com API Externa (iTunes Search API):**
  - Busca automática de **Artistas**, **Álbuns** e **Músicas** reais sem necessidade de preenchimento manual.
  - **Importação em lote:** Seleção múltipla por números (ex: `1, 2, 6, 9`) ou importação de toda a lista de resultados de uma só vez (`todas`).
  - **Prevenção de duplicidade:** Reaproveitamento automático de artistas, álbuns e faixas já cadastrados no banco.
- **Gerenciamento Avançado de Playlists:** Criação direta via API ou por IDs do banco, listagem agrupada por playlist e submenu dedicado para editar nome, autor, substituir faixas ou adicionar novas músicas.
- **Painel de Estatísticas:** Visão geral do acervo com contagem total de registros e soma da duração de áudio cadastrada.
- **Arquitetura Modular:** Separação clara de responsabilidades entre conexão com banco, modelos de domínio, repositório SQL, serviço de API e interface de terminal.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

- **Python 3** (Linguagem principal)
- **Bibliotecas Nativas (Standard Library — não requerem instalação via `pip`):**
  - `sqlite3`: Criação e manipulação do banco de dados relacional local (`beatpurple.db`).
  - `urllib.request` / `urllib.parse`: Consumo da API REST do iTunes via HTTP.
  - `json`: Desserialização dos dados retornados pela API.

---

## 📂 Estrutura do Projeto

```text
acervo_musical/
├── database.py      # Classe GerenciadorBD: conexão SQLite3 e criação das 4 tabelas
├── models.py        # Classes de domínio OO (Artista, Album, Musica, Playlist)
├── repository.py    # Classe BeatPurpleRepository: operações CRUD, estatísticas e importação relacional
├── api_service.py   # Classe ItunesService: integração com a iTunes Search API
├── main.py          # Interface de menus interativos no terminal e validação de entradas
├── beatpurple.db    # Banco de dados SQLite3 gerado automaticamente na execução
├── .gitignore       # Arquivos temporários ignorados pelo Git
└── README.md        # Documentação do projeto
