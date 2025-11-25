import csv
import glob
import itertools
import re
from collections import OrderedDict
from collections.abc import Container, Generator, Iterable, Collection
from dataclasses import dataclass
from typing import Any

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font

from tqdm import tqdm
from unidecode import unidecode

from tabelas import *
from url import *


def normalizar(s: str) -> str:
    return unidecode(s).casefold()


@dataclass
class Premiado:
    edicao: Edicao
    premio: Premio
    uf: UF | None
    nivel: Nivel | None
    privada: bool
    linha: dict[str, str]
    
    
    def __str__(self) -> str:
        return f"{self.linha['Nome']}   |   {self.linha['Escola']} ({self.linha['Tipo']})   |   {self.linha['Município']} ({self.linha['UF']})   |   {NOMES_PREMIOS[self.premio]}{'   |   Nível ' + self.nivel.value if self.nivel else ''}   |   {NOMES_EDICOES[self.edicao]}"


def tabelas() -> Generator[tuple[str, tuple[Edicao, Premio, UF | None, Nivel | None, bool]], Any, None]:
    for caminho_tabela in glob.iglob("./tabelas/*.csv"):
        caminho_tabela = caminho_tabela.replace("\\", "/")
        edicao, premio, uf, nivel, privada = caminho_tabela[caminho_tabela.rindex("/")+1:].removesuffix(".csv").split("-")
        edicao, premio, uf, nivel, privada = Edicao(edicao), Premio(premio), UF(uf) if uf else None, Nivel(nivel) if nivel else None, privada == "privada"
        
        yield caminho_tabela, (edicao, premio, uf, nivel, privada)


def buscar_linhas(*coluna_e_padrao: tuple[str, str], edicoes_a_buscar: Container[Edicao] = (), premios_a_buscar: Container[Premio] = (), ufs_a_buscar: Container[UF] = (), municipios_a_buscar: Collection[str] = (), niveis_a_buscar: Container[Nivel] = (), tipos_a_buscar: Container[TipoEscola] = ()) -> list[Premiado]:
    lista_tabelas = list(tabelas())
    
    linhas: list[Premiado] = []
    
    coluna_e_padrao_normalizado = [(coluna, normalizar(padrao)) for coluna, padrao in coluna_e_padrao]
    municipios_a_buscar_normalizados = list(map(normalizar, municipios_a_buscar))
    
    for i, (caminho_tabela, (edicao_tabela, premio_tabela, uf_tabela, nivel_tabela, privada_tabela)) in tqdm(enumerate(lista_tabelas), total=len(lista_tabelas)):
        root.title(f"{round((i+1) / len(lista_tabelas) * 100, 1)}%")
        
        if premio_tabela == Premio.GERAL: continue
        
        if (
            (edicoes_a_buscar and edicao_tabela not in edicoes_a_buscar)
            or (premios_a_buscar and premio_tabela not in premios_a_buscar)
            or (niveis_a_buscar and nivel_tabela not in niveis_a_buscar)
            or ("P" not in tipos_a_buscar and privada_tabela)
        ): continue
        
        with open(caminho_tabela, "r", encoding="UTF-8", newline="") as arquivo_tabela:
            tabela = csv.reader(arquivo_tabela)
            
            colunas = next(tabela)
            
            for i, linha in enumerate(tabela):
                dic_linha = dict(zip(colunas, linha))
                
                if (
                    all(re.search(padrao, normalizar(dic_linha[coluna])) 
                        for coluna, padrao in coluna_e_padrao_normalizado)
                    and (not ufs_a_buscar or UF(dic_linha["UF"]) in ufs_a_buscar)
                    and (not municipios_a_buscar or normalizar(dic_linha["Município"]) in municipios_a_buscar_normalizados)
                    and (not tipos_a_buscar or dic_linha["Tipo"] in tipos_a_buscar)
                ):
                    linhas.append(Premiado(edicao_tabela, premio_tabela, uf_tabela, nivel_tabela, privada_tabela, dic_linha))
                
    linhas.sort(key=lambda l: (EDICOES.index(l.edicao), PREMIOS.index(l.premio), NIVEIS.index(l.nivel or Nivel._3)))
                
    return linhas


