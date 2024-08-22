from typing import Annotated

from django.db.models import Prefetch
from ninja import Router, Header

from travels.models import Country, Info
from travels.schemas import CountrySummarySchema

router = Router(tags=['travels'])

AcceptLanguage = Annotated[str, Header(alias='Accept-Language')]


@router.get('/countries', response=list[CountrySummarySchema])
def get_country_list(request, lang: AcceptLanguage):
    countries = Country.objects.prefetch_related(
        Prefetch('info', Info.objects.filter(lang__code=lang)),
        'main_image',
    )
    return countries
