import typing
from enum import Enum
from typing import Literal, TypeAlias
from collections import OrderedDict


__all__ = [
    "Edicao",
    "EDICOES",
    "EDICOES_COM_ESC_PRIV",
    "EdicaoComEscPriv",
    "NOMES_EDICOES",
    "Premio",
    "PREMIOS",
    "MEDALHAS",
    "NOMES_PREMIOS",
    "UF",
    "UFS_POR_REGIAO",
    "UFS_POR_REGIAO_PLANO",
    "Nivel",
    "NIVEIS",
    "NOMES_NIVEIS",
    "TipoEscola",
    "TIPOS_ESCOLA",
    "NOMES_TIPOS_ESCOLA",
    "obter_url",
]


url_base = "http://premiacao.obmep.org.br/{}/verRelatorioPremiados{}.do.htm"


class Edicao(Enum):
    OBMEP19 = "19obmep"
    ANO2024 = "19obmep"
    OBMEP18 = "18obmep"
    ANO2023 = "18obmep"
    OBMEP17 = "17obmep"
    ANO2022 = "17obmep"
    OBMEP16 = "16aobmep"
    ANO2021 = "16aobmep"
    OBMEP15 = "2019"
    ANO2019 = "2019"
    OBMEP14 = "2018"
    ANO2018 = "2018"
    OBMEP13 = "2017"
    ANO2017 = "2017"
    OBMEP12 = "2016"
    ANO2016 = "2016"
    OBMEP11 = "2015"
    ANO2015 = "2015"
    OBMEP10 = "2014"
    ANO2014 = "2014"
    OBMEP9 = "2013"
    ANO2013 = "2013"
    OBMEP8 = "2012"
    ANO2012 = "2012"
    OBMEP7 = "2011"
    ANO2011 = "2011"
    OBMEP6 = "2010"
    ANO2010 = "2010"
    OBMEP5 = "2009"
    ANO2009 = "2009"
    OBMEP4 = "2008"
    ANO2008 = "2008"
    OBMEP3 = "2007"
    ANO2007 = "2007"
    OBMEP2 = "2006"
    ANO2006 = "2006"
    OBMEP1 = "2005"
    ANO2005 = "2005"

EDICOES = list(Edicao)

EDICOES_COM_ESC_PRIV = set(Edicao) - {Edicao.ANO2016, Edicao.ANO2015, Edicao.ANO2014, Edicao.ANO2013, Edicao.ANO2012, Edicao.ANO2011, Edicao.ANO2010, Edicao.ANO2009, Edicao.ANO2008, Edicao.ANO2007, Edicao.ANO2006, Edicao.ANO2005}

EdicaoComEscPriv: TypeAlias = Literal[Edicao.ANO2017, Edicao.ANO2018, Edicao.ANO2019, Edicao.OBMEP16, Edicao.OBMEP17, Edicao.OBMEP18, Edicao.OBMEP19]

NOMES_EDICOES: OrderedDict[Edicao, str] = OrderedDict([
    (Edicao.OBMEP19, "19ª OBMEP"),
    (Edicao.OBMEP18, "18ª OBMEP"),
    (Edicao.OBMEP17, "17ª OBMEP"),
    (Edicao.OBMEP16, "16ª OBMEP"),
    (Edicao.ANO2019, "OBMEP 2019"),
    (Edicao.ANO2018, "OBMEP 2018"),
    (Edicao.ANO2017, "OBMEP 2017"),
    (Edicao.ANO2016, "OBMEP 2016"),
    (Edicao.ANO2015, "OBMEP 2015"),
    (Edicao.ANO2014, "OBMEP 2014"),
    (Edicao.ANO2013, "OBMEP 2013"),
    (Edicao.ANO2012, "OBMEP 2012"),
    (Edicao.ANO2011, "OBMEP 2011"),
    (Edicao.ANO2010, "OBMEP 2010"),
    (Edicao.ANO2009, "OBMEP 2009"),
    (Edicao.ANO2008, "OBMEP 2008"),
    (Edicao.ANO2007, "OBMEP 2007"),
    (Edicao.ANO2006, "OBMEP 2006"),
    (Edicao.ANO2005, "OBMEP 2005"),
])

class Premio(Enum):
    OURO = "Ouro"
    PRATA = "Prata"
    BRONZE = "Bronze"
    MENCAO = "Mencao"
    GERAL = "Geral"
    
PREMIOS = list(Premio)
    
MEDALHAS = {Premio.OURO, Premio.PRATA, Premio.BRONZE}

NOMES_PREMIOS: OrderedDict[Premio, str] = OrderedDict([
    (Premio.OURO, "Medalha de Ouro"),
    (Premio.PRATA, "Medalha de Prata"),
    (Premio.BRONZE, "Medalha de Bronze"),
    (Premio.MENCAO, "Menção Honrosa"),
    (Premio.GERAL, "Geral"),
])
    

class UF(Enum):
    AC = "AC"
    AL = "AL"
    AM = "AM"
    AP = "AP"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MG = "MG"
    MS = "MS"
    MT = "MT"
    PA = "PA"
    PB = "PB"
    PE = "PE"
    PI = "PI"
    PR = "PR"
    RJ = "RJ"
    RN = "RN"
    RO = "RO"
    RR = "RR"
    RS = "RS"
    SC = "SC"
    SE = "SE"
    SP = "SP"
    TO = "TO"
    
UFS_POR_REGIAO = OrderedDict([
    ("Região Centro-Oeste", (UF.DF, UF.GO, UF.MS, UF.MT)),
    ("Região Nordeste", (UF.AL, UF.BA, UF.CE, UF.MA, UF.PB, UF.PE, UF.PI, UF.RN, UF.SE)),
    ("Região Norte", (UF.AC, UF.AM, UF.AP, UF.PA, UF.RO, UF.RR, UF.TO)),
    ("Região Sudeste", (UF.ES, UF.MG, UF.RJ, UF.SP)),
    ("Região Sul", (UF.PR, UF.RS, UF.SC))
])

UFS_POR_REGIAO_PLANO = [uf for nome_regiao, ufs in UFS_POR_REGIAO.items() for uf in ufs]
    
    
class Nivel(Enum):
    _1 = "1"
    _2 = "2"
    _3 = "3"
    
NIVEIS = list(Nivel)

NOMES_NIVEIS: OrderedDict[Nivel, str] = OrderedDict([
    (Nivel._1, "Nível 1"),
    (Nivel._2, "Nível 2"),
    (Nivel._3, "Nível 3")
])


TipoEscola: TypeAlias = Literal["M", "E", "F", "P"]

TIPOS_ESCOLA: tuple[TipoEscola] = typing.get_args(TipoEscola)

NOMES_TIPOS_ESCOLA = OrderedDict([
    ("M", "Municipal"),
    ("E", "Estadual"),
    ("F", "Federal"),
    ("P", "Particular"),
])


def obter_url(
    edicao: Edicao, 
    premio: Premio, 
    uf: UF | None = None, 
    nivel: Nivel | None = None, 
    /,
    *,
    privada: bool = False
) -> str:
    """
        Se `premio` é `Premio.OURO`, `Premio.PRATA` ou `Premio.BRONZE`:
        
        `nivel` é ignorado.
    """
    
    if premio in MEDALHAS:
        nivel = None
        
    return url_base.format(
        edicao.value,
        f"{premio.value}{'-' + uf.value if uf is not None else ''}{'.' + nivel.value if nivel is not None else ''}{'.privada' if privada else ''}"
    )