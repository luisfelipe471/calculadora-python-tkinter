import tkinter as tk
from tkinter import messagebox as msg
import math

historico_calculos = []
opcao_selecionada = None
botoes_operacoes = {}

operacoes = [
    ("+ Somar", 1, "+"),
    ("− Subtrair", 2, "-"),
    ("÷ Dividir", 3, "÷"),
    ("x Multiplicar", 4, "x"),
    ("^ Potência", 5, "^"),
    ("% Resto", 6, "%")
]


# =========================
# CONFIGURAÇÃO DAS CORES
# =========================

FUNDO = "#0F172A"
CARTAO = "#1E293B"
CAMPO = "#334155"
AZUL = "#2563EB"
AZUL_CLARO = "#3B82F6"
TEXTO = "#F8FAFC"
SECUNDARIO = "#94A3B8"
VERMELHO = "#EF4444"

# =========================
# FUNÇÕES
# =========================


def formatar_numero(numero):
    if not math.isfinite(numero):
        raise ValueError("O resultado é muito grande.")

    if numero == 0:
        return "0"

    return f"{numero:.10g}"


def formatar_resultado(numero):
    texto = formatar_numero(numero)

    if "e" not in texto.lower():
        return texto

    base, expoente = texto.lower().split("e")
    expoente = int(expoente)

    sobrescritos = str.maketrans(
        "0123456789-+",
        "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺"
    )

    return f"{base} × 10{str(expoente).translate(sobrescritos)}"

def selecionar_opcao(valor):
    global opcao_selecionada

    opcao_selecionada = valor

    for codigo, botao in botoes_operacoes.items():
        cor = AZUL if codigo == valor else CAMPO

        botao.config(
            bg=cor,
            activebackground=cor
        )


def calcular():
    if opcao_selecionada is None:
        msg.showwarning(
            "Atenção",
            "Selecione uma operação matemática."
        )
        return

    try:
        texto1 = ent_n1.get().strip().replace(",", ".")
        texto2 = ent_n2.get().strip().replace(",", ".")

        if not texto1 or not texto2:
            msg.showwarning(
                "Atenção",
                "Preencha os dois campos."
            )
            return

        n1 = float(texto1)
        n2 = float(texto2)

        if not math.isfinite(n1) or not math.isfinite(n2):
            raise ValueError("Digite números finitos.")

        simbolo = next(
            item[2] for item in operacoes
            if item[1] == opcao_selecionada
        )

        if opcao_selecionada == 1:
            resultado = n1 + n2

        elif opcao_selecionada == 2:
            resultado = n1 - n2

        elif opcao_selecionada == 3:
            if n2 == 0:
                raise ZeroDivisionError
            resultado = n1 / n2

        elif opcao_selecionada == 4:
            resultado = n1 * n2

        elif opcao_selecionada == 5:
            resultado = n1 ** n2

            if isinstance(resultado, complex):
                raise ValueError(
                    "O resultado não é um número real."
                )

        elif opcao_selecionada == 6:
            if n2 == 0:
                raise ZeroDivisionError
            resultado = n1 % n2

        resultado_texto = formatar_resultado(resultado)
        numero1 = formatar_numero(n1)
        numero2 = formatar_numero(n2)

        expressao = f"{numero1} {simbolo} {numero2}"

        lbl_expressao.config(text=expressao)

        lbl_resultado.config(
            text=resultado_texto,
            fg=TEXTO
        )

        historico_calculos.append(
            f"{expressao} = {resultado_texto}"
        )

    except ZeroDivisionError:
        msg.showerror(
            "Erro matemático",
            "Não é possível dividir por zero."
        )

    except ValueError as erro:
        msg.showwarning(
            "Valor inválido",
            str(erro) if str(erro) else
            "Digite apenas números válidos."
        )

    except OverflowError:
        msg.showerror(
            "Erro",
            "O resultado é muito grande."
        )


def limpar():
    global opcao_selecionada

    ent_n1.delete(0, tk.END)
    ent_n2.delete(0, tk.END)

    lbl_expressao.config(
        text="Seu cálculo aparecerá aqui"
    )

    lbl_resultado.config(text="0")

    opcao_selecionada = None

    for botao in botoes_operacoes.values():
        botao.config(bg=CAMPO)

    ent_n1.focus_set()


