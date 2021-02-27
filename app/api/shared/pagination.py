from rest_framework.pagination import PageNumberPagination as DefaultPageNumberPagination


class PageNumberPagination(DefaultPageNumberPagination):
    page_size = 50
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100000
