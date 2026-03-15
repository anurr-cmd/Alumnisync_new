import django_filters
from .models import Profile


class AlumniFilter(django_filters.FilterSet):

    username = django_filters.CharFilter(field_name="user__username", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    department = django_filters.CharFilter(field_name="department", lookup_expr="icontains")
    designation = django_filters.CharFilter(field_name="designation", lookup_expr="icontains")
    company = django_filters.CharFilter(field_name="company", lookup_expr="icontains")
    location = django_filters.CharFilter(field_name="location", lookup_expr="icontains")

    join_year = django_filters.NumberFilter(field_name="join_year")
    passout_year = django_filters.NumberFilter(field_name="passout_year")

    phone = django_filters.CharFilter(field_name="phone", lookup_expr="icontains")
    
    # created_after = django_filters.DateFilter(
    #     field_name="created_at",
    #     lookup_expr="gte"
    # )
    
    created_at = django_filters.DateFromToRangeFilter()

    # created_before = django_filters.DateFilter(
    #     field_name="created_at",
    #     lookup_expr="lte"
    # )

    class Meta:
        model = Profile
        fields = [
            "username",
            "roll_no",
            "email",
            "department",
            "designation",
            "company",
            "location",
            "join_year",
            "passout_year",
            "phone",
        ]