import requests
import io
from datetime import datetime
import zipfile
import logging
import pdfkit
import tracemalloc

logging.basicConfig(filename="sample.log", level=logging.INFO)


# pip install pipenv
# pipenv install --dev
# для импорта необходимых библиотек

def upload(link):
    response = requests.get(link)

    try:
        z = zipfile.ZipFile(io.BytesIO(response.content))
    except zipfile.BadZipFile as e:
        print('Неверный формат файла')
        logging.info(f'Неверный формат файла - {e}')
    except zipfile.LargeZipFile as e:
        print('Размер файла превышает 2 Gb')
        logging.info(f'Размер файла превышает 2 Gb - {e}')

    file_name = link.split('/')[-1].split('.')[0]

    z.extractall()

    logging.info(f'Название файла {file_name}.zip')
    logging.info(f'Дата {datetime.now()}')


WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'


def html_to_pdf(file):
    start_time = datetime.now()
    tracemalloc.start()
    try:
        conf = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
        pdfkit.from_file(file, 'index.pdf', configuration=conf)
    except Exception:
        pass

    total_time = datetime.now() - start_time

    logging.info(f'Время затраченное на конвертацию {total_time}')
    logging.info(f'Память затраченная на конвертацию {tracemalloc.get_traced_memory()[1]}')


if __name__ == '__main__':
    upload('https://github.com/Spartacusc/help/blob/main/zipfile.zip?raw=true')
    html_to_pdf('index.html')
