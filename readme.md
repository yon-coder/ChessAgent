# ChessAgent ♟️

Agente autônomo de xadrez desenvolvido em Python, com visão computacional, tomada de decisões e aprendizado de máquina.

## Objetivo

Desenvolver uma IA capaz de:

- Reconhecer um tabuleiro de xadrez através de capturas de tela.
- Identificar peças e suas posições.
- Calcular e executar movimentos automaticamente.
- Aprender através de partidas contra outros jogadores e self-play.
- Melhorar progressivamente seu desempenho.

## Tecnologias

- Python
- OpenCV
- NumPy
- MSS
- python-chess
- PyAutoGUI
- PyTorch

## Estrutura

```text
ChessAgent/
├── main.py
├── vision.py
├── inspect_board.py
├── board.py
├── engine.py
├── controller.py
├── learning.py
├── dataset/
│   ├── raw/
│   ├── labeled/
│   └── metadata/
├── models/
├── screenshots/
├── requirements.txt
└── .gitignore
```

## Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
cd ChessAgent
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative no Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Inicie o programa:

```bash
python main.py
```

Para inspecionar as casas de uma captura já salva:

```bash
python inspect_board.py
```

## Desenvolvimento

O projeto está em desenvolvimento.

Etapas planejadas:

1. Captura e processamento do tabuleiro.
2. Reconhecimento das peças.
3. Reconstrução do estado da partida.
4. Motor de decisão.
5. Automação dos movimentos.
6. Aprendizado híbrido e self-play.

---

Projeto experimental de inteligência artificial e visão computacional.git