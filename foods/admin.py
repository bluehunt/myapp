from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import Food
from .models import FCategory
from .models import Trainner
from .models import Trainee
from .models import Workout
from .models import Evaluchoice
from .models import Evaluationt
from .models import PaymentTrainee
from .models import Bodytype
from .models import Theaim
from .models import Activities
from .models import bmr_a 
from .models import bmr_b
from .models import bmr_c
from .models import bmr_d
from django.conf import settings
from django.http import HttpResponse
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer,PageBreak
from reportlab.lib.enums import TA_RIGHT
# Import Arabic fonts
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
import reportlab
from reportlab.lib.pagesizes import landscape,A4
from reportlab.lib.units import cm

from django.utils import timezone
import datetime

def downloadpdf(modeladmin, request, queryset):
    reportlab_directory = os.path.dirname(reportlab.__file__)
    font_folder = os.path.join(reportlab_directory,"fonts")
    #print(font_folder)

    custom_font_folder = os.path.join(font_folder,"Arabic.ttf")
    custom_font = TTFont("arabic",custom_font_folder)
    pdfmetrics.registerFont(custom_font)

    model_name = modeladmin.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={model_name}.pdf'

    #pdf = canvas.Canvas(response, pagesize=letter)
    pdf = canvas.Canvas(response, pagesize=(landscape(A4)))
    pdf.setTitle('تقرير المتدربين')

    '''
    logo = ImageReader('http://django-unfriendly.readthedocs.io/en/latest/_static/img/python-logo-256.png')

    numero =150
    uno = 204 - numero
    dos = uno

    pdf.drawImage(logo, 250, 500,uno,dos, mask='auto')
    '''

    (width, height) = landscape(A4)
    #canvas.Canvas.drawCentredString(width / 2.0, height - 1.2 * cm, "تقرير المتدربين")

    # Define Arabic font for text
    pdf.setFont("arabic", 14, leading=0.5)  # حدد اسم الخط العربي وحجم النص

    pdf.drawCentredString(width / 2.0, height - 1.2 * cm, get_display(arabic_reshaper.reshape("تقرير المتدربين")))
    #pdf.drawRightString(width - 1 * cm, height - 1.2 * cm, str(timezone.now()))
    pdf.drawRightString(width - 1 * cm, height - 1.2 * cm, str(datetime.date.today()))

    headers = []
    for field in modeladmin.model._meta.fields:
        if field.name == 'ID' or field.name == 'id':
            headers.append(get_display(arabic_reshaper.reshape("الرقم")))
        elif field.name == 'teimage':
            pass
        elif field.name == 'infection':
            pass
        elif field.name == 'Trainee_active':
            pass
        elif field.name == 'tecontent':
            pass
        elif field.name == 'workout':
            pass
        elif field.name == 'nitrution_breakfast':
            pass
        elif field.name == 'nitrution_lunch':
            pass
        elif field.name == 'nitrution_dinner':
            pass
        elif field.name == 'bmr_value':
            pass
        elif field.name == 'a':
            pass
        elif field.name == 'b':
            pass
        elif field.name == 'c':
            pass
        elif field.name == 'd':
            pass
        elif field.name == 'total_nitrution':
            pass
        else:
            headers.append(get_display(arabic_reshaper.reshape(field.verbose_name)))
    #[get_display(arabic_reshaper.reshape(field.verbose_name)) for field in modeladmin.model._meta.fields]
    data = [headers]
    '''
    for obj in queryset:
        data_row = []
        for field in modeladmin.model._meta.fields:
            if field.name == 'teimage' and getattr(obj, field.name):
                image_path = getattr(obj, field.name).path
                pdf.drawImage(image_path, x, y, width=100, height=100)
            else:
                data_row.append(str(getattr(obj, field.name)))
        data.append([get_display(arabic_reshaper.reshape(cell)) for cell in data_row])
    '''
    for obj in queryset:
        data_row = []
        for field in modeladmin.model._meta.fields:
            if field.name == 'teimage':
                pass
                '''
                # قم بتحميل الصورة من المسار المحلي المخزن
                image_path = getattr(obj, field.name).path
                # أضف الصورة إلى الصف الحالي في البيانات
                data_row.append(Image(image_path, width=100, height=100))
                '''
            elif field.name == 'infection':
                pass
                '''
                # قم بتحميل الصورة من المسار المحلي المخزن
                image_path = getattr(obj, field.name).path
                # أضف الصورة إلى الصف الحالي في البيانات
                data_row.append(Image(image_path, width=100, height=100))
                '''
            elif field.name == 'Trainee_active':
                pass
            elif field.name == 'tecontent':
                pass
            elif field.name == 'workout':
                pass
            elif field.name == 'nitrution_breakfast':
                pass
            elif field.name == 'nitrution_lunch':
                pass
            elif field.name == 'nitrution_dinner':
                pass
            elif field.name == 'bmr_value':
                pass
            elif field.name == 'a':
                pass
            elif field.name == 'b':
                pass
            elif field.name == 'c':
                pass
            elif field.name == 'd':
                pass
            elif field.name == 'total_nitrution':
                pass
            else:
                data_row.append(get_display(arabic_reshaper.reshape(str(getattr(obj, field.name)))))
        #data.append([cell for cell in data_row])
        data.append(data_row)

    table = Table(data,hAlign='CENTER')
    table.setStyle(TableStyle(
        [
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0,0), (-1,-1), 'arabic'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]
    ))

    canvas_width = 600
    canvas_height = 600

    table.wrapOn(pdf, canvas_width, canvas_height)
    #table.drawOn(pdf, 40, canvas_height - len(data) * 20)  # 20 is an arbitrary row height
    table.drawOn(pdf, 40, canvas_height - len(data) * 30)  # 20 is an arbitrary row height

    pdf.save()

    return response

