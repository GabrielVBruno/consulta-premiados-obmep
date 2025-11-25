from io import StringIO
import os.path
import warnings
import urllib.request

import pandas as pd
from tqdm import tqdm

from url import *


__all__ = [
    "caminho_tabela_base",
    "buscar_tabelas",
    "sanitizar_tabela",
    "obter_caminho_tabela",
    "salvar_tabela",
    "buscar_e_salvar_tabelas",
]


caminho_tabela_base = "./tabelas/{}-{}-{}-{}-{}.csv" # Edição, Prêmio, UF, Nível, Privada?


def buscar_tabelas(
    edicao: Edicao, 
    premio: Premio, 
    uf: UF | None = None, 
    nivel: Nivel | None = None, 
    /,
    *,
    privada: bool = False
) -> list[pd.DataFrame]:
    url = obter_url(edicao, premio, uf, nivel, privada=privada)
    
    solicitacao = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(solicitacao) as resposta:
            texto = resposta.read().decode(errors="ignore")
        tabelas = pd.read_html(StringIO(texto))
    except UnicodeDecodeError as e:
        print(f"Erro enquanto processava busca ({edicao.value}, {premio.value}, {uf.value if uf is not None else uf}, {nivel.value if nivel is not None else nivel}, {privada}): {e}")
        tabelas = []
    
    return tabelas


def sanitizar_tabela(tabela: pd.DataFrame) -> pd.DataFrame:
    if tabela.iloc[0, 0] == "Não existem registros de alunos neste Nível.":
        warnings.warn(Warning(f"tabela {tabela} inválida."))
        tabela.drop(0, inplace=True)
    
    tabela.columns = tabela.columns.droplevel(0) # Remove primeira coluna

    if "Unnamed" in tabela.columns[0]: # Tabela de posições, presente em algumas tabela, não possui nome
        tabela = tabela.rename(columns={tabela.columns[0]: 'Posição'})
        
        tabela['Posição'] = tabela['Posição'].astype(pd.UInt32Dtype()) # Converter para inteiro positivo ao invés de string

        tabela['Posição'] = tabela['Posição'].ffill() # Quando não há valor, significa empate, então mesma posição
    
    tabela = tabela.iloc[:, :next((i for i, nome_col in enumerate(tabela.columns, 0) if nome_col.startswith("Unnamed")), len(tabela))] # Remover da primeira coluna sem título em diante
    
    tabela.dropna(inplace=True)
    
    return tabela


def obter_caminho_tabela(
    edicao: Edicao,
    premio: Premio,
    uf: UF | None,
    nivel: Nivel,
    *,
    privada: bool
):
    return caminho_tabela_base.format(
        edicao.value,
        premio.value,
        uf.value if uf is not None else "",
        nivel.value,
        "privada" if privada else ""
    )
    

def salvar_tabela(
    tabela: pd.DataFrame,
    edicao: Edicao,
    premio: Premio,
    uf: UF | None,
    nivel: Nivel,
    *,
    privada: bool,
    regravar: bool = False,
    existe_pasta_tabelas: bool = False
):
    caminho_tabela = obter_caminho_tabela(edicao, premio, uf, nivel, privada=privada)
    
    if not existe_pasta_tabelas and not os.path.exists(caminho_tabela[:caminho_tabela.rindex("/")]):
        os.mkdir(caminho_tabela[:caminho_tabela.rindex("/")])
    
    if not regravar and os.path.exists(caminho_tabela):
        return
    
    tabela.to_csv(caminho_tabela, index=False)


def buscar_e_salvar_tabelas(
    edicoes: set[Edicao] = set(Edicao),
    premios: set[Premio] = set(Premio),
    ufs: set[UF | None] = set(UF) | {None}, # Cada UF ou nacional
    niveis: set[Nivel] = set(Nivel),
    *,
    privada: bool | None = None, # Privadas ou não
    regravar: bool = False,
):
    if privada == None:
        buscar_e_salvar_tabelas(edicoes, premios, ufs, niveis, privada=True, regravar=regravar)
        buscar_e_salvar_tabelas(edicoes, premios, ufs, niveis, privada=False, regravar=regravar)
        
        return
    
    if privada == True:
        edicoes = edicoes & EDICOES_COM_ESC_PRIV
        
    existe_pasta_tabelas = False
        
    for edicao in tqdm(edicoes):
        for premio in premios:
            if premio in MEDALHAS:
                for uf in ufs:
                    if not regravar and all(os.path.exists(
                        obter_caminho_tabela(edicao, premio, uf, nivel, privada=privada)
                    ) for nivel in niveis): continue
                    
                    tabelas = buscar_tabelas(edicao, premio, uf, privada=privada)
                    
                    for i, tabela in enumerate(tabelas, 1):
                        if Nivel(str(i)) not in niveis:
                            continue
                        
                        tabela = sanitizar_tabela(tabela)
                        
                        salvar_tabela(tabela, edicao, premio, uf, Nivel(str(i)), privada=privada, regravar=regravar, existe_pasta_tabelas=existe_pasta_tabelas)
                        
                        if not existe_pasta_tabelas: existe_pasta_tabelas = True
            else:
                for uf in ufs:
                    if uf is None:
                        continue
                    
                    if not regravar and all(os.path.exists(
                        obter_caminho_tabela(edicao, premio, uf, nivel, privada=privada)
                    ) for nivel in niveis): continue
                    
                    if not privada and edicao is Edicao.ANO2018 and premio is Premio.MENCAO: # Por que isso aconteceu?
                        tabelas = []
                        
                        for nivel in niveis:
                            tabelas_nivel = buscar_tabelas(edicao, premio, uf, nivel, privada=privada)
                            
                            tabelas.extend(tabelas_nivel)
                    else:
                        tabelas = buscar_tabelas(edicao, premio, uf, privada=privada)
                    
                    for i, tabela in enumerate(tabelas, 1):
                        if Nivel(str(i)) not in niveis:
                            continue
                        
                        tabela = sanitizar_tabela(tabela)
                        
                        if tabela is None:
                            continue
                        
                        salvar_tabela(tabela, edicao, premio, uf, Nivel(str(i)), privada=privada, regravar=regravar)