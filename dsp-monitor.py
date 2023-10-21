#!/usr/bin/env python3
import os
import time
import subprocess
import requests
from datetime import datetime
import json
import urllib.parse

TELEGRAM_BOT_TOKEN = '1234567890:abcdefghijklmnopqrstuvwxyz'
TELEGRAM_CHAT_ID = '-10012345678'
TIME_TO_CHECK = 5

ADMINS = [
    { "id": "123456", "username": "@username" },
]

def mentions():
    links = []
    for admin in ADMINS:
        link = f'<a href="tg://user?id={admin["id"]}">{admin["username"]}</a>'
        links.append(link)

    # for link in links:
    #     print(link)

    links_formatados = " ".join(links)
    # print(links_formatados)
    return links_formatados

def enviar_mensagem_telegram(mensagem):
    print_log(mensagem)
    try:
        mensagem = print_log(mensagem, 'return')
        mensagem_codificada = urllib.parse.quote_plus(mensagem)
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={mensagem_codificada}&parse_mode=HTML"
        # datas = {
        #     "chat_id": TELEGRAM_CHAT_ID,
        #     "text": mensagem_codificada,
        #     "parse_mode": "HTML"
        # }

        # response = requests.get(url, params=datas)
        response = requests.get(url)
        print(url)
        print('RESPOSTA TELEGRAM::', response.status_code)
        # Verifica se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            print_log("Mensagem enviada com sucesso!")
        else:
            print_log(f"Falha ao enviar a mensagem. Código de status: {response.status_code}")
    except requests.exceptions.HTTPError as errh:
        print(f"Erro HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Erro de Conexão: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Tempo Limite Excedido: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Erro na Requisição: {err}")
    return

def verificar_status_servico(servico):
    try:
        output = subprocess.check_output(['systemctl', 'is-active', '--quiet', servico])
        return True, f"Serviço {servico} está ativo."
    except subprocess.CalledProcessError:
        return False, f"Serviço {servico} está inativo."

def reiniciar_servico(servico):
    try:
        subprocess.check_output(['systemctl', 'restart', servico])
        return True, f"Serviço {servico} reiniciado com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"Falha ao reiniciar o serviço {servico}: {e}"

def listar_servicos_disponiveis(serviceName):
    try:
        output = subprocess.check_output(['systemctl', 'list-units', '--type=service', '--all', '--no-pager', '--plain', '--quiet'], text=True)
        servicos_disponiveis = output.strip().splitlines()
        # json_string = json.dumps(servicos_disponiveis, indent=4)
        # print(json_string)
        if any( f"{serviceName}.service" in servico for servico in servicos_disponiveis):
            return True
        else:
            return False

    except subprocess.CalledProcessError:
        return False

def print_log(mensagem, mode = 'text'):
    data_hora_atual = datetime.now()
    formato_data_hora = data_hora_atual.strftime("[%Y-%m-%d %H:%M:%S]")
    message = f"{formato_data_hora}: {mensagem}"
    if mode == 'text':
        print(message)
    elif mode == 'return':
        return message

if __name__ == "__main__":
    mentions = mentions()
    # enviar_mensagem_telegram(f"✅ <b>TESTE:</b> <i>Teste de menção.</i> {mentions}")
    
    while True:
        servicos = ['apache2', 'mysql', 'nginx']
        for servico in servicos:
            serviceExists = listar_servicos_disponiveis(servico)
            if serviceExists:
                status, motivo = verificar_status_servico(servico)
                # print(status, motivo)
                # print_log(motivo)
                if not status:
                    mensagem = f"❌ <b>{servico}:</b> <i>O serviço parou.</i> {mentions}"
                    print_log(mensagem)
                    enviar_mensagem_telegram(mensagem)
                    status_reiniciar, motivo_reiniciar = reiniciar_servico(servico)
                    if status_reiniciar:
                        mensagem_reiniciar = f"✅ <b>{servico}:</b> <i>O serviço foi reiniciado com sucesso após parar.</i> {mentions}"
                    else:
                        mensagem_reiniciar = f"❌ <b>{servico}:</b> <i>Falha ao reiniciar o serviço após parar.</i> {mentions}"
                    print_log(mensagem_reiniciar)
                    enviar_mensagem_telegram(mensagem_reiniciar)
            else:
                mensagem = f"❌ <b>{servico}:</b> <i>O serviço não existe.</i>"
                print_log(mensagem)
        time.sleep(TIME_TO_CHECK)
