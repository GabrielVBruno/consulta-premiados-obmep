from collections import OrderedDict
from collections.abc import Generator
from dataclasses import dataclass
from enum import Enum
from itertools import cycle
from math import ceil
from os.path import isfile

from tabelas import *
from url import *


__ALL__ = [
    "EdicoesPorPremio",
    "EstadoTabelasBaixadas",
    "VerificacaoTabelasBaixadas",
    "obter_verificacao_tabelas_baixadas",
]


CORES_EDICOES = OrderedDict([
    (Edicao.OBMEP19, (223, 223, 225)),
    (Edicao.OBMEP18, (167, 97, 133)),
    (Edicao.OBMEP17, (168, 118, 68)),
    (Edicao.OBMEP16, (23, 122, 69)),
    (Edicao.ANO2019, (250, 83, 19)),
    (Edicao.ANO2018, (169, 70, 58)),
    (Edicao.ANO2017, (16, 177, 238)),
    (Edicao.ANO2016, (239, 222, 15)),
    (Edicao.ANO2015, (166, 206, 57)),
    (Edicao.ANO2014, (223, 223, 225)),
    (Edicao.ANO2013, (167, 97, 133)),
    (Edicao.ANO2012, (27, 47, 88)),
    (Edicao.ANO2011, (168, 118, 68)),
    (Edicao.ANO2010, (23, 122, 69)),
    (Edicao.ANO2009, (250, 83, 19)),
    (Edicao.ANO2008, (169, 70, 58)),
    (Edicao.ANO2007, (16, 177, 238)),
    (Edicao.ANO2006, (239, 222, 15)),
    (Edicao.ANO2005, (166, 206, 57)),
])

GRADIENTE_ASCII = " .-:*=+#%@"


@dataclass
class EdicoesPorPremio:
    """Indica edições baixadas por medalha e menções por UF por edição baixadas"""
    ouro: set[Edicao]
    prata: set[Edicao]
    bronze: set[Edicao]
    mencao: dict[Edicao, set[UF]]
    privada: bool
    
    
    def __str__(self) -> str:
        n_med_de_ouro_baixadas = 0
        n_med_de_prata_baixadas = 0
        n_med_de_bronze_baixadas = 0
        n_mencoes_honrosas_baixadas = 0
        
        texto_med_de_ouro_baixadas = ""
        texto_med_de_prata_baixadas = ""
        texto_med_de_bronze_baixadas = ""
        texto_mencoes_honrosas_baixadas = ""
        
        mencoes_por_uf = dict.fromkeys(UF, 0)
        
        for edicao, (r,g,b) in CORES_EDICOES.items():
            if self.privada and edicao not in EDICOES_COM_ESC_PRIV:
                continue
            
            if edicao in self.ouro:
                texto_med_de_ouro_baixadas += f"\033[38;2;{r};{g};{b}m@\033[m"
                n_med_de_ouro_baixadas += 1
            else:
                texto_med_de_ouro_baixadas += " "
            if edicao in self.prata:
                texto_med_de_prata_baixadas += f"\033[38;2;{r};{g};{b}m@\033[m"
                n_med_de_prata_baixadas += 1
            else:
                texto_med_de_prata_baixadas += " "
            if edicao in self.bronze:
                texto_med_de_bronze_baixadas += f"\033[38;2;{r};{g};{b}m@\033[m"
                n_med_de_bronze_baixadas += 1
            else:
                texto_med_de_bronze_baixadas += " "
                
            if edicao in self.mencao:
                char_n_ufs = GRADIENTE_ASCII[ceil(len(self.mencao[edicao]) * 8 / 27) + (len(self.mencao[edicao]) == 27)]
                
                texto_mencoes_honrosas_baixadas += f"\033[38;2;{r};{g};{b}m{char_n_ufs}\033[m"
                n_mencoes_honrosas_baixadas += len(self.mencao[edicao])
                
                for uf in self.mencao[edicao]: mencoes_por_uf[uf] += 1
            else:
                texto_mencoes_honrosas_baixadas += " "
                
        resultado = ""
        
        total_edicoes = 19 - self.privada * 12
        
        for nome_premio, n_premio, texto_premio in [
            ("Medalha de Ouro  ", n_med_de_ouro_baixadas, texto_med_de_ouro_baixadas),
            ("Medalha de Prata ", n_med_de_prata_baixadas, texto_med_de_prata_baixadas),
            ("Medalha de Bronze", n_med_de_bronze_baixadas, texto_med_de_bronze_baixadas),
        ]:
            resultado += f"{nome_premio}: [{texto_premio}] ({n_premio}/{total_edicoes} - {n_premio / total_edicoes:.2%})\n"
            
        resultado += f"Menções Honrosas : [{texto_mencoes_honrosas_baixadas}] ({n_mencoes_honrosas_baixadas}/{total_edicoes * 27} - {n_mencoes_honrosas_baixadas / (total_edicoes * 27):.2%} - {', '.join(uf.value for uf, n_mencoes_uf in mencoes_por_uf.items() if n_mencoes_uf == total_edicoes)})"
        
        return resultado
    
    
