from flask_admin.contrib.sqla import ModelView


class MyModelView(ModelView):
    can_edit = False
    edit_modal = True
    can_create = True
    create_modal = True
    can_export = False
    can_delete = True

    can_view_details = False
    details_modal = True
    column_display_pk = True


class ActorView(MyModelView):
    column_list = ['id', 'actor', 'actor_pro', 'need_modify']
    column_editable_list = ['actor', 'actor_pro']
    column_searchable_list = ['actor', 'actor_pro']
    column_default_sort = ('id', True)


class CategoryView(MyModelView):
    column_editable_list = ['title']


class ForumView(MyModelView):
    can_create = False
    can_view_details = True
    column_list = ['id', 'cid', 'fid', 'url', 'title', 'actor', 'actor_pro', 'create_date', 'create_time']
    column_editable_list = ['actor', 'actor_pro', 'create_date', 'create_time']
    column_searchable_list = ['title', 'actor', 'actor_pro']
    column_filters = ['cid']
    column_default_sort = ('id', True)
