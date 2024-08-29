from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, CARD
from datetime import datetime as dt
import json
import requests

app = Flask(__name__)
#обозначаем БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bj.db'
#инициируем БД когда запускается приложение
db.init_app(app)
#создать все что есть в db.Models
with app.app_context():
    db.create_all()

global deck
#new deck
#вне маршрута, тк базовая функция
def get_deck():
    deck_id = json.loads( requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
    return deck_id


@app.route('/')
#когда человек запустил сервис, отрисовываем стартовую страницу
def start_page():
    deck=get_deck()
    return render_template('index.html', deck=deck)
    
@app.route('/<deck>/new_card')
def get_card(deck, cards_cnt='1'):
    card = json.loads(requests.post('https://deckofcardsapi.com/api/deck/'+deck+'/draw/?count='+cards_cnt).text)['cards']
    
    new_card=CARD(value=card[0]['value'], type=card[0]['suit'])
    db.session.add(new_card)
    db.session.commit()
    
    card_list = CARD.query.all()
    
    return render_template('index.html', card=card, deck= deck, card_list=card_list)
 
'''[{'code': '7S', 'image': 'https://deckofcardsapi.com/static/img/7S.png', 'images': {'svg': 'https://deckofcardsapi.com/static/img/7S.svg', 'png': 'https://deckofcardsapi.com/static/img/7S.png'}, 'value': '7', 'suit': 'SPADES'}]'''

if __name__ == '__main__':
    app.run()
