Notes on permissions for Django
See https://youtu.be/zszYgUXnId8

The difuculty here is that everypage shows things that some can see and some can't.  

The best option for now is to block: create, edit and delete.

Users will be:

viewers - can see everything - Matt
contributers - can CRUD but not staff - David
superuser - admin - michael
PW testing321

see PermissionRequiredMixin
https://docs.djangoproject.com/en/4.1/topics/auth/default/#the-permissionrequiredmixin-mixin