def mostrar_historico():
    janela_historico = tk.Toplevel(janela)

    janela_historico.title("Histórico de cálculos")
    janela_historico.geometry("430x400")
    janela_historico.configure(bg=FUNDO)
    janela_historico.resizable(False, False)

    tk.Label(
        janela_historico,
        text="Histórico de cálculos",
        font=("Segoe UI", 17, "bold"),
        bg=FUNDO,
        fg=TEXTO
    ).pack(pady=(20, 15))

    frame_lista = tk.Frame(
        janela_historico,
        bg=FUNDO
    )
    frame_lista.pack(
        fill="both",
        expand=True,
        padx=20
    )

    barra = tk.Scrollbar(frame_lista)
    barra.pack(side="right", fill="y")

    lista = tk.Listbox(
        frame_lista,
        bg=CARTAO,
        fg=TEXTO,
        font=("Consolas", 12),
        bd=0,
        highlightthickness=0,
        selectbackground=AZUL,
        yscrollcommand=barra.set
    )

    lista.pack(
        side="left",
        fill="both",
        expand=True
    )

    barra.config(command=lista.yview)

    if historico_calculos:
        for calculo in reversed(historico_calculos):
            lista.insert(tk.END, calculo)
    else:
        lista.insert(
            tk.END,
            "Nenhum cálculo realizado."
        )

    def apagar_historico():
        if not historico_calculos:
            return

        confirmar = msg.askyesno(
            "Confirmar",
            "Deseja apagar todo o histórico?",
            parent=janela_historico
        )

        if confirmar:
            historico_calculos.clear()
            lista.delete(0, tk.END)
            lista.insert(
                tk.END,
                "Nenhum cálculo realizado."
            )

    tk.Button(
        janela_historico,
        text="Limpar histórico",
        command=apagar_historico,
        bg=VERMELHO,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        pady=10
    ).pack(
        fill="x",
        padx=20,
        pady=20
    )


# =========================
# JANELA PRINCIPAL
# =========================

janela = tk.Tk()

janela.title("Calculadora | Python")

# Tamanho corrigido
largura = 480
altura = 750

# Centralização da janela
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

x = (largura_tela - largura) // 2
y = (altura_tela - altura) // 2

janela.geometry(
    f"{largura}x{altura}+{x}+{y}"
)

janela.minsize(480, 650)
janela.resizable(True, True)
janela.configure(bg=FUNDO)


# =========================
# TÍTULO
# =========================

tk.Label(
    janela,
    text="CALCULADORA",
    font=("Segoe UI", 23, "bold"),
    bg=FUNDO,
    fg=TEXTO
).pack(pady=(20, 2))

tk.Label(
    janela,
    text="Operações matemáticas com Python",
    font=("Segoe UI", 10),
    bg=FUNDO,
    fg=SECUNDARIO
).pack(pady=(0, 15))


# =========================
# CAMPOS DE ENTRADA
# =========================

frame_entradas = tk.Frame(
    janela,
    bg=CARTAO
)

frame_entradas.pack(
    fill="x",
    padx=25,
    pady=5
)

frame_campos = tk.Frame(
    frame_entradas,
    bg=CARTAO
)

frame_campos.pack(
    fill="x",
    padx=15,
    pady=18
)


def criar_campo(pai, titulo, coluna):
    frame = tk.Frame(
        pai,
        bg=CARTAO
    )

    frame.grid(
        row=0,
        column=coluna,
        padx=7,
        sticky="ew"
    )

    tk.Label(
        frame,
        text=titulo,
        bg=CARTAO,
        fg=SECUNDARIO,
        font=("Segoe UI", 10)
    ).pack(
        anchor="w",
        pady=(0, 7)
    )

    entrada = tk.Entry(
        frame,
        bg=CAMPO,
        fg=TEXTO,
        insertbackground=TEXTO,
        font=("Segoe UI", 14),
        relief="flat",
        justify="center",
        bd=0
    )

    entrada.pack(
        fill="x",
        ipady=10
    )

    return entrada


frame_campos.columnconfigure(0, weight=1)
frame_campos.columnconfigure(1, weight=1)

ent_n1 = criar_campo(
    frame_campos,
    "Primeiro número",
    0
)

