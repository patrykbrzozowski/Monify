from datetime import datetime
from accounts.models import Account

def add_custom_context(request):
    return {
        'app_name': request.resolver_match.app_name,
        'page_path': request.path,
        'today': datetime.today(),
        'today_year': datetime.today().year,
        'user': request.user if request.user.is_authenticated else None,
        'user_saving_method': Account.objects.get(user_id=request.user.id).saving_method if request.user.is_authenticated else None,
        'user_currency': Account.objects.get(user_id=request.user.id).get_currency_display() if request.user.is_authenticated else None
    }
