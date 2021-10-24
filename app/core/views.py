import time

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
import openpyxl
from django.utils import timezone
from django.views.generic import View

from core.forms import ContactFileForm
from core.models import Contact
from helpers.s3utils import upload_to_aws_folder

from helpers.tasks import create_new_contact


class HomeView(View):
    form_class = ContactFileForm
    queryset = Contact.objects.all().order_by('-created_at')
    template_name = "core/home.html"
    paginate_by = 5

    def get(self, request):
        form = self.form_class()

        return render(request, self.template_name, self.get_context_data(form, self.queryset))

    def post(self, request):
        form = ContactFileForm(request.POST, request.FILES)
        if form.is_valid():
            xls_file = request.FILES.get('xls_file')
            if xls_file:
                work_book = openpyxl.load_workbook(xls_file)
                exel_sheet = work_book.active
                keys = ('name', 'phone_number', 'email')

                contacts = []
                for row in exel_sheet.iter_rows(min_row=3, max_col=3, values_only=True):
                    if None in row:
                        break
                    contacts.append(dict(zip(keys, row)))

                create_new_contact.apply_async(kwargs={'contact_list': contacts})
                file_name = 'contact_files/%d.xlsx' % time.time()
                upload_to_aws_folder(file_name, xls_file)
                messages.success(request, "Contacts are being created")

            else:
                try:
                    form.save()
                    messages.success(request, "Manual order is created successfully")
                except ValueError as err:
                    messages.warning(request, err)

            form = self.form_class()

        return render(request, self.template_name, self.get_context_data(form, self.queryset))

    def get_paginated_object(self, queryset):
        paginator = Paginator(queryset, self.paginate_by)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return page_obj

    def get_context_data(self, form, queryset):
        context = {
            'form': form,
            'page_obj': self.get_paginated_object(queryset)
        }
        return context


