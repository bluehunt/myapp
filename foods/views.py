from django.shortcuts import render
from .models import Food, Trainee
from PIL import Image, ImageDraw, ImageFont
import os
from bidi.algorithm import get_display
import arabic_reshaper

# Create your views here.

def food(request):
    return render(request, 'foods/food.html')

def foods(request):
    # استعلام قاعدة البيانات لاستخراج بيانات Trainee
    trainees = Trainee.objects.all()

    for trainee in trainees:
        # تنسيق البيانات للتقرير
        report_data = ""
        report_data += f"اسم المتدرب: {trainee.tename}\n"
        report_data += f"العمر: {trainee.age}\n"
        # إضافة المزيد من المعلومات هنا حسب الحاجة

        # إعادة تشكيل النص العربي
        reshaped_text = arabic_reshaper.reshape(report_data)
        arabic_text = get_display(reshaped_text)

        # إنشاء صورة فارغة
        image = Image.new("RGB", (800, 600), color="white")
        draw = ImageDraw.Draw(image)

        # تنسيق النص
        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'arial.ttf')
        font = ImageFont.truetype(font_path, 24)  # اختيار خط الكتابة وحجم الخط

        # ألوان النص والخلفية
        text_color = (0, 0, 0)  # اللون الأسود
        background_color = (255, 255, 255)  # اللون الأبيض

        # حساب عرض وارتفاع النص بواسطة ImageFont
        left, top, right, bottom = font.getbbox(arabic_text)
        text_width = right - left - 100
        text_height = bottom - top -100 
        #text_width, text_height = font.getbbox(arabic_text)

        # تحديد موقع النص
        x = 800 - text_width   # يبدأ من اليمين مع هامش من اليمين
        y = 10

        # رسم النص على الصورة
        draw.text((x, y), arabic_text, font=font, fill=text_color)

        # تحديد مسار حفظ الصورة
        image_path = f"media/trainee_reports/trainee_report_{trainee.id}.png"
        directory = os.path.dirname(os.path.abspath(image_path))
        if not os.path.exists(directory):
            os.makedirs(directory)

        # حفظ الصورة كملف
        image.save(image_path)

    # عرض البيانات على الصفحة
    return render(request, 'foods/foods.html', {'fo': Food.objects.all()})
