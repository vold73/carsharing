from app import app, db
from app.models import Auto, RentTime
from flask import render_template, request
from datetime import datetime


@app.route('/')
def index():
    
    # Получаем все записи из таблицы Auto
    auto_list = Auto.query.all()

    # Получаем все записи из таблицы User (пока не обрабатываем)
    # user_list = User.query.all()

    # Полученные наборы передаем в контекст
    context = {
        'auto_list': auto_list
    #    'user_list': user_list,
    }

    return render_template('index.html', **context)


@app.route('/create_auto', methods=['POST', 'GET'])
def create_auto():
#НЕЗАКОНЧЕНО
    context = None

    if request.method == 'POST':
        
        # Пришел запрос с методом POST (пользователь нажал на кнопку 'Добавить машину')
        # Получаем название машины - это значение поля input с атрибутом name="name"
        auto_title = request.form['name']

        # Получаем цену машины - это значение поля input с атрибутом name="price"
        auto_price = request.form['price']

        # Получаем описание машины - это значение поля input с атрибутом name="description"
        auto_description = request.form['description']

        # Получаем КПП машины - это значение поля input с атрибутом name="transmission"
        # РАЗОБРАТЬСЯ С ПЕРЕДАЧЕЙ. TRUE/FALSE
        auto_at = request.form['transmission']

        auto_img1 = request.form['img_url1']
        auto_img2 = request.form['img_url2']
        auto_img3 = request.form['img_url3']
        auto_img4 = request.form['img_url4']

        #ДОБАВИТЬ в create_auto поля для картинок

        # Добавляем товар в базу данных
        db.session.add(Auto(title = auto_title, 
                            price = auto_price, 
                            description = auto_at, 
                            #at = 1 if auto_at == 'at_yes' else 0, 
                            img_url1 = auto_img1, 
                            img_url2 = auto_img2,
                            img_url3 = auto_img3,
                            img_url4 = auto_img4,
                            free = 1,
                            created = datetime.now()))

        # сохраняем изменения в базе
        db.session.commit()

        # Заполняем словарь контекста
        context = {
            'method': 'POST',
            'title': auto_title,
            'price': auto_price,
        }
    
    elif request.method == 'GET':

        # Пришел запрос с методом GET - пользователь просто открыл в браузере страницу по адресу http://127.0.0.1:5000/create_auto
        # В этом случае просто передаем в контекст имя метода
        context = {
            'method': 'GET',
        }

    return render_template('create_auto.html', **context)


@app.route('/auto_detail/<int:auto_id>', methods=['POST', 'GET'])
def auto_detail(auto_id):
    
    auto = Auto.query.get(auto_id)
    log_list = RentTime.query.filter_by(auto=auto_id).all()


    context = None


    if request.method == 'POST':


        new_title = request.form['new_title']
        new_price = request.form['new_price']
        new_img_url1 = request.form['new_img_url1']
        new_description = request.form['description']


        if new_title:
            auto.title = request.form['new_title']
        
        if new_price:
            auto.price = request.form['new_price']
        
        if new_img_url1:
            auto.img_url1 = request.form['new_img_url1']

        if new_description:
            auto.description = request.form['description']

        db.session.commit()


    context = {
        'id': auto.id,
        'title': auto.title,
        'price': auto.price,
        'description': auto.description,
        'yes_or_not': auto.at,
        'auto_free': auto.free,
        'start_rent':auto.start_rent,
        'log_list': log_list,
        'img_url1': auto.img_url1,
        'img_url2': auto.img_url2,
        'img_url3': auto.img_url3,
        'img_url4': auto.img_url4,
    }


    return render_template('auto_detail.html', **context)


@app.route('/rental_log', methods=['GET'])
def rental_log():

    log_record = {}
    log = []
    auto_list = Auto.query.all()
        
    # проходим по всем машинам
    for auto_id in auto_list:
        # выбираем для соответствующей машины все записи из базы журнала
        log_list = RentTime.query.filter_by(auto=auto_id.id).all()
        #log_list = RentTime.query.get(1)

        # добавляем в пустой словарь все нужные поля
        log_record['img'] = auto_id.img_url1
        log_record['title'] = auto_id.title
        log_record['description'] = auto_id.description
        log_record['count'] = len(log_list)
        log_record['cost'] = sum(item.cost for item in log_list)
        seconds = sum((item.end_rent - item.start_rent).seconds for item in log_list)
        # расчитываем количество секунд, минут, часов и дней общего времени аренды
        minutes = divmod(seconds, 60)
        hours = divmod(minutes[0], 60)
        days = divmod(hours[0], 24)
        log_record['time'] = f'{days[0]} д. {days[1]} ч. {hours[1]} м. {minutes[1]} с.'
        log.append(log_record)
        log_record = {}
    
    
    context = {
            'log': log,            
    }

    return render_template('rental_log.html', **context)


@app.route('/del_auto/<int:auto_id>', methods=['POST'])
def del_auto(auto_id):
    
    auto = Auto.query.get(auto_id)

    context = {
        'title': auto.title,
        'price': auto.price,
        'img_url1': auto.img_url1,
    }
    
    db.session.delete(auto)
    db.session.commit()

    return render_template('del_auto.html', **context)
