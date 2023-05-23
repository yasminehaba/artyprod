from django.contrib import admin

# Register your models here.
from .models import*
from .models import Message
admin.site.register(Message)
from .models import Personnel
admin.site.register(Personnel)
from .models import Equipe
admin.site.register(Equipe)
from .models import ServiceProjet
admin.site.register(ServiceProjet)
from .models import Projet
admin.site.register(Projet)
from .models import ProjetRealisee
admin.site.register(ProjetRealisee)
from .models import Service
admin.site.register(Service)
from .models import Contact
admin.site.register(Contact)