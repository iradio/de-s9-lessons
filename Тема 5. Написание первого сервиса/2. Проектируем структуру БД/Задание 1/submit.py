import os
import sys
import importlib
import json

import requests

class TerminalColors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

def submit(test_name, rlz_file=''):
    user_code = ''
    if rlz_file:
        full_lesson_path = os.path.dirname(os.path.abspath(__file__))
        user_file = f'{full_lesson_path}/{rlz_file}'

        with open(user_file, 'r') as u_file:
            user_code = u_file.read()

    settings_path = os.path.dirname(os.path.abspath(__file__)).split('Тема')[0]

    sys.path.append(settings_path)
    u_settings = importlib.import_module('settings')
    TESTS_HOST_2 = u_settings.TESTS_HOST_2
    student = u_settings.student
    pg_settings = u_settings.pg_settings

    try:
        r = requests.get(
            f'http://{TESTS_HOST_2}/health'
        )
        if r.status_code != 200:
            print(f'Что-то пошло не так, сервер вернул ошибку {r.status_code}')
            return

        r = requests.post(
            f'http://{TESTS_HOST_2}/{test_name}',
            json={
                "student": student,
                "pg_settings": pg_settings,
                },
            timeout=300
        )

    except Exception as e:
        print(e)
        return

    if r.status_code:
        if 'result_key' in r.json()['response']['payload']:
            print(f"\n{TerminalColors.OKGREEN}{r.json()['response']['payload']['message']}{TerminalColors.ENDC}")
            print(f"Ключ: {r.json()['response']['payload']['result_key']}")
        else:
            print(f"\n{TerminalColors.FAIL}{r.json()['response']['payload']['message']}{TerminalColors.ENDC}")
    else:
        print(f'Что-то пошло не так, сервер вернул ошибку {r.status_code}')
        

if __name__ == '__main__':
    submit('de09050201_check_schema_cdm')