def mostrar_premiados(premiados: list[Premiado]):
    global saida
    
    saida.configure(state="normal")
    
    saida.delete("1.0", "end")
    
    if len(premiados) > 10:
        saida.insert("end", f"Quantidade: {len(premiados)}\n")
    
    if len(premiados) > 100:
        for resultado in premiados[:100]:
            saida.insert("end", str(resultado) + "\n")
        saida.insert("end", "...\n")
    else:
        for resultado in premiados:
            saida.insert("end", str(resultado) + "\n")
            
    saida.configure(state="disabled")
    
    
def processar_busca_premiados(*args):
    global entrada_buscar_nome, entrada_buscar_escola
    global entrada_edicoes_vars, entrada_premios_vars, entrada_ufs_vars, entrada_municipios, entrada_niveis_vars, entrada_tipos_vars
    
    padrao_nome: str = entrada_buscar_nome.get()
    padrao_escola: str = entrada_buscar_escola.get()
    
    edicoes_a_buscar = list(itertools.compress(Edicao, map(tk.BooleanVar.get, entrada_edicoes_vars)))
    premios_a_buscar = list(itertools.compress(itertools.islice(Premio, 0, 4), map(tk.BooleanVar.get, entrada_premios_vars)))
    ufs_a_buscar = list(itertools.compress(UFS_POR_REGIAO_PLANO, map(tk.BooleanVar.get, entrada_ufs_vars)))
    municipios_a_buscar = entrada_municipios.get().split(",") if normalizar(entrada_municipios.get()) else ()
    niveis_a_buscar = list(itertools.compress(Nivel, map(tk.BooleanVar.get, entrada_niveis_vars)))
    tipos_a_buscar: list[TipoEscola] = list(itertools.compress(TIPOS_ESCOLA, map(tk.BooleanVar.get, entrada_tipos_vars))) # type: ignore
    
    resultados = buscar_linhas(
        ("Nome", padrao_nome), 
        ("Escola", padrao_escola), 
        edicoes_a_buscar=edicoes_a_buscar,
        premios_a_buscar=premios_a_buscar,
        ufs_a_buscar=ufs_a_buscar,
        municipios_a_buscar=municipios_a_buscar,
        niveis_a_buscar=niveis_a_buscar,
        tipos_a_buscar=tipos_a_buscar,
    )
    
    mostrar_premiados(resultados)

    
@dataclass
class PremiosPorEscola:
    escola: str
    tipo: TipoEscola
    uf: UF
    municipio: str
    medalhas_de_ouro: int = 0
    medalhas_de_prata: int = 0
    medalhas_de_bronze: int = 0
    mencoes_honrosas: int = 0
    
    
    def __lt__(self, other: Any) -> bool: return (self.medalhas_de_ouro, self.medalhas_de_prata, self.medalhas_de_bronze, self.mencoes_honrosas) < (other.medalhas_de_ouro, other.medalhas_de_prata, other.medalhas_de_bronze, other.mencoes_honrosas) if isinstance(other, PremiosPorEscola) else NotImplemented
    def __le__(self, other: Any) -> bool: return (self.medalhas_de_ouro, self.medalhas_de_prata, self.medalhas_de_bronze, self.mencoes_honrosas) <= (other.medalhas_de_ouro, other.medalhas_de_prata, other.medalhas_de_bronze, other.mencoes_honrosas) if isinstance(other, PremiosPorEscola) else NotImplemented
    def __gt__(self, other: Any) -> bool: return (self.medalhas_de_ouro, self.medalhas_de_prata, self.medalhas_de_bronze, self.mencoes_honrosas) > (other.medalhas_de_ouro, other.medalhas_de_prata, other.medalhas_de_bronze, other.mencoes_honrosas) if isinstance(other, PremiosPorEscola) else NotImplemented
    def __ge__(self, other: Any) -> bool: return (self.medalhas_de_ouro, self.medalhas_de_prata, self.medalhas_de_bronze, self.mencoes_honrosas) >= (other.medalhas_de_ouro, other.medalhas_de_prata, other.medalhas_de_bronze, other.mencoes_honrosas) if isinstance(other, PremiosPorEscola) else NotImplemented
    
    
    def __str__(self) -> str:
        return f"Ouro: {self.medalhas_de_ouro}   |   Prata: {self.medalhas_de_prata}   |   Bronze: {self.medalhas_de_bronze}   |   Menção Honrosa: {self.mencoes_honrosas}"
    

