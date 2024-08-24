from typing import Annotated

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from ninja import Router, Header, Path
from pydantic import UUID4

from travels.models import Country, Info
from travels.schemas import CountrySummarySchema, CountryDetailSchema

router = Router(tags=['travels'])

AcceptLanguage = Annotated[str, Header(alias='Accept-Language')]
ID = Annotated[UUID4, Path()]


@router.get('/countries', response=list[CountrySummarySchema])
def get_country_list(request, lang: AcceptLanguage):
    countries = Country.objects.prefetch_related(
        Prefetch('info', Info.objects.filter(lang__code=lang)),
        'main_image',
    )
    return countries


@router.get('/countries/{id}', response=CountryDetailSchema)
def get_country_detail(request, id: ID, lang: AcceptLanguage):
    return get_object_or_404(
        Country.objects.prefetch_related(
            Prefetch('info', Info.objects.filter(lang__code=lang)),
            'main_image',
        ),
        id=id,
    )
