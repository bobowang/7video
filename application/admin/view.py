# coding=utf-8

from flask import abort, redirect, url_for, request
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_security import current_user
from flask_security.utils import hash_password


class MyAdminIndexView(AdminIndexView):
    def __init__(self, name='首页', category=None, endpoint=None, url=None, template='admin/index.html',
                 menu_class_name=None, menu_icon_type='glyph', menu_icon_value='glyphicon-home'):
        super().__init__(name, category, endpoint, url, template, menu_class_name, menu_icon_type, menu_icon_value)


class AuthModelView(ModelView):
    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None,
                 static_folder=None, menu_class_name=None, menu_icon_type=None, menu_icon_value=None):
        self.can_edit = False
        self.edit_modal = True
        self.can_create = True
        self.create_modal = True
        self.can_export = False
        self.can_delete = True
        self.can_view_details = False
        self.column_display_pk = True
        self.details_modal = True

        super().__init__(model, session, name, category, endpoint, url, static_folder,
                         menu_class_name, menu_icon_type, menu_icon_value)

    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated \
               and current_user.has_role('administrator')

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


class ActorView(AuthModelView):
    def __init__(self, model, session, name='主演', category=None, endpoint=None, url=None,
                 static_folder=None, menu_class_name=None, menu_icon_type='glyph', menu_icon_value='glyphicon-user'):
        self.column_list = ['id', 'actor', 'actor_pro', 'need_modify']
        self.column_editable_list = ['actor', 'actor_pro']
        self.column_searchable_list = ['actor', 'actor_pro']
        self.column_default_sort = ('id', True)

        super().__init__(model, session, name, category, endpoint, url, static_folder,
                         menu_class_name, menu_icon_type, menu_icon_value)


class CategoryView(AuthModelView):
    def __init__(self, model, session, name='分类', category=None, endpoint=None, url=None,
                 static_folder=None, menu_class_name=None, menu_icon_type='glyph', menu_icon_value='glyphicon-tags'):
        self.column_editable_list = ['title']

        super().__init__(model, session, name, category, endpoint, url, static_folder,
                         menu_class_name, menu_icon_type, menu_icon_value)


class ForumView(AuthModelView):
    def __init__(self, model, session, name='帖子', category=None, endpoint=None, url=None,
                 static_folder=None, menu_class_name=None, menu_icon_type='glyph', menu_icon_value='glyphicon-film'):
        self.column_list = ['id', 'cid', 'fid', 'url', 'title', 'actor', 'actor_pro', 'create_date', 'create_time']
        self.column_editable_list = ['title', 'actor', 'actor_pro', 'create_date', 'create_time']
        self.column_searchable_list = ['title', 'actor', 'actor_pro']
        self.column_filters = ['cid']
        self.column_default_sort = ('id', True)

        super().__init__(model, session, name, category, endpoint, url, static_folder,
                         menu_class_name, menu_icon_type, menu_icon_value)

        self.can_create = False
        self.can_view_details = True


class UserView(AuthModelView):
    def __init__(self, model, session, name='用户', category=None, endpoint=None, url=None,
                 static_folder=None, menu_class_name=None, menu_icon_type='glyph', menu_icon_value='glyphicon-user'):
        self.column_list = ['id', 'username', 'email', 'phone', 'roles', 'active']
        self.column_editable_list = ['email', 'phone', 'roles', 'active']

        super().__init__(model, session, name, category, endpoint, url, static_folder,
                         menu_class_name, menu_icon_type, menu_icon_value)

        self.can_edit = True
        self.edit_modal = True

    def create_model(self, form):
        form.password.data = hash_password(form.password.data)
        return super(AuthModelView, self).create_model(form)

    def update_model(self, form, model):
        form.password.data = hash_password(form.password.data)
        return super(AuthModelView, self).update_model(form, model)


class RoleView(AuthModelView):
    def __init__(self, model, session, name='角色', category=None,
                 endpoint=None, url=None, static_folder=None, menu_class_name=None,
                 menu_icon_type='glyph', menu_icon_value='glyphicon-lock'):
        self.column_editable_list = ['name', 'description']

        super().__init__(model, session, name, category, endpoint, url, static_folder,
                         menu_class_name, menu_icon_type, menu_icon_value)
