import requests as re
from bs4 import BeautifulSoup
from tabulate import tabulate

s = re.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    })

def load_user_data(city_id,session):
    url = 'https://www.kinopoisk.ru/afisha/new/city/%d/' % (city_id)
    request = session.get(url)
    return request.text

def contain_movies_data(text):
    soup = BeautifulSoup(text,'html.parser')
    film_list = soup.find_all('div', {'class': 'item'})
    return film_list

results = []
for id_City in range(3):
    idC = id_City+1
    film_list = contain_movies_data(load_user_data(idC,s))
    for film in film_list:
            url = 'https://www.kinopoisk.ru/afisha/new/city/%d/' % (id_City)
            movie_link = url+film.find('div',{'class':'name'}).find('a').get('href')
            movie_desc = film.find('div',{'class':'name'}).find('a').text
            movie_id = film.get('id')
            date_img = film.find('div',{'class':'date'}).find_all('img')
            #https://st.kp.yandex.net/images/dates/1.png
            date_str = ''
            month = ''
            if (len(date_img)>2):
                date_str= date_img[0].get('src')[38] + date_img[1].get('src')[38]
                month = date_img[2].get('src')[44]+date_img[2].get('src')[45]  #/images/dates/month_01.png
            else:
                date_str = '0'+date_img[0].get('src')[38]
                month = date_img[1].get('src')[44]+date_img[1].get('src')[45]
            date_str += '.'+month
            #print(date_str)
            results.append({
                '1':movie_id,
                '2':str(idC),
                '3':movie_link,
                '4':movie_desc,
                '5':date_str,
                })

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)        
        self.setMinimumSize(QSize(600, 400))             # Устанавливаем размеры
        self.setWindowTitle("Простой пример парсера")   # Устанавливаем заголовок окна
        central_widget = QWidget(self)                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
        grid_layout = QGridLayout()                     # Создаём QGridLayout
        central_widget.setLayout(grid_layout)           # Устанавливаем данное размещение в центральный виджет
        table = QTableWidget(self)                      # Создаём таблицу
        table.setColumnCount(len(results[0]))           # Устанавливаем три колонки
        table.setRowCount(len(results))                 # и одну строку в таблице
        # Устанавливаем заголовки таблицы
        table.setHorizontalHeaderLabels(["ID", "Город", "Ссылка", "Название", "Дата показа"])
        for i,row in enumerate(results):
            for j,col in enumerate(row):
                item = QTableWidgetItem(results[i][str(j+1)])
                table.setItem(i,j,item)
        # делаем ресайз колонок по содержимому
        table.resizeColumnsToContents()
        grid_layout.addWidget(table, 0, 0)   # Добавляем таблицу в сетку
import sys
app = QApplication(sys.argv)
mw = MainWindow()
mw.show()
sys.exit(app.exec())
