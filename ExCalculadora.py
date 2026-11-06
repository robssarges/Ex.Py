import tkinter as tk
from tkinter import messagebox

janela = tk.Tk()
janela.title("Calculadora")
janela.geometry("350x520")
janela.resizable(False, False)
janela.configure(bg="#D6D6D6")

FUNDO = "#D6D6D6"
VISOR = "#F5F5F5"
BOTAO = "#EAEAEA"
OPERADOR = "#C8C8C8"
DESTAQUE = "#B5B5B5"
TEXTO = "#222222"

valor = tk.StringVar(value="0")
primeiro_numero = None
operacao = None
aguardando_segundo = False
resultado_exibido = False


def adicionar_numero(numero):
    global aguardando_segundo, resultado_exibido

    atual = valor.get()

    if aguardando_segundo or resultado_exibido:
        valor.set(numero)
        aguardando_segundo = False
        resultado_exibido = False

    elif atual == "0":
        valor.set(numero)

    elif len(atual) < 15:
        valor.set(atual + numero)


def adicionar_decimal():
    global aguardando_segundo, resultado_exibido

    if aguardando_segundo or resultado_exibido:
        valor.set("0.")
        aguardando_segundo = False
        resultado_exibido = False

    elif "." not in valor.get():
        valor.set(valor.get() + ".")


def selecionar_operacao(op):
    global primeiro_numero, operacao
    global aguardando_segundo, resultado_exibido

    if operacao is not None and not aguardando_segundo:
        calcular()

    primeiro_numero = float(valor.get())
    operacao = op
    aguardando_segundo = True
    resultado_exibido = False


def formatar_resultado(numero):
    return format(numero, ".10g")


def calcular():
    global primeiro_numero, operacao
    global aguardando_segundo, resultado_exibido

    if primeiro_numero is None or operacao is None:
        return

    if aguardando_segundo:
        return

    segundo_numero = float(valor.get())

    if operacao == "+":
        resultado = primeiro_numero + segundo_numero

    elif operacao == "-":
        resultado = primeiro_numero - segundo_numero

    elif operacao == "×":
        resultado = primeiro_numero * segundo_numero

    elif operacao == "÷":
        if segundo_numero == 0:
            messagebox.showwarning(
                "Erro",
                "Não é possível dividir por zero!"
            )
            limpar()
            return

        resultado = primeiro_numero / segundo_numero

    valor.set(formatar_resultado(resultado))

    primeiro_numero = None
    operacao = None
    aguardando_segundo = False
    resultado_exibido = True


def limpar():
    global primeiro_numero, operacao
    global aguardando_segundo, resultado_exibido

    valor.set("0")
    primeiro_numero = None
    operacao = None
    aguardando_segundo = False
    resultado_exibido = False


def apagar_ultimo():
    global aguardando_segundo, resultado_exibido

    if aguardando_segundo or resultado_exibido:
        valor.set("0")
        aguardando_segundo = False
        resultado_exibido = False
        return

    atual = valor.get()

    if len(atual) > 1:
        novo = atual[:-1]

        if novo == "-":
            novo = "0"

        valor.set(novo)
    else:
        valor.set("0")


def inverter_sinal():
    global resultado_exibido

    atual = valor.get()

    if atual != "0":
        if atual.startswith("-"):
            valor.set(atual[1:])
        else:
            valor.set("-" + atual)

        resultado_exibido = False


titulo = tk.Label(
    janela,
    text="Calculadora",
    font=("Arial", 20, "bold"),
    bg=FUNDO,
    fg=TEXTO
)
titulo.pack(pady=18)

# Visor
painel = tk.Frame(
    janela,
    bg=VISOR,
    padx=10,
    pady=15
)
painel.pack(fill="x", padx=15, pady=10)

visor = tk.Entry(
    painel,
    textvariable=valor,
    font=("Arial", 30),
    bg=VISOR,
    fg=TEXTO,
    justify="right",
    relief="flat",
    state="readonly"
)
visor.pack(fill="x", ipady=12)

teclado = tk.Frame(janela, bg=FUNDO)
teclado.pack(fill="both", expand=True, padx=12, pady=10)

for i in range(4):
    teclado.columnconfigure(i, weight=1)

for i in range(5):
    teclado.rowconfigure(i, weight=1)


def criar_botao(texto, comando, linha, coluna,
                cor=BOTAO, largura=1, altura=1):

    botao = tk.Button(
        teclado,
        text=texto,
        command=comando,
        font=("Arial", 17, "bold"),
        bg=cor,
        fg=TEXTO,
        activebackground=DESTAQUE,
        activeforeground=TEXTO,
        relief="raised",
        bd=1
    )

    botao.grid(
        row=linha,
        column=coluna,
        columnspan=largura,
        rowspan=altura,
        sticky="nsew",
        padx=3,
        pady=3
    )

criar_botao("C", limpar, 0, 0, OPERADOR)
criar_botao("⌫", apagar_ultimo, 0, 1, OPERADOR)
criar_botao("÷", lambda: selecionar_operacao("÷"), 0, 2, OPERADOR)
criar_botao("×", lambda: selecionar_operacao("×"), 0, 3, OPERADOR)

criar_botao("7", lambda: adicionar_numero("7"), 1, 0)
criar_botao("8", lambda: adicionar_numero("8"), 1, 1)
criar_botao("9", lambda: adicionar_numero("9"), 1, 2)
criar_botao("-", lambda: selecionar_operacao("-"), 1, 3, OPERADOR)

criar_botao("4", lambda: adicionar_numero("4"), 2, 0)
criar_botao("5", lambda: adicionar_numero("5"), 2, 1)
criar_botao("6", lambda: adicionar_numero("6"), 2, 2)
criar_botao("+", lambda: selecionar_operacao("+"), 2, 3, OPERADOR)

criar_botao("1", lambda: adicionar_numero("1"), 3, 0)
criar_botao("2", lambda: adicionar_numero("2"), 3, 1)
criar_botao("3", lambda: adicionar_numero("3"), 3, 2)
criar_botao("=", calcular, 3, 3, DESTAQUE, altura=2)

criar_botao("0", lambda: adicionar_numero("0"), 4, 0, largura=2)
criar_botao(".", adicionar_decimal, 4, 2)

rodape = tk.Button(
    janela,
    text="+/-  Inverter sinal",
    command=inverter_sinal,
    font=("Arial", 10),
    bg=FUNDO,
    fg=TEXTO,
    relief="flat"
)
rodape.pack(pady=8)

def usar_teclado(event):
    tecla = event.keysym
    caractere = event.char

    if caractere.isdigit():
        adicionar_numero(caractere)
    elif caractere in [".", ","]:
        adicionar_decimal()
    elif caractere in ["+", "-"]:
        selecionar_operacao(caractere)
    elif caractere == "*":
        selecionar_operacao("×")
    elif caractere == "/":
        selecionar_operacao("÷")
    elif tecla in ["Return", "equal"]:
        calcular()
    elif tecla == "BackSpace":
        apagar_ultimo()
    elif tecla == "Escape":
        limpar()


janela.bind("<Key>", usar_teclado)

janela.mainloop()