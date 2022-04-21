from datetime import datetime, timedelta
import requests

LISTA_MOEDAS = ("USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "DKK", "NOK", "SEK")


def get_value(question, validation):

    while True:
        if validation == "valores":
            try:
                result = float(input(f"{question}: ").replace(",", "."))
            except ValueError:
                print("Valor inválido. Apenas números.")
                continue

            if result < 0:
                print("O valor não pode ser negativo.")
                continue
            else:
                break

        if validation == "moedas":
            result = input(f"{question}: ").upper()
            if result in LISTA_MOEDAS:
                break
            else:
                print(
                    f"Moeda inválida. Apenas {'/'.join(LISTA_MOEDAS)} estão disponíveis para o cálculo."
                )

    return result


print("---")

moeda = get_value("Moeda", "moedas")
valor = get_value(f"Valor em {moeda}", "valores")
spread = get_value("Spread (em %)", "valores")

dia_inicio = (datetime.today() - timedelta(days=5)).strftime("%m-%d-%Y")
dia_final = datetime.today().strftime("%m-%d-%Y")

API_BC = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda='{moeda}'&@dataInicial='{dia_inicio}'&@dataFinalCotacao='{dia_final}'&$filter=contains(tipoBoletim%2C'Fechamento')&$orderby=dataHoraCotacao%20desc&$format=json"
IOF = 6.38

response_bc = requests.get(API_BC)

data_bc = response_bc.json()

dia_cotacao = data_bc["value"][0]["dataHoraCotacao"].split()[0]

valor_moeda = round(data_bc["value"][0]["cotacaoVenda"], 2)
moeda_spread = round(valor_moeda * ((100 + spread) / 100), 2)
moeda_spread_iof = round(moeda_spread * ((100 + IOF) / 100), 2)

valor_iof_brl = (valor * moeda_spread) * (IOF / 100)
valor_iof_usd = valor_iof_brl / valor_moeda

valor_final_iof = valor * moeda_spread_iof

print(f"---\nValor Final: {valor_final_iof:.2f} BRL ({valor:.2f} {moeda})")
print(f"Data Cotação: {dia_cotacao} | Valor {moeda} (PTAX): {valor_moeda:.2f} BRL")
print(
    f"Valor {moeda} (Spread): {moeda_spread:.2f} BRL | Valor {moeda} (Spread + IOF): {moeda_spread_iof:.2f}"
)
print(
    f"Spread: {spread:.2f}% | IOF: {IOF}% | Valor IOF: {valor_iof_brl:.2f} BRL ({valor_iof_usd:.2f} {moeda})\n---"
)