def buscar_premios_escola(*, edicoes_a_buscar: Container[Edicao] = (), premios_a_buscar: Container[Premio] = (), ufs_a_buscar: Container[UF] = (), municipios_a_buscar: Collection[str] = (), niveis_a_buscar: Container[Nivel] = (), tipos_a_buscar: Container[TipoEscola] = ()) -> dict[str, PremiosPorEscola]:
    lista_tabelas = list(tabelas())
    
    premios: dict[str, PremiosPorEscola] = dict()
    
    municipios_a_buscar_normalizados = list(map(normalizar, municipios_a_buscar))
    
    for i, (caminho_tabela, (edicao_tabela, premio_tabela, uf_tabela, nivel_tabela, privada_tabela)) in tqdm(enumerate(lista_tabelas), total=len(lista_tabelas)):
        root.title(f"{round((i+1) / len(lista_tabelas) * 100, 1)}%")
        
        if premio_tabela == Premio.GERAL: continue
        
        if (
            (edicoes_a_buscar and edicao_tabela not in edicoes_a_buscar)
            or (premios_a_buscar and premio_tabela not in premios_a_buscar)
            or (niveis_a_buscar and nivel_tabela not in niveis_a_buscar)
        ): continue
        
        with open(caminho_tabela, "r", encoding="UTF-8", newline="") as arquivo_tabela:
            tabela = csv.reader(arquivo_tabela)
            
            colunas = next(tabela)
        
            for i, linha in enumerate(tabela):
                dic_linha = dict(zip(colunas, linha))
                
                if (
                    (ufs_a_buscar and UF(dic_linha["UF"]) not in ufs_a_buscar)
                    or (municipios_a_buscar and normalizar(dic_linha["Município"]) not in municipios_a_buscar_normalizados)
                    or (tipos_a_buscar and dic_linha["Tipo"] not in tipos_a_buscar)
                ):
                    continue
                
                premios_escola = premios.setdefault(dic_linha["Escola"], PremiosPorEscola(dic_linha["Escola"], dic_linha["Tipo"], UF(dic_linha["UF"]), dic_linha["Município"])) # type: ignore
                
                if premio_tabela == Premio.OURO:
                    premios_escola.medalhas_de_ouro += 1
                if premio_tabela == Premio.PRATA:
                    premios_escola.medalhas_de_prata += 1
                if premio_tabela == Premio.BRONZE:
                    premios_escola.medalhas_de_bronze += 1
                if premio_tabela == Premio.MENCAO:
                    premios_escola.mencoes_honrosas += 1

    return premios


def mostrar_premios_escola(premios: OrderedDict[str, PremiosPorEscola], *, premios_a_mostrar: Container[Premio]):
    global saida
    
    filtro_por_premio = [premio in premios_a_mostrar for premio in PREMIOS[:-1]]
    
    saida.configure(state="normal")
    
    saida.delete("1.0", "end")
    
    saida.insert("end", f"Quantidade: {len(premios)}\n")
    
    for nome_escola, premios_por_escola in itertools.islice(premios.items(), 40):
        premios_por_escola_filtrado = "   |   ".join(itertools.compress(str(premios_por_escola).split("   |   "), filtro_por_premio))
        
        saida.insert("end", f"{nome_escola} ({premios_por_escola.tipo})   |   {premios_por_escola.municipio} ({premios_por_escola.uf.value}):   {premios_por_escola_filtrado}\n")
    if len(premios) > 40:
        saida.insert("end", "...")
            
    saida.configure(state="disabled")


