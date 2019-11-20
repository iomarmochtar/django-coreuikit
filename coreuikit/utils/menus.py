from menu import MenuItem


class PermissionMenuItem(MenuItem):
    permission = None

    def __init__(self, *args, **kwargs):
        if 'permission' in kwargs:
            self.permission = kwargs.pop('permission')
        super(PermissionMenuItem, self).__init__(*args, **kwargs)

    def check(self, request):
        self.visible = True
        if request.user and self.permission:
            self.visible = request.user.has_perms(self.permission)
