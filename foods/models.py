from django.db import models
from django.db.models import F, DecimalField, Sum, CheckConstraint, Q
from django.db.models.functions import Cast
from django.db.models.expressions import RawSQL
from django.core.exceptions import ValidationError
from decimal import Decimal
# Create your models here.

class FCategory(models.Model):
    catname = models.CharField(verbose_name='اسم الصنف',max_length=100)
    catlatinename = models.CharField(verbose_name='اسم الصنف بالانكليزي',max_length=100,blank=True)
    catcontent = models.TextField(verbose_name='المحتويات و التفاصيل',null=True,blank=True)
    
    def __str__(self):
        return self.catname

    class Meta:
        verbose_name_plural = 'أصناف الأغذية'
        verbose_name  = 'أصناف الأغذية'    

class Food(models.Model):
    fname = models.CharField(verbose_name='الاسم', max_length=100)
    latinname = models.CharField(verbose_name='الاسم بالانكليزي', max_length=100, null=True, blank=True)
    fats = models.DecimalField(verbose_name='الدهون', max_digits=6, decimal_places=2, default=0.00)
    carbohydrates = models.DecimalField(verbose_name='الكربوهيدرات/النشويات', max_digits=6, decimal_places=2, default=0.00)
    protein = models.DecimalField(verbose_name='البروتينات', max_digits=6, decimal_places=2, default=0.00)
    calories= models.DecimalField(verbose_name='السعرات الحرارية', max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(verbose_name='الصورة', upload_to='foodphotos/%Y/%m/%d', blank=True)
    content = models.TextField(verbose_name='المحتويات و التفاصيل', null=True, blank=True)
    active = models.BooleanField(verbose_name='فعال', default=True)
    breakfast = models.BooleanField(verbose_name='الافطار', default=True)
    lunch = models.BooleanField(verbose_name='الغداء', default=True)
    dinner = models.BooleanField(verbose_name='العشاء', default=True)
    fcat = models.ForeignKey(FCategory, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='الصنف',)
    
    def __str__(self):
        return f'{self.fname}.......السعرات الحرارية : {self.calculate_calories()}.......الدهون : {self.fats}.......الكربوهيدرات/النشويات : {self.carbohydrates}.......البروتينات : {self.protein}'

    class Meta:
        verbose_name_plural = 'الأغذية'
        verbose_name = 'الأغذية'
        ordering = ['fname']

    def calculate_calories(self):
        return (self.fats * 9) + (self.carbohydrates * 4) + (self.protein * 4)

    def save(self, *args, **kwargs):
        self.calories = self.calculate_calories()
        super().save(*args, **kwargs)

class Workout(models.Model):
    wname = models.CharField(verbose_name='اسم الحركة',max_length=100)
    wimage = models.ImageField(verbose_name='صورة الحركة',upload_to='Traineephotos/%y/%m/%d',null=True,blank=True)
    wtimes = models.IntegerField(verbose_name='عدد الدقائق/عدد تكرار الحركة',default=12)

    def __str__(self):
        #return self.wname
        return f'{self.wname}..................عدد الدقائق/عدد تكرار الحركة : {self.wtimes} '
    class Meta:
        verbose_name_plural = 'برنامج التدريب'
        verbose_name = 'برنامج التدريب'
        ordering = ['wname']

class Activities(models.Model):
    aname = models.CharField(verbose_name='نوع العمل / نشاط',max_length=100)

    def __str__(self):
        return self.aname

    class Meta:
        verbose_name_plural = 'نشاط/عمل المتدرب'
        verbose_name = 'نشاط/عمل المتدرب'
        ordering = ['aname']

class Theaim(models.Model):
    ainame = models.CharField(verbose_name='هدف المتدرب',max_length=100)

    def __str__(self):
        return self.ainame

    class Meta:
        verbose_name_plural = 'هدف المتدرب'
        verbose_name = 'هدف المتدرب'
        ordering = ['ainame']

class Bodytype(models.Model):
    bname = models.CharField(verbose_name='طبيعة الجسم',max_length=100)

    def __str__(self):
        return self.bname
    
    class Meta:
        verbose_name_plural = 'طبيعة الجسم'
        verbose_name = 'طبيعة الجسم'    

class bmr_a(models.Model):
    bmr_a = models.FloatField(verbose_name='a',default=0.000)

    def __str__(self):
        return str(self.bmr_a)
    
    class Meta:
        verbose_name_plural = 'bmr_a'
        verbose_name = 'bmr_a'

class bmr_b(models.Model):
    bmr_b = models.FloatField(verbose_name='b',default=0.000)

    def __str__(self):
        return str(self.bmr_b)
    
    class Meta:
        verbose_name_plural = 'bmr_b'
        verbose_name = 'bmr_b'

class bmr_c(models.Model):
    bmr_c = models.FloatField(verbose_name='c',default=0.000)

    def __str__(self):
        return str(self.bmr_c)
    
    class Meta:
        verbose_name_plural = 'bmr_c'
        verbose_name = 'bmr_c'

class bmr_d(models.Model):
    bmr_d = models.FloatField(verbose_name='d',default=0.000)

    def __str__(self):
        return str(self.bmr_d)

    class Meta:
        verbose_name_plural = 'bmr_d'
        verbose_name = 'bmr_d'

class Trainee(models.Model):
    GENDER_CHOICES = (
        ("ذكر", "ذكر"),
        ("انثى", "انثى"),
    )
    tename = models.CharField(verbose_name='اسم المتدرب', max_length=100)
    tlatinname = models.CharField(verbose_name='اسم المتدرب بالانكليزي', max_length=100, null=True, blank=True)
    age = models.IntegerField(verbose_name='العمر', default=14)
    gender = models.CharField(verbose_name='الجنس', max_length=9,
                              choices=GENDER_CHOICES,
                              default="ذكر")
    weight = models.FloatField(verbose_name='الوزن', default=0.00, null=True, blank=True)
    height = models.FloatField(verbose_name='الطول', default=0.00, null=True, blank=True)
    activities_work = models.ForeignKey(Activities, on_delete=models.DO_NOTHING, blank=True, null=True,
                                        verbose_name='نشاط / العمل',)
    aimoftrainee = models.ForeignKey(Theaim, on_delete=models.DO_NOTHING, blank=True, null=True,
                                     verbose_name='الهدف',)
    bodytypet = models.ForeignKey(Bodytype, on_delete=models.DO_NOTHING, blank=True, null=True,
                                  verbose_name='طبيعة الجسم',)
    teimage = models.ImageField(verbose_name='صورة المتدرب', upload_to='Traineephotos/%y/%m/%d', null=True, blank=True)
    infection = models.ImageField(verbose_name='صورة اصابة المتدرب ان وجدت', upload_to='Traineev/%y/%m/%d',
                                   null=True, blank=True)
    Trainee_active = models.BooleanField(verbose_name='فعال', default=True, null=True, blank=True)
    tecontent = models.TextField(verbose_name='التفاصيل', null=True, blank=True)
    subsciption_fee = models.DecimalField(verbose_name='رسم الاشتراك الشهري', max_digits=6, decimal_places=2,
                                           default=0.00, null=True, blank=True)
    tejoined_date = models.DateField(verbose_name='تاريخ الاشتراك', null=True, blank=True)
    start_date = models.DateField(verbose_name='بدأ من تاريخ ', null=True, blank=True)
    end_date = models.DateField(verbose_name='الى تاريخ ', null=True, blank=True)
    workout = models.ManyToManyField(Workout, verbose_name='برنامج التدريب')
    nitrution_breakfast = models.ManyToManyField(Food, related_name='الفطور', verbose_name='الفطور')
    nitrution_lunch = models.ManyToManyField(Food, related_name='الغداء', verbose_name='الغداء')
    nitrution_dinner = models.ManyToManyField(Food, related_name='العشاء', verbose_name='العشاء')
    bmr_value = models.FloatField(verbose_name='السعرات الحرارية المطلوبة',
                                    default=0.00, null=True, blank=True)
    a = models.ForeignKey(bmr_a, on_delete=models.DO_NOTHING,
                          verbose_name=' + (bmr_a)', default=88.362)
    b = models.ForeignKey(bmr_b, on_delete=models.DO_NOTHING,
                          verbose_name='+( الوزن bmr_b X)', default=13.397)
    c = models.ForeignKey(bmr_c, on_delete=models.DO_NOTHING,
                          verbose_name='+( الارتفاع bmr_c X)', default=4.799)
    d = models.ForeignKey(bmr_d, on_delete=models.DO_NOTHING,
                          verbose_name='-( العمر bmr_d X)', default=5.677)
    total_nitrution = models.FloatField(verbose_name='مجموع السعرات', null=True,
                                           blank=True)

    def __str__(self):
        return self.tename
        #return str({self.total_nitrution})

    def total_breakvalue(self):
        return self.nitrution_breakfast.aggregate(total=Sum('calories'))['total']
    
    def total_lunchvalue(self):
        return self.nitrution_lunch.aggregate(total=Sum('calories'))['total']
    
    def total_dinnervalue(self):
        return self.nitrution_dinner.aggregate(total=Sum('calories'))['total']
    
    @property
    def bmr_calc(self):
        '''
        if self.age < 18:
            raise ValueError("BMR calculation is not applicable for individuals under 18 years old.")
        '''
        bmr = self.a.bmr_a + (self.b.bmr_b * self.weight) + (self.c.bmr_c * self.height) - (self.d.bmr_d * self.age)
        return bmr


    def save(self, *args, **kwargs):
        self.bmr_value = self.bmr_calc
        total_breakfast = self.total_breakvalue() or 0
        total_lunch = self.total_lunchvalue() or 0
        total_dinner = self.total_dinnervalue() or 0
        self.total_nitrution = float(total_breakfast) + float(total_lunch) + float(total_dinner)
        '''
        if self.total_nitrution >= self.bmr_value:
            raise ValueError("مجموع السعرات الحرارية في الأغذية أكبر من اللازم BMR")
        '''
        super().save(*args, **kwargs)

    '''
    def save(self, *args, **kwargs):
        self.bmr_value = self.bmr_calc
        self.total_nitrution = float(self.total_breakvalue()) + float(self.total_lunchvalue()) +float(self.total_dinnervalue())
        super().save(*args, **kwargs)
    '''

    '''
    def validate_calories(self):
        total_calories = self.total_breakvalue + self.total_lunchvalue + self.total_dinnervalue
        return total_calories <= self.bmr_value
    '''
    class Meta:
        verbose_name_plural = 'المتدربين'
        verbose_name = 'المتدربين'
        ordering = ['tename']
        constraints = [
        CheckConstraint(
            check=Q(total_nitrution__lt=F('bmr_value')),
            name='مجموع السعرات الحرارية في الأغذية أكبر من اللازم BMR'
        )
    ]
        '''
        constraints = [
            models.CheckConstraint(
                name="يجب أن يكون مجموع السعرات الحرارية أقل من أو يساوي BMR",
                check=(
                    Q(total_nitrution__sum=F('total_breakvalue') + F('total_lunchvalue') + F('total_dinnervalue')) &
                    Q(total_nitrution__sum__lte=1000)
                ),
            )
        ]
'''

    '''         
    def total_break(self):
        queryset = self.nitrution_breakfast.all().aggregate(
            total_break=models.Sum('calories'))
        return queryset["total_break"]
    def total_lunch(self):
        queryset1 = self.nitrution_lunch.all().aggregate(
            total_lunch=models.Sum('calories'))
        return queryset1["total_lunch"]
    def total_dinner(self):
        queryset2 = self.nitrution_dinner.all().aggregate(
            total_dinner=models.Sum('calories'))
        return queryset2["total_dinner"]
    '''

    '''         
    def total_nitrution(self):
        breakf = self.nitrution_breakfast.through.objects.all().aggregate(
            total_calories1=models.Sum('Food_calories'))     

        lunch = self.nitrution_lunch.through.objects.all().aggregate(
            total_calories2=models.Sum('Food_calories')) 

        dinner = self.nitrution_dinner.through.objects.all().aggregate(
            total_calories3=models.Sum('Food_calories'))        
        return  breakf["total_calories1"] + lunch["total_calories2"] + dinner["total_calories3"]
    '''




class Trainner(models.Model):
    GENDER_CHOICES = (
    ("ذكر", "ذكر"),
    ("انثى", "انثى"),
    )
    tname = models.CharField(verbose_name='اسم المدرب',max_length=100)
    tlatinname = models.CharField(verbose_name='اسم المدرب بالانكليزي',max_length=100,null=True,blank=True)
    age = models.IntegerField(verbose_name='العمر',default=14)
    gender = models.CharField(verbose_name='الجنس',max_length=9,
                  choices=GENDER_CHOICES,
                  default="ذكر")
    weight = models.IntegerField(verbose_name='الوزن',default=20,null=True,blank=True)
    height = models.IntegerField(verbose_name='الطول',default=150,null=True,blank=True)
    timage = models.ImageField(verbose_name='صورة المدرب',upload_to='Trainnerphotos/%y/%m/%d',null=True,blank=True)
    certificate = models.ImageField(verbose_name='صورة شهادة المدرب',upload_to='TrainnerCerti/%y/%m/%d',null=True,blank=True)
    Trainee_track = models.BooleanField(verbose_name='فعال',default=True,null=True,blank=True)
    content = models.TextField(verbose_name='التفاصيل',null=True,blank=True)
    salary = models.DecimalField(verbose_name='الراتب',max_digits=6,decimal_places=2,default=0.00,null=True,blank=True)
    joined_date = models.DateField(verbose_name='تاريخ مباشرة',null=True,blank=True)

    def __str__(self):
        return self.tname

    class Meta:
        verbose_name_plural = 'المدربين'
        verbose_name = 'المدربين'
        ordering = ['tname']
 
class Evaluchoice(models.Model):
    id = models.BigAutoField(primary_key=True)
    evalgradename = models.CharField(verbose_name='درجة التقييم',max_length=100)

    def __str__(self):
        return self.evalgradename

    class Meta:
        verbose_name_plural = 'درجات التقييم'
        verbose_name = 'درجات التقييم'
        ordering = ['evalgradename']

class Evaluationt(models.Model):
    tename = models.ForeignKey(Trainee, on_delete = models.DO_NOTHING , blank = True , null = True,verbose_name='اسم المتدرب',primary_key=False)
    eval_date = models.DateField(verbose_name='تاريخ التقييم',null=True,blank=True,primary_key=False)
    eval_points = models.IntegerField(verbose_name='نقاط التقييم',default=14,primary_key=False)
    eval_grade = models.ForeignKey(Evaluchoice, on_delete = models.DO_NOTHING , blank = True , null = True,verbose_name='درجة التقييم',primary_key=False)
    
    class Meta:
        verbose_name_plural = 'التقييم'
        verbose_name = 'التقييم'
        ordering = ['tename']

class PaymentTrainee(models.Model):
    traineepay = models.ForeignKey(Trainee, on_delete = models.DO_NOTHING , blank = True , null = True,verbose_name='المتدرب',)
    pay_date = models.DateField(verbose_name='تاريخ الدفعة',null=True,blank=True)
    pay_amount = models.DecimalField(verbose_name='مقدار الدفعة',max_digits=6,decimal_places=2,default=0.00)
    
    class Meta:
        verbose_name_plural = 'المدفوعات'
        verbose_name = 'المدفوعات'
        ordering = ['traineepay']

        