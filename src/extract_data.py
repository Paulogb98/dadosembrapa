from bs4 import BeautifulSoup
from flask import Response
import requests
import json


def script_comercializacao(ano=None):
    anos = [ano] if ano else range(1970, 2023+1)
    comercializacao_total = {}

    for ano in anos:
        url_comercializacao = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_04'
        response = requests.get(url_comercializacao)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            linhas = soup.select('tbody tr')
            comercializacao = {}

            for linha in linhas:
                colunas = linha.find_all('td')
                if len(colunas) == 2:
                    nome = colunas[0].get_text().strip()
                    valor = int(colunas[1].get_text().strip().replace('.', '').replace('-', '0'))
                    if 'tb_item' in colunas[0]['class']:
                        tipo_atual = nome
                        comercializacao[tipo_atual] = {'total': valor, 'variedades': {}}
                    elif 'tb_subitem' in colunas[0]['class'] and tipo_atual:
                        if tipo_atual in comercializacao:
                            comercializacao[tipo_atual]['variedades'][nome] = valor

            comercializacao_total[ano] = comercializacao
        else:
            return f"Erro na requisição para o ano {ano}: {response.status_code}"

    json_data = json.dumps(comercializacao_total, ensure_ascii=False, indent=4)
    return Response(json_data, mimetype='application/json')


def script_exportacao(ano=None):
    anos = [ano] if ano else range(1970, 2023+1)
    subopcoes = ['01', '02', '03', '04']
    subopcoes_nomes = ['Vinhos de mesa', 'Espumantes', 'Uvas frescas', 'Suco de uva']
    exportacao_total = {}

    for ano in anos:
        exportacao_total[ano] = {}

        for idx, subopcao in enumerate(subopcoes):
            subopcao_nome = subopcoes_nomes[idx]
            url_exportacao = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_06&subopcao=subopt_{subopcao}'
            response = requests.get(url_exportacao)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')
                linhas = soup.select('tbody tr')
                exportacao_subopcao = {}

                for linha in linhas:
                    colunas = linha.find_all('td')
                    if len(colunas) == 3:
                        pais = colunas[0].get_text().strip()
                        quantidade = int(colunas[1].get_text().strip().replace('.', '').replace('-', '0'))
                        valor = int(colunas[2].get_text().strip().replace('.', '').replace('-', '0'))
                        exportacao_subopcao[pais] = {'quantidade': quantidade, 'valor': valor}

                exportacao_total[ano][subopcao_nome] = exportacao_subopcao
            else:
                return f"Erro na requisição para o ano {ano}, subopção {subopcao}: {response.status_code}"

    json_data = json.dumps(exportacao_total, ensure_ascii=False, indent=4)
    return Response(json_data, mimetype='application/json')


def script_importacao(ano=None):
    anos = [ano] if ano else range(1970, 2023+1)
    subopcoes = ['01', '02', '03', '04', '05']
    subopcoes_nomes = ['Vinhos de mesa', 'Espumantes', 'Uvas frescas', 'Uvas passas', 'Suco de uva']
    importacao_total = {}

    for ano in anos:
        importacao_total[ano] = {}

        for idx, subopcao in enumerate(subopcoes):
            subopcao_nome = subopcoes_nomes[idx]
            url_importacao = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao=subopt_{subopcao}'
            response = requests.get(url_importacao)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')
                linhas = soup.select('tbody tr')
                importacao_subopcao = {}

                for linha in linhas:
                    colunas = linha.find_all('td')
                    if len(colunas) == 3:
                        pais = colunas[0].get_text().strip()
                        quantidade = int(colunas[1].get_text().strip().replace('.', '').replace('-', '0'))
                        valor = int(colunas[2].get_text().strip().replace('.', '').replace('-', '0'))
                        importacao_subopcao[pais] = {'quantidade': quantidade, 'valor': valor}

                importacao_total[ano][subopcao_nome] = importacao_subopcao
            else:
                return f"Erro na requisição para o ano {ano}, subopção {subopcao}: {response.status_code}"

    json_data = json.dumps(importacao_total, ensure_ascii=False, indent=4)
    return Response(json_data, mimetype='application/json')


def script_processamento(ano=None):
    anos = [ano] if ano else range(1970, 2023+1)
    subopcao = ['01', '02', '03', '04']
    subopcao_nomes = ['Viníferas', 'Americanas e híbridas', 'Uvas de mesa', 'Sem classificação']
    processamento_total = {}

    for ano in anos:
        processamento_ano = {}

        for idx, subop in enumerate(subopcao):
            subop_nome = subopcao_nomes[idx]
            url_processamento = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_03&subopcao=subopt_{subop}'
            response = requests.get(url_processamento)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')
                linhas = soup.select('tbody tr')
                processamento_subop = {}

                for linha in linhas:
                    colunas = linha.find_all('td')
                    if len(colunas) == 2:
                        nome = colunas[0].get_text().strip()
                        valor = int(colunas[1].get_text().strip().replace('.', '').replace('-', '0').replace('*', '0').replace('nd', '0'))
                        if 'tb_item' in colunas[0]['class']:
                            tipo_atual = nome
                            processamento_subop[tipo_atual] = {'total': valor, 'variedades': {}}
                        elif 'tb_subitem' in colunas[0]['class'] and tipo_atual:
                            if tipo_atual in processamento_subop:
                                processamento_subop[tipo_atual]['variedades'][nome] = valor

            processamento_ano[subop_nome] = processamento_subop

        processamento_total[ano] = processamento_ano

    json_data = json.dumps(processamento_total, ensure_ascii=False, indent=4)
    return Response(json_data, mimetype='application/json')


def script_producao(ano=None):
    anos = [ano] if ano else range(1970, 2023+1)
    producao_total = {}

    for ano in anos:
        url_producao = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02'
        response = requests.get(url_producao)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            linhas = soup.select('tbody tr')
            producao = {}

            for linha in linhas:
                colunas = linha.find_all('td')
                if len(colunas) == 2:
                    nome = colunas[0].get_text().strip()
                    valor = int(colunas[1].get_text().strip().replace('.', '').replace('-', '0'))
                    if 'tb_item' in colunas[0]['class']:
                        tipo_atual = nome
                        producao[tipo_atual] = {'total': valor, 'variedades': {}}
                    elif 'tb_subitem' in colunas[0]['class'] and tipo_atual:
                        if tipo_atual in producao:
                            producao[tipo_atual]['variedades'][nome] = valor

            producao_total[ano] = producao
        else:
            return f"Erro na requisição para o ano {ano}: {response.status_code}"

    json_data = json.dumps(producao_total, ensure_ascii=False, indent=4)
    return Response(json_data, mimetype='application/json')