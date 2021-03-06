from django.conf.urls import url, include

from modular_blocks import ModuleApp, TemplateTagBlock, modules

from . import urls


class CarpoolingModule(ModuleApp):
    app_name = 'cov'
    name = 'cov'
    urls = url(r'^carpooling/', include(urls))
    templatetag_blocks = [
        TemplateTagBlock(
            name='cov',
            library='cov_tag',
            tag='get_cov',
            cache_time=60
        ),
    ]


modules.register(CarpoolingModule)