ent_n2 = criar_campo(
    frame_campos,
    "Segundo número",
    1
)


# =========================
# BOTÕES DE OPERAÇÕES
# =========================

tk.Label(
    janela,
    text="ESCOLHA UMA OPERAÇÃO",
    bg=FUNDO,
    fg=SECUNDARIO,
    font=("Segoe UI", 10, "bold")
).pack(
    anchor="w",
    padx=27,
    pady=(15, 10)
)

frame_operacoes = tk.Frame(
    janela,
    bg=FUNDO
)

frame_operacoes.pack(
    fill="x",
    padx=20
)

for coluna in range(3):
    frame_operacoes.columnconfigure(
        coluna,
        weight=1
    )

for indice, (texto, codigo, simbolo) in enumerate(operacoes):

    botao = tk.Button(
        frame_operacoes,
        text=texto,
        command=lambda v=codigo: selecionar_opcao(v),
        bg=CAMPO,
        fg=TEXTO,
        activeforeground=TEXTO,
        activebackground=AZUL_CLARO,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        cursor="hand2",
        pady=13
    )

    botao.grid(
        row=indice // 3,
        column=indice % 3,
        sticky="ew",
        padx=5,
        pady=5
    )

    botoes_operacoes[codigo] = botao


# =========================
# ÁREA DE RESULTADO
# =========================

frame_resultado = tk.Frame(
    janela,
    bg=CARTAO
)

frame_resultado.pack(
    fill="x",
    padx=25,
    pady=(15, 12)
)

tk.Label(
    frame_resultado,
    text="RESULTADO",
    bg=CARTAO,
    fg=SECUNDARIO,
    font=("Segoe UI", 10, "bold")
).pack(
    anchor="w",
    padx=15,
    pady=(12, 5)
)

lbl_expressao = tk.Label(
    frame_resultado,
    text="Seu cálculo aparecerá aqui",
    bg=CARTAO,
    fg=SECUNDARIO,
    font=("Segoe UI", 10)
)

lbl_expressao.pack(
    anchor="w",
    padx=15
)

lbl_resultado = tk.Label(
    frame_resultado,
    text="0",
    bg=CARTAO,
    fg=TEXTO,
    font=("Segoe UI", 27, "bold")
)

lbl_resultado.pack(
    anchor="w",
    padx=15,
    pady=(0, 12)
)


# =========================
# BOTÕES CALCULAR E LIMPAR
# =========================

frame_acoes = tk.Frame(
    janela,
    bg=FUNDO
)

frame_acoes.pack(
    fill="x",
    padx=25,
    pady=(5, 0)
)

frame_acoes.columnconfigure(0, weight=1)
frame_acoes.columnconfigure(1, weight=1)

btn_calcular = tk.Button(
    frame_acoes,
    text="Calcular",
    command=calcular,
    bg=AZUL,
    fg=TEXTO,
    activebackground=AZUL_CLARO,
    activeforeground=TEXTO,
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    cursor="hand2",
    pady=12
)

btn_calcular.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=(0, 5)
)

btn_limpar = tk.Button(
    frame_acoes,
    text="Limpar",
    command=limpar,
    bg=CAMPO,
    fg=TEXTO,
    activebackground=VERMELHO,
    activeforeground=TEXTO,
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    cursor="hand2",
    pady=12
)

btn_limpar.grid(
    row=0,
    column=1,
    sticky="ew",
    padx=(5, 0)
)


# =========================
# BOTÃO DE HISTÓRICO
# =========================

btn_historico = tk.Button(
    janela,
    text="Visualizar histórico",
    command=mostrar_historico,
    bg=FUNDO,
    fg=SECUNDARIO,
    activebackground=FUNDO,
    activeforeground=TEXTO,
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    cursor="hand2",
    bd=0
)

btn_historico.pack(pady=(15, 10))


# =========================
# ATALHOS E EXECUÇÃO
# =========================

# Enter realiza o cálculo
janela.bind(
    "<Return>",
    lambda evento: calcular()
)

# Escape limpa os campos
janela.bind(
    "<Escape>",
    lambda evento: limpar()
)

# Campo inicial selecionado
ent_n1.focus_set()

# Inicia o programa
janela.mainloop()
