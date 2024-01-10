from app.models import UserRoleEnum, RentForm, ReserveForm, Receipt, Staff, Room, Orderer,RoomType,CustomerType
from app import app, db, dao
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect, request

admin = Admin(app=app, name='QUẢN TRỊ BÁN HÀNG', template_mode='bootstrap4')


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class RentFormView(AuthenticatedAdmin):
    column_list = ['id', 'orderer', 'create_date', 'checkin_date', 'checkout_date', 'rooms', 'customers', ]
    column_searchable_list = ['id']
    column_filters = ['checkin_date']
    can_export = True
    edit_modal = True
    can_view_details = True


class ReserveFormView(AuthenticatedAdmin):
    column_list = ['id', 'orderer', 'create_date', 'checkin_date', 'checkout_date', 'customers', ]

    column_searchable_list = ['id']
    column_filters = ['checkin_date']
    can_export = True
    edit_modal = True


class StaffView(AuthenticatedAdmin):
    column_list = ['id', 'name', 'address', 'id_card', 'dob', 'salary', 'role']
    column_searchable_list = ['id','name']
    column_filters = ['name']
    can_export = True
    edit_modal = True


class RoomView(AuthenticatedAdmin):
    column_list = ['id', 'name', 'status', 'room_type.formatted_price', 'room_type']
    column_searchable_list = ['name']
    column_filters = ['name']
    can_export = True
    edit_modal = True
    column_labels = {
        'id': 'Id',
        'name': 'Name',
        'status': 'Status',
        'room_type.formatted_price': 'Price',
        'room_type': 'Type'
    }


class ReceiptView(AuthenticatedAdmin):
    column_list = ['id', 'orderer.name', 'created_date', 'caculate_price']
    column_searchable_list = ['price']
    column_filters = ['price']
    can_export = True
    edit_modal = True


class OrdererView(AuthenticatedAdmin):
    column_list = ['id', 'name', 'email', 'phone']
    column_searchable_list = ['name']
    column_filters = ['name']
    can_export = True
    edit_modal = True

class RoomTypeView(AuthenticatedAdmin):
    column_list = ['id', 'type', 'formatted_price']
    column_searchable_list = ['type']
    column_filters = ['type']
    can_export = True
    edit_modal = True
    column_labels = {
        'id': 'Id',
        'type': 'Type Name',
        'formatted_price': 'Price',
    }

class CustomerTypeView(AuthenticatedAdmin):
    column_list = ['id', 'type', 'value']
    column_filters = ['type']
    can_export = True
    edit_modal = True


class MyStatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        month = request.args.get('months')

        # index_selected = month -1
        revenue = dao.revenue_stats(month)
        total = sum(item[2] for item in revenue)
        room_frequency = dao.room_frequency(month)

        return self.render('admin/stats.html', revenue=revenue, total=total, room_frequency=room_frequency)


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(StaffView(Staff, db.session))
admin.add_view(RoomView(Room, db.session))
admin.add_view(RentFormView(RentForm, db.session))
admin.add_view(ReserveFormView(ReserveForm, db.session))
admin.add_view(ReceiptView(Receipt, db.session))
admin.add_view(OrdererView(Orderer, db.session))
admin.add_view(RoomTypeView(RoomType, db.session))
admin.add_view(CustomerTypeView(CustomerType, db.session))



admin.add_view(MyStatsView(name='Statistic'))
admin.add_view(LogoutView(name='Log out'))
