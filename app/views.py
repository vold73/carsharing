from app import app, db
from app.models import User, Auto, RentTime
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
        auto_transmission = request.form['transmission']

        #ДОБАВИТЬ в create_auto поля для картинок

        # Добавляем товар в базу данных
        db.session.add(Auto(title=auto_title, price=auto_price, description=auto_description, at=True))

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

#@app.route('/create_user', methods=['POST', 'GET'])
#def create_user():
#
#    context = None
#
#    if request.method == 'POST':
#        
#        name = request.form['name']
#        username = request.form['username']
#
#        db.session.add(User(name=name, username=username))
#        db.session.commit()
#
#        context = {
#            'method': 'POST',
#            'name': name,
#            'username': username,
#        }
#    
#    elif request.method == 'GET':
#
#        context = {
#            'method': 'GET',
#        }
#
#    return render_template('create_user.html', **context)

@app.route('/auto_detail/<int:product_id>', methods=['POST', 'GET'])
def auto_detail(auto_id):
    
    aoto = Auto.query.get(auto_id)


    context = None


    if request.method == 'POST':


        new_title = request.form['new_title']
        new_price = request.form['new_price']
        new_img_url = request.form['new_img_url']


        if new_title:
            product.title = request.form['new_title']
        
        if new_price:
            product.price = request.form['new_price']
        
        if new_img_url:
            product.img_url = request.form['new_img_url']


        db.session.commit()


    age_seconds = (datetime.now() - product.created).seconds
    age = divmod(age_seconds, 60)


    context = {
        'id': product.id,
        'title': product.title,
        'price': product.price,
        'img_url': product.img_url,
        'age': f'{age[0]} мин {age[1]} сек',
    }


    return render_template('product_detail.html', **context)

@app.route('/rental_log/<int:auto_id>', methods=['POST'])
def rental_log(auto_id):
# Вывод журнала. ТРЕБУЕТСЯ НАПИСАТЬ    
    auto = Product.query.get(auto_id)

    context = {
        'title': product.title,
        'price': product.price,
        'img_url': product.img_url,
    }
    
    db.session.delete(product)
    db.session.commit()

    return render_template('del_product.html', **context)
