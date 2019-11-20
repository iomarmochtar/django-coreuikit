from django.utils.safestring import mark_safe
import django_tables2 as tables



class GridList(tables.Table):

    __start_num = None
    # spesial column for listing sequence number
    #seq_num = tables.Column(empty_values=(), orderable=False, verbose_name='#')

    def render_seq_num(self, value):
        if not self.__start_num:
            page_number = self.page.number
            if page_number == 1:
                self.__start_num = 1
            else:
                per_page = self.paginator.per_page
                self.__start_num = ( page_number * per_page ) - (per_page - 1)
        pn = self.__start_num
        self.__start_num += 1
        return pn