downloadpdf.short_description = "حمل تقرير المتدربين"


# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)




@admin.register(FCategory)
class FCategoryAdmin(admin.ModelAdmin):
    list_display = ['catname','catlatinename','catcontent']
    list_display_links = ['catname','catlatinename']
    list_editable = ['catcontent']
    search_fields = ['catname']

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    fields = ['fname','latinname','fcat','fats','carbohydrates','protein','image','content','active','breakfast','lunch','dinner']
    list_display = ['fname','breakfast','lunch','dinner','active']
    list_display_links = ['fname']
    list_editable = ['breakfast','lunch','dinner','active']
    search_fields = ['fname']
    list_filter = ['fcat','breakfast','lunch','dinner','active']
    actions = [downloadpdf]

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['wname','wtimes','wimage',]
    list_display_links =  ['wname','wtimes','wimage',]
    search_fields = ['wname']

@admin.register(Activities)
class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ['aname']
    list_display_links = ['aname']
    search_fields = ['aname']

@admin.register(Theaim)
class TheaimAdmin(admin.ModelAdmin):
    list_display = ['ainame']
    list_display_links = ['ainame']
    search_fields = ['ainame']

@admin.register(Bodytype)
class BodytypeAdmin(admin.ModelAdmin):
    list_display = ['bname']
    list_display_links = ['bname']
    search_fields = ['bname']

admin.site.register(bmr_a)
admin.site.register(bmr_b)
admin.site.register(bmr_c)
admin.site.register(bmr_d)
'''
@admin.register(bmr_a)
class bmr_aAdmin(admin.ModelAdmin):
    list_display = ['bmr_a']
    list_display_links = ['bmr_a']

@admin.register(bmr_b)
class bmr_bAdmin(admin.ModelAdmin):
    list_display = ['bmr_b']
    list_display_links = ['bmr_b']

@admin.register(bmr_c)
class bmr_cAdmin(admin.ModelAdmin):
    list_display = ['bmr_c']
    list_display_links = ['bmr_c']

@admin.register(bmr_d)
class bmr_dAdmin(admin.ModelAdmin):
    list_display = ['bmr_d']
    list_display_links = ['bmr_d']
'''

@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    fields = ['tename','tlatinname','age','gender','weight','height','activities_work','aimoftrainee','bodytypet','teimage','infection','Trainee_active','tecontent','subsciption_fee','tejoined_date','start_date','end_date','workout','nitrution_breakfast','nitrution_lunch','nitrution_dinner']
    list_display = ['tename','gender','subsciption_fee','start_date','end_date','tejoined_date','bmr_value']
    list_display_links = ['tename','gender','tejoined_date']
    list_editable = ['subsciption_fee','start_date','end_date','bmr_value']
    search_fields = ['tename']
    list_filter = ['gender','tejoined_date','start_date','end_date',]
    actions = [downloadpdf]

@admin.register(Trainner)
class TrainnerAdmin(admin.ModelAdmin):
    list_display = ['tname','tlatinname','gender','joined_date']
    list_display_links = ['tname','tlatinname','joined_date']
    #list_editable = ['joined_date']
    search_fields = ['tname']
    list_filter = ['gender','joined_date']

@admin.register(Evaluchoice)
class EvaluchoiceAdmin(admin.ModelAdmin):
    list_display = ['evalgradename']
    list_display_links = ['evalgradename']
    #list_editable = ['evalgradename']
    search_fields = ['evalgradename']

@admin.register(Evaluationt)
class EvaluationtAdmin(admin.ModelAdmin):
    list_display = ['tename','eval_date','eval_points','eval_grade']
    list_display_links = ['tename','eval_date']
    list_editable = ['eval_points','eval_grade']
    search_fields = ['tename']
    list_filter = ['eval_grade','eval_points','eval_date','tename',]

@admin.register(PaymentTrainee)
class PaymentTraineeAdmin(admin.ModelAdmin):
    list_display = ['traineepay','pay_date','pay_amount']
    list_display_links = ['traineepay','pay_date']
    list_editable = ['pay_amount']
    search_fields = ['traineepay']
    list_filter = ['traineepay','pay_date']

admin.site.site_header = "لوحة التحكم"
admin.site.site_title = "عنوان الصفحة"
admin.site.index_title = "أهـــلاً بــــك بـ صفحـة لـوحـــة الــتـحـكــم"







