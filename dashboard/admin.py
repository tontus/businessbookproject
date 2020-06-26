from django.contrib import admin

from dashboard.models import *

admin.site.register(balance)
admin.site.register(adpack)
admin.site.register(refer)
admin.site.register(withdraw_requests)
admin.site.register(pm_accounts)
admin.site.register(bank_accounts)
admin.site.register(agent_accounts)
admin.site.register(deposit_history)

