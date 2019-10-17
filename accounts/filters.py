import django_filters
from .models import userPosts



class postFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(name='price', lookup_expr='lt')

    class Meta:
        model = userPosts
        fields = ('name','exchange','wilaya','phoneStatus','description')