def processar_busca_premios_escola():
    global entrada_edicoes_vars, entrada_premios_vars, entrada_ufs_vars, entrada_municipios, entrada_niveis_vars, entrada_tipos_vars
    
    edicoes_a_buscar = list(itertools.compress(Edicao, map(tk.BooleanVar.get, entrada_edicoes_vars)))
    premios_a_buscar = list(itertools.compress(itertools.islice(Premio, 0, 4), map(tk.BooleanVar.get, entrada_premios_vars)))
    ufs_a_buscar = list(itertools.compress(UFS_POR_REGIAO_PLANO, map(tk.BooleanVar.get, entrada_ufs_vars)))
    municipios_a_buscar = entrada_municipios.get().split(",") if normalizar(entrada_municipios.get()) else ()
    niveis_a_buscar = list(itertools.compress(Nivel, map(tk.BooleanVar.get, entrada_niveis_vars)))
    tipos_a_buscar: list[TipoEscola] = list(itertools.compress(TIPOS_ESCOLA, map(tk.BooleanVar.get, entrada_tipos_vars))) # type: ignore
    
    premios = list(buscar_premios_escola(
        edicoes_a_buscar=edicoes_a_buscar,
        ufs_a_buscar=ufs_a_buscar,
        municipios_a_buscar=municipios_a_buscar,
        niveis_a_buscar=niveis_a_buscar,
        tipos_a_buscar=tipos_a_buscar,
    ).items())
    
    premios.sort(key=lambda par_escola: par_escola[1], reverse=True)
    premios = OrderedDict(premios)
    
    mostrar_premios_escola(premios, premios_a_mostrar=premios_a_buscar)


def definir_multiplas_vars(vars: Iterable[tk.Variable], value: Any):
    for var in vars:
        var.set(value)


def criar_menu_de_seleção(master: tk.Misc, rotulo_botao: str, rotulo_sel_todos: str, rotulos_opcoes: Collection[str] | OrderedDict[str, Collection[str]]) -> tuple[tk.Menubutton, tk.Menu, list[tk.BooleanVar]]:
    global fonte
    
    botao = tk.Menubutton(master, font=fonte, text=rotulo_botao)
    menu = tk.Menu(botao, font=fonte, tearoff=0)
    botao.config(menu=menu)
    
    vars_opcoes = [tk.BooleanVar(value=True) for _ in range(sum(map(len, rotulos_opcoes.values())) if isinstance(rotulos_opcoes, OrderedDict) else len(rotulos_opcoes))]
    todas_opcoes_selecionadas = tk.BooleanVar(value=True)
    
    menu.add_checkbutton(
        command=lambda: definir_multiplas_vars(vars_opcoes, todas_opcoes_selecionadas.get()),
        font=fonte,
        label=rotulo_sel_todos, 
        variable=todas_opcoes_selecionadas)
    
    if not isinstance(rotulos_opcoes, OrderedDict):
        for rotulo_opcao, var_opcao in zip(rotulos_opcoes, vars_opcoes):
            menu.add_checkbutton(
                command=lambda: todas_opcoes_selecionadas.set(all(map(tk.BooleanVar.get, vars_opcoes))),
                font=fonte,
                label=rotulo_opcao, 
                variable=var_opcao, 
            )
    else:
        i = 0
        
        for rotulo_subsecao, subsecao in rotulos_opcoes.items():
            submenu = tk.Menu(menu, tearoff=0)
            menu.add_cascade(label=rotulo_subsecao, menu=submenu)
            
            for rotulo_opcao in subsecao:
                submenu.add_checkbutton(
                    command=lambda: todas_opcoes_selecionadas.set(all(map(tk.BooleanVar.get, vars_opcoes))),
                    font=fonte,
                    label=rotulo_opcao, 
                    variable=vars_opcoes[i], 
                )
                
                i += 1
        
    return botao, menu, vars_opcoes


