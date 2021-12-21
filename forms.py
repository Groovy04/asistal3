from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Email, InputRequired, Optional
from wtforms.fields.core import DateField, RadioField


#FORMS HERE
#FORMS TO BE INCLUDED - ... OTHERS?
#////////////////////////////////////////////////////////////
class Login(FlaskForm):
    name = StringField("Enter your email please..", validators=[DataRequired()])
    password = StringField("Enter your password please..", validators=[DataRequired()])
    submit = SubmitField("Login")

class Work_entry(FlaskForm):
    
    #evaluation = SelectField(label='Evaluation Result', choices=[("Pending", "Pending"), ("Accept", "Accept"), ("Reject", "Reject")])

    customer_name = StringField("Müşteri Adı", validators=[DataRequired()])
    customer_drawing = StringField("Müşteri Çizim Numarası veya İsmi", validators=[DataRequired()])
          
    offer_demand_type = SelectField(label='Teklif Talep Şekli', choices=[("Numune", "Numune"), ("DWG Çizim", "DWG Çizim"), ("PDF", "PDF")])
    mechanical_process = SelectField(label='Mekanik İşlem', choices=[("Var", "Var"), ("Yok", "Yok")])
    heat_barrier = SelectField(label='Isı Bariyer', choices=[("Var", "Var"), ("Yok", "Yok")])
    demand_for_31_certificate = SelectField(label='3.1 Sertifika Talebi', choices=[("Var", "Var"), ("Yok", "Yok")])

    profile_length = IntegerField("Profil Boyu (mm.)", validators=[InputRequired()])
    compound = SelectField(label='Alaşım', choices=[("6060", "6060"), ("6063", "6063"), ("6463", "6463"), ("6005", "6005"), ("6061", "6061"), ("6082", "6082"), ("1050", "1050"), ("1070", "1070")]) #6060, 6063, 6463, 6005, 6061, 6082, 1050,1070
    condition = SelectField(label='Kondüsyon', choices=[("T4", "T4"), ("T5", "T5"), ("T6", "T6"), ("T64", "T64"), ("T66", "T66")]) #T4, T5, T6, T64, T66  
    
    surface= SelectField(label='Yüzey', choices=[("Pres", "Pres"), ("Eloksal", "Eloksal"), ("Toz Boya", "Toz Boya")]) #Pres, Eloksal, Toz Boya
    additional_equipment = SelectField(label='Fonksiyonel Aparat', choices=[("Var", "Var"), ("Yok", "Yok")]) #Var, yok
    additional_equipment_explanation  =  TextAreaField("Fonksiyonel Aparat Açıklaması")
    visible_surface  = SelectField(label='Görünür Yüzey', choices=[("Var", "Var"), ("Yok", "Yok")]) #Var, yok - teknik resimde belirtilmeli
    elocsal_coating_thickness  = SelectField(label='Eloksal Kaplama Kalınlığı', choices=[("Yok", "Yok"), ("10μm Sınıfı", "10μm Sınıfı"), ("15 μm Sınıfı", "15 μm Sınıfı"), ("20μm Sınıfı", "20μm Sınıfı"), ("25μm Sınıfı", "25μm Sınıfı"), ("Koruyucu Eloksal(3-5μm)", "Koruyucu Eloksal(3-5μm)")]) #10 microm class, 15 microm class, 20 microm class, 25 microm class, protective(3-5) class
    hanging_print  =  SelectField(label='Askı İzi', choices=[("Var", "Var"), ("Yok", "Yok")])#Var, yok
    hanging_print_explanation  = TextAreaField("Askı İzi Açıklaması")
    order_amount_in_kg  = IntegerField("Toplam Sipariş Miktarı (kg.)", validators=[InputRequired()])
    profile_section_measure_tolerance  = SelectField(label='Profil Kesit Ölçü Toleransı', choices=[("TS EN 755-9", "TS EN 755-9"), ("TS EN 12020-2", "TS EN 12020-2")]) #TS EN 755-9, TS EN 12020-2
    sales_dept_approval  = SelectField(label='Satış Departmanı Onayı', choices=[("Onayla", "Onayla"), ("Reddet", "Reddet")])

    #choices_list ile okuyarak aşağıda otomatik olarak bir dropdown yoluna gidebilir miyiz? Özellikle şirket isimlerini seçerken bu mümkün mü? 
    # Kısa bir program ile bunu test edebilir miyiz?
    
        
    submit = SubmitField("İşin Detaylarını Kaydet")

class Technical_entry(FlaskForm):
    #BURADAN DEVAM... 
    order_no  = IntegerField("Teknik Ofis Sipariş Kodu", validators=[InputRequired()])
    circumference  = IntegerField("Çevre (mm.)", validators=[InputRequired()])
    area  = IntegerField("Alan (mm2.)", validators=[InputRequired()])
    weight_in_gr  = IntegerField("Gramaj (gr./m.)", validators=[InputRequired()])
    press  = SelectField(label='Pres', choices=[("A", "A"), ("B", "B"), ("D", "D")]) #A,B,D
    difficulty  = SelectField(label='Zorluk Derecesi', choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]) #1 En kolay ve 5 en zor şeklinde bir açıklama iyi olabilir.

    #choices_list ile okuyarak aşağıda otomatik olarak bir dropdown yoluna gidebilir miyiz? Özellikle şirket isimlerini seçerken bu mümkün mü? 
    # Kısa bir program ile bunu test edebilir miyiz?
    
    user_evaluation = SelectField(label='Teknik Departman Onayı', choices=[("Onayla", "Onayla"), ("Reddet", "Reddet")])
    user_evaluation_explanation  = TextAreaField("Teknik Departman Değerlendirme ve Yorumu", validators=[DataRequired()])
    
    submit = SubmitField("İşin Detaylarını Kaydet")

class Approval_entry(FlaskForm):
    
    user_evaluation = SelectField(label='Departman Onayı', choices=[("Onayla", "Onayla"), ("Reddet", "Reddet")])
    user_evaluation_explanation  = TextAreaField("Departman Değerlendirme ve Yorumu")
    
    submit = SubmitField("İşin Detaylarını Kaydet")



class Works_result(FlaskForm):

    #choices_list ile okuyarak aşağıda otomatik olarak bir dropdown yoluna gidebilir miyiz? Özellikle şirket isimlerini seçerken bu mümkün mü?
    evaluation = SelectField(label='Evaluation Result', choices=[("Pending", "Pending"), ("Accept", "Accept"), ("Reject", "Reject")])
    submit = SubmitField("Save Evaluation")


