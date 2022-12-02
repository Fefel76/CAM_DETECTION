import requests
from requests.exceptions import HTTPError
import logging

def call_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.debug("Requête : %s \n Statut : %s \n Contenu : %s ", url, response.status_code, response.content)

        # Gestion des exceptions
    except HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
        return response.status_code
    except Exception as err:
        logging.error(f'Other error occurred: {err}')
        return response.status_code
    else:
        logging.info('Appel réussi de la requête : %s', url)
        return response.status_code, response.content


def send_sms(msg="TEST"):
    try :
        call_api("https://smsapi.free-mobile.fr/sendmsg?user=20226894&pass=HIh0RvwSUqE80x&msg="+msg)
    except:
        logging.error("Echec de l'envoi du SMS")