PADDING = 5


def executar_ui():
    global root, fonte, saida
    global entrada_buscar_nome, entrada_buscar_escola
    global entrada_edicoes_vars, entrada_premios_vars, entrada_ufs_vars, entrada_municipios, entrada_niveis_vars, entrada_tipos_vars
    
    
    root = tk.Tk(screenName="Premiados da OBMEP")
    root.geometry("1280x720")
    root.resizable(width=False, height=False)

    fonte = Font(root, family="Helvetica", size=13)
    

    linha_buscar_nome = ttk.Frame(root)

    ttk.Label(linha_buscar_nome, font=fonte, text="Nome do premiado (Padrão regex):").pack(side="left")

    entrada_buscar_nome = ttk.Entry(linha_buscar_nome, font=fonte)
    entrada_buscar_nome.pack(side="left", fill="x", expand=True, padx=(0, PADDING))

    linha_buscar_nome.pack(fill="x", expand=True)

    linha_buscar_escola = ttk.Frame(root)

    ttk.Label(linha_buscar_escola, font=fonte, text="Nome da escola (Padrão regex):").pack(side="left")

    entrada_buscar_escola = ttk.Entry(linha_buscar_escola, font=fonte)
    entrada_buscar_escola.pack(side="left", fill="x", expand=True, padx=(0, PADDING))

    linha_buscar_escola.pack(fill="x", expand=True)


    linha_filtros = ttk.Frame(root)

        
    entrada_edicoes_botao, entrada_edicoes_menu, entrada_edicoes_vars = criar_menu_de_seleção(linha_filtros, "Selecione edições", "Todas edições", NOMES_EDICOES.values())

    entrada_premios_botao, entrada_premios_menu, entrada_premios_vars = criar_menu_de_seleção(linha_filtros, "Selecione prêmios", "Todos prêmios", list(NOMES_PREMIOS.values())[:-1])

    entrada_ufs_botao, entrada_ufs_menu, entrada_ufs_vars = criar_menu_de_seleção(linha_filtros, "Selecione UFs", "Todas UFs", OrderedDict([(nome_regiao, [uf.value for uf in ufs]) for nome_regiao, ufs in UFS_POR_REGIAO.items()]))

    entrada_edicoes_botao.pack(side="left")
    entrada_premios_botao.pack(side="left")
    entrada_ufs_botao.pack(side="left")
        

    ttk.Label(linha_filtros, font=fonte, text="Nomes dos municipíos (separados por vírgula):").pack(side="left")

    entrada_municipios = ttk.Entry(linha_filtros, font=fonte)
    entrada_municipios.pack(side="left", fill="x", expand=True, padx=(0, PADDING))


    entrada_niveis_botao, entrada_niveis_menu, entrada_niveis_vars = criar_menu_de_seleção(linha_filtros, "Selecione níveis", "Todos níveis", NOMES_NIVEIS.values())

    entrada_tipos_botao, entrada_tipos_menu, entrada_tipos_vars = criar_menu_de_seleção(linha_filtros, "Selecione tipos de escola", "Todos tipos", NOMES_TIPOS_ESCOLA.values())
        
    entrada_niveis_botao.pack(side="left")
    entrada_tipos_botao.pack(side="left")


    linha_filtros.pack(fill="x", expand=True)


    linha_botoes = ttk.Frame(root)

    botao_quant_por_escola = tk.Button(linha_botoes, command=processar_busca_premiados, font=fonte, text="Buscar premiados")
    botao_quant_por_escola.pack(side="left", expand=True)
    botao_quant_por_escola = tk.Button(linha_botoes, command=processar_busca_premios_escola, font=fonte, text="Buscar premios por escola")
    botao_quant_por_escola.pack(side="left", expand=True)

    linha_botoes.pack(fill="x", expand=True)


    root.grid_rowconfigure(3, weight=1)

    saida = ScrolledText(root, font=fonte, height=100, state="disabled")
    saida.pack(fill="both", expand=True)
    
    root.mainloop()