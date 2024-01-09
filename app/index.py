from flask import render_template, request, redirect, jsonify, session
from flask_login import login_user
import dao
import utils
from app import app, login
from flask_login import login_user, current_user


# import paypalrestsdk


@app.route("/")
def index():
    roomtype = request.args.get('roomtype')
    roomtype = dao.load_roomtype()
    kw = request.args.get('kw')
    rooms = dao.get_room(kw)
    return render_template('index.html', roomtype=roomtype, rooms=rooms)


@app.route("/index")
def home():
    roomtype = request.args.get('roomtype')
    roomtype = dao.load_roomtype()
    kw = request.args.get('kw')
    rooms = dao.get_room(kw)
    return render_template('index.html', roomtype=roomtype, rooms=rooms)


@app.route('/room', methods=['post', 'get'])
def room():
    key_room = request.args.get('roomtype')
    room = dao.load_roomtype()

    kw = request.form.get('kw')
    rt = dao.load_rooms()

    return render_template('room.html', room=room, rt=rt)


@app.route('/room/<id>')
def product_details(id):
    return render_template('detail_room.html', room=dao.get_roomtype_by_id(id=id))


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user)

    return redirect('/admin/staff')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    data = request.json

    cart = session.get('cart')
    if cart is None:
        cart = {}

    id = str(data.get("id"))
    if id in cart:  # da co trong gio
        cart[id]['quantity'] += 1
    else:  # chua co trong gio
        cart[id] = {
            "id": id,
            "name": data.get('name'),
            "price": data.get('price'),
            "quantity": 1
        }

    session['cart'] = cart
    """
    {
        "1": {
            "id": "1",
            "name": "abc",
            "price": 123,
            "quantity": 2
        }, "2": {
            "id": "2",
            "name": "abc",
            "price": 123,
            "quantity": 1
        }
    }
    """

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        quantity = request.json.get('quantity')
        cart[product_id]['quantity'] = int(quantity)

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route('/login', methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)

        next = request.args.get('next')
        return redirect("/" if next is None else next)

    return render_template('admin/category')


@app.route("/api/pay", methods=['post'])
def pay():
    if dao.add_receipt(session.get('cart')):
        del session['cart']
        return jsonify({'status': 200})

    return jsonify({'status': 500, 'err_msg': 'Something wrong!'})


@app.route('/booking', methods=['get', 'post'])
def booking():
    key_room = request.args.get('roomtype')
    room = dao.load_roomtype()
    if request.method.__eq__('POST'):
        try:
            dao.add_orderer(name=request.form.get('name'),
                            email=request.form.get('email'),
                            phone=request.form.get('phone'), checkin=request.form.get('checkin'),
                            checkout=request.form.get('checkout'))
        except Exception as ex:
            print(str(ex))

    return render_template('booking.html', room=room)


@app.route('/service')
def service():
    return render_template('service.html')


@app.context_processor
def common_responses():
    return {
        'categories': dao.get_categories(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


# @app.route('/payment', methods=['POST'])
# def payment():
#
#     amount = request.form['amount']
#     description = request.form['description']
#
#     # Tạo thanh toán PayPal
#     payment = paypalrestsdk.Payment({
#         "intent": "sale",
#         "payer": {
#             "payment_method": "paypal"
#         },
#         "redirect_urls": {
#             "return_url": "http://localhost:5000/payment-success",
#             "cancel_url": "http://localhost:5000/cancel"
#         },
#         "transactions": [{
#             "item_list": {
#                 "items": [{
#                     "name": "Item",
#                     "sku": "item",
#                     "price": amount,
#                     "currency": "USD",
#                     "quantity": 1
#                 }]
#             },
#             "amount": {
#                 "total": amount,
#                 "currency": "USD"
#             },
#             "description": description
#         }]
#     })
#
#     if payment.create():
#         for link in payment.links:
#             if link.method == "REDIRECT":
#                 redirect_url = str(link.href)
#                 return redirect(redirect_url)
#     else:
#         return "Error during payment creation"


# @app.route('/', methods=['POST'])
# def stats_month():
#
#     month=request.form['months']
#     revenue = dao.revenue_stats(month)
#     total = sum(item[2] for item in revenue)
#
#     room_frequency = dao.room_frequency(month)
#
#     return render_template('admin/stats.html', revenue=revenue, total=total, room_frequency=room_frequency)


if __name__ == '__main__':
    with app.app_context():
        from app import admin

        # dao.revenue_stats(1)
        # dao.revenue_mon_stats()
        # dao.room_frequency(1)
        app.run(debug=True)
