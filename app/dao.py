from datetime import datetime

from sqlalchemy import func, cast, Numeric

from app.models import User, rent_room, RoomType, Room, Receipt, RentForm, Orderer, ReserveForm, Staff
from app import app, db
import hashlib
import flask_sqlalchemy
from flask_login import current_user


def get_categories():
    pass
    # return Category.query.all()


# def load_room(ks=None):
#
#     ks = Room.query
#
#     if ks:
#         products = Room.filter(R.name.contains(kw))
#
#     if cate_id:
#         products = products.filter(Product.category_id.__eq__(cate_id))
#
#     if page:
#         page = int(page)
#         page_size = app.config['PAGE_SIZE']
#         start = (page - 1)*page_size
#
#         return products.slice(start, start + page_size)
#
#     return products.all()

def load_rooms(rp=None):
    rt = RoomType.query
    if rp:
        rt = rt.filter(RoomType.price.between(0, rp))
    return rt.all()


def load_room():
    pk = Room.query.all()
    return pk


def get_room(kw=None):
    rooms = Room.query

    if kw:
        rooms = rooms.filter(Room.name.contains(kw))

    return rooms.all()


def load_roomtype():
    roomtype = RoomType.query.all()
    return roomtype

def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_roomtype_by_id(id):
    return RoomType.query.get(id)


def add_orderer(name, email, phone,checkin,checkout):
    od1 = Orderer(name=name,email=email,phone=phone)
    db.session.add(od1)
    db.session.commit()

    lastODer = Orderer.query.order_by(Orderer.id.desc()).first()
    nvid = Staff.query.order_by(Staff.id.desc()).first()
    current_datetime = datetime.now()
    resfo = ReserveForm(staff_id = 1,checkin_date= checkin,checkout_date=checkout,orderer_id=1)
    db.session.add(resfo)
    db.session.commit()

    lastResfo = ReserveForm.query.order_by(ReserveForm.id.desc()).first()


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()


def add_receipt(cart):
    pass
    # if cart:
    #     r = Receipt(user=current_user)
    #     db.session.add(r)
    #
    #     for c in cart.values():
    #         d = ReceiptDetails(quantity=c['quantity'], price=c['price'], receipt=r, product_id=c['id'])
    #         db.session.add(d)
    #     try:
    #         db.session.commit()
    #     except:
    #         return False
    #     else:
    #         return True


def revenue_stats(month:None):

    if month == None:
        month = 1

    sub = db.session.query(func.count(rent_room.c.room_id)).join(RentForm, RentForm.id == rent_room.c.rent_form_id) \
        .filter(func.extract('month', RentForm.create_date).__eq__(1)) \
        .all()

    total_rooms_in_month = sub[0][0] if sub else 0

    query = db.session.query(RoomType.id, RoomType.type, db.func.sum(RoomType.price).label('total_price'),
                             db.func.count(Room.id).label('amount')
                             , ((db.func.count(Room.id) / total_rooms_in_month) * 100)) \
        .join(Room, RoomType.id == Room.room_type_id) \
        .join(rent_room, Room.id == rent_room.c.room_id) \
        .join(RentForm, RentForm.id == rent_room.c.rent_form_id) \
        .filter(func.extract('month', RentForm.create_date).__eq__(month)) \
        .group_by(RoomType.id, RoomType.type) \
        .all()

    return (query)


def room_frequency(month: None ):

    if month == None:
        month = 1

    sub = db.session.query(func.count(rent_room.c.room_id)).join(RentForm, RentForm.id == rent_room.c.rent_form_id) \
        .filter(func.extract('month', RentForm.create_date).__eq__(1)) \
        .all()

    total_rooms_in_month = sub[0][0] if sub else 0
    query = db.session.query(Room.name, func.count(Room.id),(func.count(Room.id)/total_rooms_in_month)*100) \
        .join(rent_room, Room.id == rent_room.c.room_id) \
        .join(RentForm, RentForm.id == rent_room.c.rent_form_id) \
        .filter(func.extract('month', RentForm.create_date).__eq__(month)) \
        .group_by(Room.name) \
        .all()

    return (query)
