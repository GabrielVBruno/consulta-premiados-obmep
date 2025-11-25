import os

from verificacao import *
from ui import executar_ui, normalizar

tamanho_terminal = os.get_terminal_size().columns

titulo = "Consulta de premiados da Olimpíada Brasileira de Matemática das Escolas Públicas (OBMEP)"
if tamanho_terminal < len(titulo): titulo = "Consulta de premiados da OBMEP"
divisoria = "-" * tamanho_terminal

riscar = "\033[9m", "\033[m"
opcoes_de_instalação = """Escolha uma opção:
{}[ 0 ] - Continuar.{}
{}[ 1 ] - Baixar as tabelas de todas as medalhas. (~9 MB){}
{}[ 2 ] - Baixar as tabelas de todas as medalhas e das menções honrosas de uma UF. (~9-24 MB){}
{}[ 3 ] - Baixar as tabelas de todas as medalhas e todas as menções honrosas. (~70 MB){}"""

def verificar_tabelas_baixadas():
    print("Verificando tabelas baixadas...")
    verificacao = obter_verificacao_tabelas_baixadas()
    estado = verificacao.obter_estado()
    print(estado)
    if estado is not EstadoTabelasBaixadas.NENHUMA_TABELA and estado is not EstadoTabelasBaixadas.TODAS_MED_MENC:
        print(verificacao)
    if estado is not EstadoTabelasBaixadas.TODAS_MED_MENC: escolher_opcoes_de_instalação(estado)
    
def escolher_opcoes_de_instalação(estado: EstadoTabelasBaixadas):
    op_0_possivel = estado is not EstadoTabelasBaixadas.NENHUMA_TABELA and estado is not EstadoTabelasBaixadas.MEDALHAS_INCOMPLETAS
    op_1_possivel = not op_0_possivel
    op_2_possivel = estado is not EstadoTabelasBaixadas.TODAS_MED_MENC
    op_3_possivel = op_2_possivel
    
    print(opcoes_de_instalação.format(
        *(("", "") if op_0_possivel else riscar), 
        *(("", "") if op_1_possivel else riscar), 
        *(("", "") if op_2_possivel else riscar),
        *(("", "") if op_3_possivel else riscar),
    ))
    
    while True:
        escolha = input("")
        
        match escolha:
            case "0" if op_0_possivel:
                break
            case "1" if op_1_possivel:
                buscar_e_salvar_tabelas(premios=MEDALHAS, ufs={None})
                break
            case "2" if op_2_possivel:
                uf = input("Digite o UF: ")
                while normalizar(uf) not in (normalizar(uf.value) for uf in UF):
                    print("UF inválida. Tente novamente.")
                    uf = input("Digite o UF: ")
                buscar_e_salvar_tabelas(premios=MEDALHAS, ufs={None})
                buscar_e_salvar_tabelas(premios={Premio.MENCAO}, ufs={UF(uf)})
                break
            case "3" if op_3_possivel:
                buscar_e_salvar_tabelas(premios=MEDALHAS, ufs={None})
                buscar_e_salvar_tabelas(premios={Premio.MENCAO}, ufs=set(UF))
                break
            case _:
                print("Opção impossível ou inválida. Tente novamente.")

def init():
    print(divisoria)
    print(f"{titulo:^{tamanho_terminal}}")
    print(divisoria)
    verificar_tabelas_baixadas()
    
if __name__ == "__main__":
    try:
        init()
        print("Inicializando GUI...")
        executar_ui()
    except KeyboardInterrupt:
        print("Fechando programa...")