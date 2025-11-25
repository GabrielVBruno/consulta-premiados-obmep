<<<<<<< HEAD
# Consulta de premiados da OBMEP

Um programa em Python para consultar, filtrar e analisar os premiados na Olimpíada Brasileira de Matemática das Escolas Públicas (OBMEP).

## Funcionalidades

- Baixar todas as tabelas das listagens dos premiados como CSV utilizando urllib e Pandas.

![Captura de tela com quatro janelas: Google Chrome aberto numa página de premiação da OBMEP; editor de texto com arquivo CSV, o qual indica uma tabela de dados dos premiados de escola pública na 19ª OBMEP com medalha de ouro no nível 1; linha de comando em que está sendo rodado o programa indicando tabelas baixadas e opções para baixar ou continuar; linha de comando que indica alguns arquivos CSV baixados](assets/screenshot1.png)
Monitoramento e divisão de tabelas baixadas.

- Pesquisar e filtrar premiações por nome do premiado, nome e tipo da escola, edição, prêmio, UF, município e nível.

![Captura de tela da interface do programa com diversos campos e botões, e uma listagem. O campo "Nome de premiado (padrão regex)" possui o valor "^gabriel.*bruno". Na listagem, inicia-se indicada "Quantidade: 23" e seguem diversas linhas com informações sobre essas premiações, indicando nome, escola, município, prêmio, nível e edição](assets/screenshot2.png)
Premiações cujo nome do aluno atende ao padrão regex `^gabriel.*bruno`.

![Captura de tela da interface do programa com diversos campos e botões, e uma listagem. O campo "Nomes dos municípios" está preenchido com o valor "sao paulo". "Quantidade: 18" e diversos nomes e escolas na listagem](assets/screenshot3.png)
Premiações filtradas para serem apenas aquelas da 19ª OBMEP, com prêmio sendo uma medalha de ouro, na cidade de São Paulo, no nível 3 e de escolas particulares.

- Listar, em ordem, a quantidade de premiações por escola com os mesmos filtros.

![Captura de tela da interface do programa com diversos campos e botões, e uma listagem. Nenhum campo preenchido. Estão sendo mostrados na listagem o texto "Quantidade: 21843" e, em seguida, certas informações sobre diferentes escolas incluindo nome, município, quantidade medalhas de ouro, de prata e de bronze, e menções honrosas](assets/screenshot4.png)
Escolas com mais medalhas de ouro da Região Sudeste.

## Instalação

1. Tenha instalado Python 3.10.0 ou mais recente

2. Clone o repositório:
```
git clone https://github.com/GabrielVBruno/consulta-premiados-obmep.git
cd consulta-premiados-obmep
```

3. Instale as dependências (`pandas`, `tqdm` e `unidecode`):
```
pip install -r requirements.txt
```

## Uso

1. Digite o comando para inicializar o `main.py`:
```
python src/main.py
```

2. Escolha uma das opção para baixar as tabelas ou continue caso já tenha baixado.

![Captura de tela da linha de comando na qual está sendo rodado o programa. Dentre outros elementos, aparecem: "Verificando tabelas baixadas"; "Nenhuma tabela baixada"; "Escolha uma opção"; e 4 opções entre continuar, baixar tabelas de todas as medalhas, de todas as medalhas e das menções honrosas de uma UF e de todas as medalhas e todas as menções honrosas](assets/screenshot5.png)

3. Uma nova janela de interface aparecerá. 
   - Nela é possível filtrar premiações digitando o nome do premiado e/ou da escola a partir de um padrão regex, além de selecionar edições, prêmios, UFs, municípios, níveis e tipo de escola.
   - Após preencher os filtros, escolha, ao pressionar um dos os dois botões, entre buscar premiados ou escolas com tais critérios.

![Captura de tela da interface do programa com os campos "Nome do premiado (Padrão regex)" e "Nome da escola (Padrão regex)", as caixas de seleção "Selecione edições", "Selecione prêmios" e "Selecione UFs", o espaço para texto "Nomes dos municípios (separados por vírgula)", as caixas de seleção "Selecione níveis" e "Selecione tipos de escola", os botões "Buscar premiados" e "Buscar premiados por escola" e uma caixa de texto vazia](assets/screenshot6.png)