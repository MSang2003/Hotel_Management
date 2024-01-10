from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from flask_login import UserMixin
import enum
from datetime import datetime
import cloudinary.uploader


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class CustomerType(db.Model):
    __tablename__ = 'customer_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False, unique=True)
    value = Column(Float, nullable=False)
    customers = relationship('Customer', backref='customer_type', lazy=True)

    def __str__(self):
        return self.type


class BaseUser(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    address = Column(String(50), nullable=False)
    id_card = Column(String(50), nullable=False, unique=True)


class RoomType(db.Model):
    __tablename__ = 'room_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False, unique=True)
    price = Column(Float, nullable=False, default=8754387)
    capacity = Column(Integer, nullable=False, default=2)
    image = Column(String(100))

    rooms = relationship('Room', backref='room_type', lazy=True)

    @property
    def formatted_price(self):
        return f'{self.price:,} VND'

    def __str__(self):
        return self.type


class Staff(BaseUser):
    __tablename__ = 'staff'
    dob = Column(DateTime, default=datetime.now())
    salary = Column(String(50), nullable=False, unique=False, default="47634")
    role = Column(String(50), nullable=False, unique=False, default='Nhanvien')

    account = relationship('User', backref='staff', lazy=True)


class Orderer(db.Model):
    __tablename__ = 'orderer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=False)

    rent_form = relationship('RentForm', backref='orderer', lazy=True)
    reserve_form = relationship('ReserveForm', backref='orderer', lazy=True)
    receipt = relationship('Receipt', backref='orderer', lazy=True)

    def __str__(self):
        return self.name


class BaseForm(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    checkin_date = Column(DateTime, default=datetime.now())
    checkout_date = Column(DateTime, default=datetime.now())
    create_date = Column(DateTime, default=datetime.now())

    orderer_id = Column(Integer, ForeignKey(Orderer.id), nullable=False)


rent_room = db.Table('rent_room', Column('rent_form_id', Integer, ForeignKey('rent_form.id'), primary_key=True),
                     Column('room_id', Integer, ForeignKey('room.id'), primary_key=True))

reverse_room = db.Table('reverse_room',
                        Column('reserve_form_id', Integer, ForeignKey('reserve_form.id'), primary_key=True),
                        Column('room_id', Integer, ForeignKey('room.id'), primary_key=True))


class RentForm(BaseForm):
    __tablename__ = 'rent_form'

    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=False)
    customers = relationship("Customer", backref='rent_form', lazy=True)
    rooms = relationship('Room', secondary='rent_room', lazy='subquery', backref=backref('rent_rooms', lazy=True))

    def __str__(self):
        return self.name


class ReserveForm(BaseForm):
    __tablename__ = 'reserve_form'

    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=True)
    customers = relationship("Customer", backref='reserve_form', lazy=True)

    rooms = relationship('Room', secondary='reverse_room', lazy='subquery', backref=backref('reverse_rooms', lazy=True))


class Room(db.Model):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    status = Column(Boolean, nullable=True, default=True)
    room_type_id = Column(Integer, ForeignKey(RoomType.id), nullable=False)

    def __str__(self):
        return self.name


class Customer(BaseUser):
    __tablename__ = 'customer'

    cus_coefficient_id = Column(Integer, ForeignKey(CustomerType.id), nullable=False, default=1)

    rent_form_id = Column(Integer, ForeignKey(RentForm.id), nullable=False, default=1)
    reserve_form_id = Column(Integer, ForeignKey(ReserveForm.id), nullable=True, default=1)

    def __str__(self):
        return self.name