class EstadoTabelasBaixadas(Enum):
    """`Enum` para indicar o nível de quais tabelas foram baixadas"""
    NENHUMA_TABELA = "Nenhuma tabela baixada"
    MEDALHAS_INCOMPLETAS = "Medalhas incompletas"
    TODAS_MEDALHAS = "Todas medalhas baixadas"
    TODAS_MED_MENC_1_UF = "Todas medalhas baixadas e todas menções honrosas de pelo menos uma UF baixadas"
    TODAS_MED_MENC = "Todas medalhas e todas menções honrosas baixadas"
    
    def __str__(self) -> str: return self.value


@dataclass
class VerificacaoTabelasBaixadas:
    """Indica as edições baixadas por premio por nível e tipo (escola pública ou privada)"""
    premios_N1_publ: EdicoesPorPremio
    premios_N1_priv: EdicoesPorPremio
    premios_N2_publ: EdicoesPorPremio
    premios_N2_priv: EdicoesPorPremio
    premios_N3_publ: EdicoesPorPremio
    premios_N3_priv: EdicoesPorPremio
    
    @property
    def premios_baixados(self) -> Generator[EdicoesPorPremio]:
        """Gerador com os campos"""
        yield self.premios_N1_publ
        yield self.premios_N1_priv
        yield self.premios_N2_publ
        yield self.premios_N2_priv
        yield self.premios_N3_publ
        yield self.premios_N3_priv
    
    def __str__(self) -> str:
        resultado = ""
            
        for nivel, tipo, premios in zip((1, 1, 2, 2, 3, 3), cycle(("Públicas", "Privadas")), self.premios_baixados):
            resultado += "Nível {} - Escolas {}:\n    {}\n".format(nivel, tipo, str(premios).replace('\n', '\n    '))
            
        resultado += f"{self.obter_estado()}"
        
        return resultado
    
    
    def obter_estado(self) -> EstadoTabelasBaixadas:
        """Obtem estado das tabelas baixadas (`EstadoTabelasBaixadas`)"""
        nenhuma_tabela = True
        todas_medalhas = True
        
        for edicoes_por_premio in self.premios_baixados:
            edicoes_possiveis = EDICOES_COM_ESC_PRIV if edicoes_por_premio.privada else EDICOES
            
            if nenhuma_tabela and (edicoes_por_premio.ouro or edicoes_por_premio.prata or edicoes_por_premio.bronze):
                nenhuma_tabela = False
            
            if todas_medalhas and not (edicoes_por_premio.ouro.issuperset(edicoes_possiveis)
                    and edicoes_por_premio.prata.issuperset(edicoes_possiveis)
                    and edicoes_por_premio.bronze.issuperset(edicoes_possiveis)):
                todas_medalhas = False
        
        if nenhuma_tabela: return EstadoTabelasBaixadas.NENHUMA_TABELA
        if not todas_medalhas: return EstadoTabelasBaixadas.MEDALHAS_INCOMPLETAS
        
        ufs_completos = set(UF)
                
        for edicoes_por_premio in self.premios_baixados:
            edicoes_possiveis = EDICOES_COM_ESC_PRIV if edicoes_por_premio.privada else EDICOES
            
            if not edicoes_por_premio.mencao:
                return EstadoTabelasBaixadas.TODAS_MEDALHAS
            
            for edicao in edicoes_possiveis:
                ufs_completos &= edicoes_por_premio.mencao[edicao]
                if not ufs_completos:
                    return EstadoTabelasBaixadas.TODAS_MEDALHAS
                
        if len(ufs_completos) == len(UF): return EstadoTabelasBaixadas.TODAS_MED_MENC
        else: return EstadoTabelasBaixadas.TODAS_MED_MENC_1_UF


def obter_verificacao_tabelas_baixadas() -> VerificacaoTabelasBaixadas:
    edicoes_por_premio = []
    
    for nivel, privada in [(Nivel._1, False), (Nivel._1, True), (Nivel._2, False), (Nivel._2, True), (Nivel._3, False), (Nivel._3, True)]:
        ouro: set[Edicao] = set()
        prata: set[Edicao] = set()
        bronze: set[Edicao] = set()
        mencao: dict[Edicao, set[UF]] = {edicao: set() for edicao in Edicao}
        
        for edicao in Edicao:
            caminho_ouro = obter_caminho_tabela(edicao, Premio.OURO, None, nivel, privada=privada)
            if isfile(caminho_ouro): ouro.add(edicao)
            
            caminho_prata = obter_caminho_tabela(edicao, Premio.PRATA, None, nivel, privada=privada)
            if isfile(caminho_prata): prata.add(edicao)
            
            caminho_bronze = obter_caminho_tabela(edicao, Premio.BRONZE, None, nivel, privada=privada)
            if isfile(caminho_bronze): bronze.add(edicao)
            
            for uf in UF:
                caminho_mencao = obter_caminho_tabela(edicao, Premio.MENCAO, uf, nivel, privada=privada)
                if isfile(caminho_mencao): mencao[edicao].add(uf)
                
        edicoes_por_premio.append(EdicoesPorPremio(ouro, prata, bronze, mencao, privada))
        
    verificacao = VerificacaoTabelasBaixadas(*edicoes_por_premio)
    
    return verificacao