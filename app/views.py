from app import app, db
from app.models import User, Product
from flask import render_template, request
from datetime import datetime


@app.route('/')
def index():
    
    # Получаем все записи из таблицы Product
    car_list = Car.query.all()

    # Получаем все записи из таблицы User
    user_list = User.query.all()

    # Полученные наборы передаем в контекст
    context = {
        'product_list': product_list,
        'user_list': user_list,
    }

    return render_template('index.html', **context)


@app.route('/create_auto', methods=['POST', 'GET'])
def create_auto():

    context = None

    if request.method == 'POST':
        
        # Пришел запрос с методом POST (пользователь нажал на кнопку 'Добавить товар')
        # Получаем название товара - это значение поля input с атрибутом name="title"
        car_title = request.form['title']

        # Получаем цену товара - это значение поля input с атрибутом name="price"
        product_price = request.form['price']

        # Добавляем товар в базу данных
        db.session.add(Product(title=product_title, price=product_price, img_url=request.form['img_url']))

        # сохраняем изменения в базе
        db.session.commit()

        # Заполняем словарь контекста
        context = {
            'method': 'POST',
            'title': product_title,
            'price': product_price,
        }
    
    elif request.method == 'GET':

        # Пришел запрос с методом GET - пользователь просто открыл в браузере страницу по адресу http://127.0.0.1:5000/create_product
        # В этом случае просто передаем в контекст имя метода
        context = {
            'method': 'GET',
        }

    return render_template('create_product.html', **context)

@app.route('/create_user', methods=['POST', 'GET'])
def create_user():

    context = None

    if request.method == 'POST':
        
        name = request.form['name']
        username = request.form['username']

        db.session.add(User(name=name, username=username))
        db.session.commit()

        context = {
            'method': 'POST',
            'name': name,
            'username': username,
        }
    
    elif request.method == 'GET':

        context = {
            'method': 'GET',
        }

    return render_template('create_user.html', **context)

@app.route('/product_detail/<int:product_id>', methods=['POST', 'GET'])
def product_detail(product_id):
    
    product = Product.query.get(product_id)


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

@app.route('/del_product/<int:product_id>', methods=['POST'])
def del_product(product_id):
    
    product = Product.query.get(product_id)

    context = {
        'title': product.title,
        'price': product.price,
        'img_url': product.img_url,
    }
    
    db.session.delete(product)
    db.session.commit()

    return render_template('del_product.html', **context)