class ExtraFee(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    price = Column(Float, default=100)

    def __str__(self):
        return self.name


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    price = Column(Float, default=100)

    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=False, default=1)
    rent_form_id = Column(Integer, ForeignKey(RentForm.id), nullable=False, default=1)
    extra_fee_id = Column(Integer, ForeignKey(ExtraFee.id), nullable=True)
    orderer_id = Column(Integer, ForeignKey(Orderer.id), nullable=True, default=1)

    @property
    def caculate_price(self):
            return f'{self.price:,} VND'

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)

    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    staff_id = Column(Integer, ForeignKey(Staff.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        #
        import hashlib

        #
        #
        # VietNam = CustomerType(type = 'Viet Nam',value = 1.0)
        # NuocNgoai = CustomerType(type = 'Nuoc ngoai',value = 1.3)
        # db.session.add_all([VietNam,NuocNgoai])
        # db.session.commit()
        #
        # room_type1 = RoomType(type='Phong thuong',image= 'https://res.cloudinary.com/dnzpkdfli/image/upload/v1704761195/images/u1qwkvucgdmclw8aqfw6.jpg')
        # room_type2 = RoomType(type='Phong VIP',image='https://res.cloudinary.com/dnzpkdfli/image/upload/v1704761196/images/advidzxvzsobyf9s2fwz.jpg')
        # db.session.add_all([room_type1, room_type2])
        # db.session.commit()
        #
        #
        # room_type3 = RoomType(type='Phong King',
        #                       image='https://res.cloudinary.com/dnzpkdfli/image/upload/v1704761196/images/qaqhzq5qmbsup55d06ic.jpg')
        # room_type4 = RoomType(type='Phong Queen',
        #                       image='https://res.cloudinary.com/dnzpkdfli/image/upload/v1704761198/images/tdkt8xebhh126oj3w1hz.jpg')
        # db.session.add_all([room_type3, room_type4])
        # db.session.commit()
        #
        #
        # room_type5 = RoomType(type='Phong President',price = 2000000,
        #                       image='https://res.cloudinary.com/dnzpkdfli/image/upload/v1704761196/images/qaqhzq5qmbsup55d06ic.jpg')
        # room_type6 = RoomType(type='Phong Ace',price = 5000000,
        #                       image='https://res.cloudinary.com/dnzpkdfli/image/upload/v1704761198/images/tdkt8xebhh126oj3w1hz.jpg')
        # db.session.add_all([room_type5, room_type6])
        # db.session.commit()

        # nguoidat1 = Orderer(name = 'nguoi dat 1', email = 'nguoidat1@gmail.com',phone = '04387')
        # nguoidat2 = Orderer(name = 'nguoi dat 2', email = 'nguoidat2@gmail.com',phone = '0434387')
        # nguoidat3 = Orderer(name = 'nguoi dat 3', email = 'nguoidat3@gmail.com',phone = '04343387')
        # db.session.add_all([nguoidat1, nguoidat3,nguoidat2])
        # db.session.commit()
        #
        #
        # r3 = Room(room_type_id=1, name = 'Executive Suite')
        # r4 = Room(room_type_id=2, name='Super Deluxe')
        #
        # db.session.add_all([r3, r4])
        # db.session.commit()
        # r5 = Room(room_type_id=3, name='Vua')
        # r6 = Room(room_type_id=4, name='Nu Hoang')
        #
        # db.session.add_all([r5, r6])
        # db.session.commit()
        #
        #
        #
        # extra1 = ExtraFee( name = "Thêm người",price = 1.2)
        # db.session.add((extra1))
        # db.session.commit()
        #
        # s1 = Staff(name = 'Hai', address = 'hcm', id_card = '43786754', )
        # s2 = Staff(name = 'Danh', address = 'hcm', id_card = '4378436754')
        # s3 = Staff(name = 'Trieu', address = 'hcm', id_card = '437867323254')
        # db.session.add_all([s3,s2,s1])
        # db.session.commit()

        # rent1 = RentForm(staff_id=1, orderer_id=1)
        # rent2 = RentForm(staff_id = 2,orderer_id =2)
        #
        # db.session.add_all([rent1, rent2])
        # db.session.commit()
        #
        #
        # re1 = ReserveForm(staff_id = 2,orderer_id = 2)
        # re2 = ReserveForm(staff_id = 3,orderer_id = 1)
        # db.session.add_all([re2, re1])
        # db.session.commit()
        #
        # c1 = Customer(name='Sang', address='HCm', id_card='8543679843', cus_coefficient_id=1)
        # c2 = Customer(name='Long', address='Gia Lai', id_card='8543546679843', cus_coefficient_id=2)
        # c3 = Customer(name='Hieu', address='BinhDuong', id_card='85436792843', cus_coefficient_id=1)
        # db.session.add_all([c1,c2,c3])
        # db.session.commit()
        # # #
        # #
        #
        #
        # u = User(name='Admin', username='admin',staff_id=1,
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN)
        # u3 = User(name='Receptionist', username='nhanvien',staff_id=2,
        #          password=str(hashlib.md5('12345'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.USER)
        # db.session.add(u)
        # db.session.add(u3)
        #
        # db.session.commit()

        # receipt = Receipt(staff_id=2)
        # db.session.add_all([receipt])
        # db.session.commit()

        # rent1 = RentForm.query.get(1)
        # room1 = Room.query.get(1)
        # room2 = Room.query.get(2)
        # rent1.rooms.append(room1)
        # rent1.rooms.append(room2)
        #
        # db.session.add((rent1))
        # db.session.commit()
