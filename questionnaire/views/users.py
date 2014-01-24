from django.contrib.auth.models import User
from django.views.generic import ListView


class UsersList(ListView):
    template_name = 'users/index.html'
    model = User

    def __init__(self, **kwargs):
        super(UsersList, self).__init__(**kwargs)
        self.object_list = self.get_queryset()

    def get(self, *args, **kwargs):
        context = {'request': self.request, 'users': self.object_list}
        return self.render_to_response(context)