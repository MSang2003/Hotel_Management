from app.models import UserRoleEnum, RentForm, ReserveForm, Receipt, Staff,Room,RoomType,CustomerType, Customer
from app import app, db
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect

admin = Admin(app=app, name='QUẢN TRỊ BÁN HÀNG', template_mode='bootstrap4')


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class RentFormView(AuthenticatedAdmin):
    column_list = ['id', 'checkin_date', 'checkout_date','customers']
    column_searchable_list = ['id']
    column_filters = ['checkin_date']
    can_export = True
    edit_modal = True
    can_view_details = True


class ReserveFormView(AuthenticatedAdmin):
    column_list = ['id', 'checkin_date', 'checkout_date','customers']
    column_searchable_list = ['id']
    column_filters = ['checkin_date']
    can_export = True
    edit_modal = True

class StaffView(AuthenticatedAdmin):
    column_list = ['id', 'name', 'address','id_card','dob','salary','role']
    column_searchable_list = ['id']
    column_filters = ['name']
    can_export = True
    edit_modal = True

class RoomView(AuthenticatedAdmin):
    column_list = ['id', 'name','room', 'room_type_id']
    column_searchable_list = ['id']
    column_filters = ['id']
    can_export = True
    edit_modal = True


class ReceiptView(AuthenticatedAdmin):
    column_list = ['id', 'created_date', 'price']
    column_searchable_list = ['price']
    column_filters = ['price']
    can_export = True
    edit_modal = True

class CustomerView(AuthenticatedAdmin):
    column_list = ['id', 'name']
    column_searchable_list = ['name']
    column_filters = ['name']
    can_export = True
    edit_modal = True


class MyStatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')


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
admin.add_view(CustomerView(Customer, db.session))


admin.add_view(MyStatsView(name='Thống kê báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
