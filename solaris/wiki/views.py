from solaris.views import SolarisViewMixin

from wiki.views import article 

''' SolarisViewMixin contains a lot of site-wide stuff that our templates need, so
    wrap the Wiki views with it to keep consistency with the rest of the site
'''


'''
   Article Views
'''
class SolarisWikiMixin(SolarisViewMixin):
    menu_selected = 'Wiki'
    
class SolarisWikiArticleView(article.ArticleView, SolarisWikiMixin):
    pass

class SolarisWikiCreate(article.Create, SolarisWikiMixin):
    pass

class SolarisWikiDelete(article.Delete, SolarisWikiMixin):
    pass

class SolarisWikiEdit(article.Edit, SolarisWikiMixin):
    pass

class SolarisWikiDeleted(article.Deleted, SolarisWikiMixin):
    pass

class SolarisWikiSource(article.Source, SolarisWikiMixin):
    pass

class SolarisWikiHistory(article.History, SolarisWikiMixin):
    pass

class SolarisWikiDir(article.Dir, SolarisWikiMixin):
    pass

class SolarisWikiSearchView(article.SearchView, SolarisWikiMixin):
    pass

class SolarisWikiPlugin(article.Plugin, SolarisWikiMixin):
    pass

class SolarisWikiSettings(article.Settings, SolarisWikiMixin):
    pass

class SolarisWikiChangeRevisionView(article.ChangeRevisionView, SolarisWikiMixin):
    pass

class SolarisWikiPreview(article.Preview, SolarisWikiMixin):
    pass

class SolarisWikiCreateRootView(article.CreateRootView, SolarisWikiMixin):
    pass

class SolarisWikiMissingRootView(article.MissingRootView, SolarisWikiMixin):
    pass