from os import error
from flask import Flask, render_template, flash, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms import validators
from wtforms.validators import DataRequired, Email, ValidationError, InputRequired

from datetime import datetime, date

from flask_login import UserMixin
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, or_
from forms import Login, Works_result, Work_entry, Technical_entry, Approval_entry

import pandas

app = Flask(__name__)

bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://tansubaktiran:Avz9p9&9Dgsu_099@193.111.73.99/tansubaktiran"
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://sql11460522:ycvXfE6mjZ@sql11.freemysqlhosting.net/sql11460522"

#Secret key
app.config['SECRET_KEY'] = "MYTESTKEY"
#Initialize the adatabase
db = SQLAlchemy(app)

#Setting up user login parts
login_manager = LoginManager(app)
login_manager.login_view = 'login' #Name of the route in charge of logging in
login_manager.login_message_category = 'info'


#USER LOGIN FUNCTION FOR LOADING ACTIVE USER?
@login_manager.user_loader
def load_user(id):
    return Staff_db.query.get(int(id)) #DB table name to be updated!!!! ////////////

#TIME NOW
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")


#MODELS
class Staff_db(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    name_db = db.Column(db.String(200))
    email_db = db.Column(db.String(200))
    password_db = db.Column(db.String(120))
    role_db = db.Column(db.String(120))
        
    def __repr__(self):
        #Aşağıdaki gibi (global active_user_id gerek olmadan bir current_user üzerinden loggedin kullanıcıyı takip edebilir miyiz? 21.12.2021
        #return self.id
        #return '<Id %r>' % self.id
        return '<Name %r>' % self.name_db

class Works_db(db.Model): #MT Planned db - 
    id = db.Column(db.Integer, primary_key=True)
    asistal_id_db = db.Column(db.String(20))
    version_db = db.Column(db.Integer)
    date_added_db = db.Column(db.DateTime, default=datetime.utcnow)
    sales_rep_db = db.Column(db.String(50))
    customer_name_db = db.Column(db.String(50))
    customer_drawing_db = db.Column(db.String(50))
    offer_demand_type_db = db.Column(db.String(20))
    mechanical_process_db = db.Column(db.String(20))
    heat_barrier_db = db.Column(db.String(20))
    demand_for_31_certificate_db = db.Column(db.String(20))
    profile_length_db = db.Column(db.Integer, default=0)
    compound_db = db.Column(db.String(10)) #6060, 6063, 6463, 6005, 6061, 6082, 1050,1070
    condition_db = db.Column(db.String(10)) #T4, T5, T6, T64, T66
    surface_db = db.Column(db.String(10)) #Pres, Eloksal, Toz Boya
    additional_equipment_db = db.Column(db.String(10)) #Var, yok
    additional_equipment_explanation_db = db.Column(db.String(300)) #String
    visible_surface_db = db.Column(db.String(10)) #Var, yok - teknik resimde belirtilmeli
    elocsal_coating_thickness_db = db.Column(db.String(10)) #10 microm class, 15 microm class, 20 microm class, 25 microm class, protective(3-5) class
    hanging_print_db = db.Column(db.String(10)) #Var, yok
    hanging_print_explanation_db = db.Column(db.String(300))
    order_amount_in_kg_db = db.Column(db.Integer, default=0)
    profile_section_measure_tolerance_db = db.Column(db.String(30)) #TS EN 755-9, TS EN 12020-2
    order_no_db = db.Column(db.Integer, default=0) #TB String??? or Integer???
    circumference_db = db.Column(db.Integer, default=0)
    area_db = db.Column(db.Integer, default=0)
    weight_in_gr_db = db.Column(db.Integer, default=0)
    press_db = db.Column(db.String(10)) #A,B,D
    difficulty_db = db.Column(db.String(10))

    user1_evaluation_db = db.Column(db.String(20))
    user2_evaluation_db = db.Column(db.String(20))
    user3_evaluation_db = db.Column(db.String(20))
    user4_evaluation_db = db.Column(db.String(20))
    user5_evaluation_db = db.Column(db.String(20))
    user6_evaluation_db = db.Column(db.String(20))
    user7_evaluation_db = db.Column(db.String(20))
    user8_evaluation_db = db.Column(db.String(20))
    user9_evaluation_db = db.Column(db.String(20))
    user10_evaluation_db = db.Column(db.String(20))

    user1_evaluation_explanation_db = db.Column(db.String(400))
    user2_evaluation_explanation_db = db.Column(db.String(400))
    user3_evaluation_explanation_db = db.Column(db.String(400))
    user4_evaluation_explanation_db = db.Column(db.String(400))
    user5_evaluation_explanation_db = db.Column(db.String(400))
    user6_evaluation_explanation_db = db.Column(db.String(400))
    user7_evaluation_explanation_db = db.Column(db.String(400))
    user8_evaluation_explanation_db = db.Column(db.String(400))
    user9_evaluation_explanation_db = db.Column(db.String(400))
    user10_evaluation_explanation_db = db.Column(db.String(400))

    #Her user kendi değerlendirmesini yaptığında log tarih atacak. Buna sonra bakalım.
    user1_evaluation_date_db = db.Column(db.DateTime, default=dt_string)
    user2_evaluation_date_db= db.Column(db.DateTime, default=dt_string)
    user3_evaluation_date_db = db.Column(db.DateTime, default=datetime.utcnow)
    user4_evaluation_date_db = db.Column(db.DateTime, default=datetime.utcnow)
    user5_evaluation_date_db = db.Column(db.DateTime, default=datetime.utcnow)
    user6_evaluation_date_db = db.Column(db.DateTime, default=datetime.utcnow)
    user7_evaluation_date_db = db.Column(db.DateTime, default=datetime.utcnow)
    user8_evaluation_date_db = db.Column(db.DateTime, default=datetime.utcnow)
    user9_evaluation_date_db = db.Column(db.DateTime, default=datetime.utcnow)
    user10_evaluation_date_db = db.Column(db.DateTime, default=datetime.utcnow)
    
        
    def __repr__(self):
        return '<Entry No: %r>' % self.id



@app.route('/')
@app.route('/index')
def index():
    name="TEST"
    number = 10
    return  render_template("index.html", name=name, number=number)

active_user= None #Burada kaldık. active_user'in rolünü tespit edip ona göre o user için olan Pending işleri göstermesini sağladık. 
#Notu sonrasındaki çalışmalar için silmedim.

#//////////////////////NEW FUNCTION
@app.route('/new_work_entry', methods=["GET", "POST"])
@login_required
def new_work_entry(): #Adding a new work to database by sales team
    
    

    form = Work_entry()

    # active_user_id tespiti ile login olmuş kullanıcıyı buluyoruz. Oradan da e-mailine de ulaşarak kaydı kimin yaptığını otomatik olarak sisteme atıyoruz.
    active_user = Staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    
    print(user_email, user_name, user_role, "Just passed from new_work_entry... beginning")
    
    if user_role == "user1":

        all_works = Works_db.query.order_by(Works_db.date_added_db).all()    
        last_work = Works_db.query.order_by(Works_db.id.desc()).first() #For getting the id of last record to be used in the Asistal Reference Code
        #db_session.query(Courses).order_by(Courses.courses_now.id.desc()).first() #Example code for getting the last record in the base.
    
        #Database'e ilk kayıt yapıldığında en son kaydı arayarak onun referansına öre ID veriyordu. Ancak hiç kayıt yok ise hata veriyordu. 
        # Bunun önüne geçebilmek için None bulursa manuel olarak Asistal referansı oluştursun diye bu if statement kurguladık.
        if last_work == None:
            new_asistal_ref = "AST_1"
        else:
            id_of_last_work = last_work.id
            print("ID of last work", id_of_last_work)
            id_of_next_work = id_of_last_work+1
            new_asistal_ref = "AST_" + str(id_of_next_work)
    
        #Validation of our form - NORMALDE YENİ İŞ KAYIT EKRANINA GİRİŞTE SORUN YAŞAMAZ İKEN, ŞU ANDA LİNK BİZİ INDEX SAYFASINA GÖTÜRÜYOR. 14.12.21'DE BAKALIM.
        if request.method == "POST":
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            if form.validate_on_submit():
                print("form vaidate???")
                new_work = Works_db(  
                        
                version_db = 1,
                sales_rep_db =user_email,     #Otomatik olarak gelmeli. Kontrol edilecek.
                asistal_id_db = new_asistal_ref, #new_asistal_ref,
                customer_name_db =form.customer_name.data,
                customer_drawing_db =form.customer_drawing.data,
                offer_demand_type_db =form.offer_demand_type.data,
                mechanical_process_db =form.mechanical_process.data,
                heat_barrier_db =form.heat_barrier.data,
                demand_for_31_certificate_db =form.demand_for_31_certificate.data,
                profile_length_db =form.profile_length.data,
                compound_db =form.compound.data,
                condition_db =form.condition.data,
                surface_db =form.surface.data,
                additional_equipment_db =form.additional_equipment.data,
                additional_equipment_explanation_db =form.additional_equipment_explanation.data,
                visible_surface_db =form.visible_surface.data,
                elocsal_coating_thickness_db =form.elocsal_coating_thickness.data,
                hanging_print_db =form.hanging_print.data,
                hanging_print_explanation_db =form.hanging_print_explanation.data,
                order_amount_in_kg_db =form.order_amount_in_kg.data,
                profile_section_measure_tolerance_db =form.profile_section_measure_tolerance.data,
                
                user1_evaluation_db = form.sales_dept_approval.data, #Satış
                user2_evaluation_db = "Beklemede", #Teknik ofis
                user3_evaluation_db = "Beklemede", #Ekstrüzyon
                user4_evaluation_db = "Beklemede", #Eloksal
                user5_evaluation_db = "Beklemede", #Boyahane
                user6_evaluation_db = "Beklemede", #Mekanik işlem
                user7_evaluation_db = "Beklemede", #Isı bariyer
                user8_evaluation_db = "Beklemede",
                user9_evaluation_db = "Beklemede",
                user10_evaluation_db = "Beklemede",
                user1_evaluation_date_db = dt_string     )
                
                db.session.add(new_work)
                db.session.commit()
                
                last_work = Works_db.query.order_by(Works_db.id.desc()).first()
                if form.mechanical_process.data=="Yok":
                    last_work.user6_evaluation_db = "Onayla"
                if form.heat_barrier.data=="Yok":
                    last_work.user7_evaluation_db = "Onayla"
                if form.surface.data=="Pres":
                    last_work.user4_evaluation_db = "Onayla"
                    last_work.user5_evaluation_db = "Onayla"
                if form.surface.data=="Eloksal":
                    last_work.user5_evaluation_db = "Onayla"
                if form.surface.data=="Toz Boya":
                    last_work.user4_evaluation_db = "Onayla"
                #Diğerleri

                db.session.commit()

                flash("Yeni çalışma başarılı biçimde kaydedildi! Teşekkürler!", "success")
                return render_template("index.html")
            else:
                flash("İşin kaydında bir sorun oluştu. Lütfen Profil Boyu ve Toplam Sipariş Miktarı kısımlarının rakam olduğuna emin olunuz. Problem çözülmüyor ise IT Yöneticisi ile temasa geçiniz.", 'error')
    else:   
        flash("Yeni iş girişi ekranı sadece satış personeli erişimine açıktır. İyi çalışmalar dileriz.", 'error')
        return render_template("index.html")
    #User.query.order_by(User.popularity.desc(), User.date_created.desc()).limit(10).all()
    all_works = Works_db.query.order_by(Works_db.date_added_db).all()
    return render_template("new_work_entry.html", form=form, all_works = all_works)

#//////////////////////NEW FUNCTION


#//////////////////////NEW FUNCTION
@app.route('/view_pending_works', methods=["GET", "POST"])
@login_required
def view_pending_works(): #Viewing pending works for relevant department or staff or role.

    global pending_works
    pending_works = None
    if pending_works == None:
        print("Heyyo")
    # active_user_id tespiti ile login olmuş kullanıcıyı buluyoruz. Oradan da e-mailine de ulaşarak kaydı kimin yaptığını otomatik olarak sisteme atıyoruz.
    #TRY EXCEPT
    try:
        active_user = Staff_db.query.filter_by(id=active_user_id).first()
        flash("Try Except - Servera active_user için bağlanırken sorun oluşMADI.", "success")
    except:
        flash("Try Except - Servera active_user için bağlanırken sorun oluştu.", "success")
    
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    print(user_email, user_name, user_role, "Just passed here...")

    if user_role=="user1":
        #Rejected için pending_works oluşturamadık. Oluşturduk. 17.12.2021
        #Aşağıda User1'in de ilk filtreye dahil edilmesinin sebebi, olur da o iş için yeni versiyon oluşturulursa, yeni versiyon kaydedildiğinde, orijinal işi 
        # User1 bekleyen işler listesinden çıkarmasını istedik. Eğer gerekli olursa User1'in göreceği şekilde, yeni versiyonu oluşturulduğu için 
        # iptal edilmiş işler listesi de ayrı yerde gösterilebilir.

        try:
            pending_works = Works_db.query.filter(Works_db.user1_evaluation_db=="Onayla", Works_db.user2_evaluation_db!="Beklemede", Works_db.user3_evaluation_db!="Beklemede", Works_db.user4_evaluation_db!="Beklemede", Works_db.user5_evaluation_db!="Beklemede", 
        Works_db.user6_evaluation_db!="Beklemede", Works_db.user7_evaluation_db!="Beklemede", Works_db.user8_evaluation_db!="Beklemede", Works_db.user9_evaluation_db!="Beklemede", Works_db.user10_evaluation_db!="Beklemede")
            flash("Try Except - Servera pending_works için bağlanırken sorun oluşMADI.", "success")
        #if not (pending_works): #Şevket yazdı.
            #raise db.error #Şevket yazdı.
        except :
            flash("Servera pending_works için bağlanırken sorun oluştu.", "success")

        
        
        print("Passed from internal pending works ///")
        rejected_works = Works_db.query.filter(or_(Works_db.user2_evaluation_db=="Reddet", Works_db.user3_evaluation_db=="Reddet", Works_db.user4_evaluation_db=="Reddet", Works_db.user5_evaluation_db=="Reddet", 
        Works_db.user6_evaluation_db=="Reddet", Works_db.user7_evaluation_db=="Reddet", Works_db.user8_evaluation_db=="Reddet", Works_db.user9_evaluation_db=="Reddet", Works_db.user10_evaluation_db=="Reddet"))
        
        return render_template("view_pending_works.html", pending_works = pending_works, rejected_works = rejected_works, user_name = user_name, user_role=user_role)
    else:
        filterdict = {
            "user1" : Works_db.user1_evaluation_db,
            "user2" : Works_db.user2_evaluation_db,
            "user3" : Works_db.user3_evaluation_db,
            "user4" : Works_db.user4_evaluation_db,
            "user5" : Works_db.user5_evaluation_db,
            "user6" : Works_db.user6_evaluation_db,
            "user7" : Works_db.user7_evaluation_db,
            "user8" : Works_db.user8_evaluation_db,
            "user9" : Works_db.user9_evaluation_db,
            "user10" : Works_db.user10_evaluation_db
        }
        filterlist = list(filterdict)
        role_position_index = filterlist.index(user_role)
        role_position_index = role_position_index-1
        previous_role = filterlist[role_position_index]
        #User1 seviyesinde de Pending durumu oluşsaydı, aşağıdaki gibi bir if döngüsü ile devam etmek gerekecekti. Burada user1 satış pozisyonu olduğu için 
        # ve sürecin de tetikleyicisi olduğu için, bu ilk if döngüsüne gerek olmayacak gibi.
        #if user_role=="user1":
        #    pending_records = Works_db.query.filter(Works_db.user1_evaluation_db=="Pending")
        
        pending_works = Works_db.query.filter(filterdict[user_role]=="Beklemede", filterdict[previous_role]=="Onayla")
        return render_template("view_pending_works.html", pending_works = pending_works, user_name = user_name)

#//////////////////////NEW FUNCTION

#//////////////////////NEW FUNCTION
@app.route('/view_in_detail/<int:id>', methods=["GET", "POST"])
@login_required
def view_in_detail(id): #Viewing pending works for relevant department or staff or role.
    active_user = Staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    work_to_show = Works_db.query.get_or_404(id)

    #Aşağıdaki ilk deneme çalışıyor...şimdi formlar, yeni html sayfaları ile get/post işleyişini deneyeceğiz. 14.12.21
    if request.method == "POST":
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        if user_role=="user2":
            form = Technical_entry()
            work_to_show.order_no_db = form.order_no.data
            work_to_show.circumference_db = form.circumference.data
            work_to_show.area_db = form.area.data
            work_to_show.weight_in_gr_db = form.weight_in_gr.data
            work_to_show.press_db = form.press.data
            work_to_show.difficulty_db = form.difficulty.data
            work_to_show.user2_evaluation_db = form.user_evaluation.data
            work_to_show.user2_evaluation_explanation_db = form.user_evaluation_explanation.data
                                  
            work_to_show.user2_evaluation_date_db = dt_string
            
            #BURADAN DEVAM EDELİM.
            
                        
            db.session.commit() #Unutma
            #Try except eklenecek. Kayıt sonrası ONAY Flash + yeni bir sayfaya yönlendirilecek. Unutma. 
            # Teknik verilerin üzerinde ön bilgilere yer verilecek. Teknik sayfanın altında onay/reddet seçenekleri eklenecek.
            return render_template("technical_entry.html", form=form, work_to_show=work_to_show)
        else:
            form = Approval_entry()
            work_to_show = Works_db.query.get_or_404(id)
            evaluation_dict = {
                "user1" : work_to_show.user1_evaluation_db,
                "user2" : work_to_show.user2_evaluation_db,
                "user3" : work_to_show.user3_evaluation_db,
                "user4" : work_to_show.user4_evaluation_db,
                "user5" : work_to_show.user5_evaluation_db,
                "user6" : work_to_show.user6_evaluation_db,
                "user7" : work_to_show.user7_evaluation_db,
                "user8" : work_to_show.user8_evaluation_db,
                "user9" : work_to_show.user9_evaluation_db,
                "user10" : work_to_show.user10_evaluation_db
            }
            evaluation_explanation_dict = {
                "user1" : work_to_show.user1_evaluation_explanation_db,
                "user2" : work_to_show.user2_evaluation_explanation_db,
                "user3" : work_to_show.user3_evaluation_explanation_db,
                "user4" : work_to_show.user4_evaluation_explanation_db,
                "user5" : work_to_show.user5_evaluation_explanation_db,
                "user6" : work_to_show.user6_evaluation_explanation_db,
                "user7" : work_to_show.user7_evaluation_explanation_db,
                "user8" : work_to_show.user8_evaluation_explanation_db,
                "user9" : work_to_show.user9_evaluation_explanation_db,
                "user10" : work_to_show.user10_evaluation_explanation_db
            } #Bu dictionaryleri Stackoverflow yanıtına göre silebiliriz. Dictionary ile ilerlemenin bir yolunu bulmalı. Bu şekilde kod kalabalık görünüyor.
      
            #BURAYI DICTIONARY ILE COZEBILIR MIYIZ? YUKARIDAKI ORNEKLERDE OLDUGU GIBI?
            #YUKARIDAKILERI "" ICINE ALSAK ÇÖZÜM OLABİLİR Mİ? - BURADA KALDIK - 14.12.21 - STACKOVERFLOW'A SORALIM.
            #evaluation_dict[user_role] = form.user_evaluation.data
            #evaluation_explanation_dict[user_role] = form.user_evaluation_explanation.data
            work_to_show = Works_db.query.get_or_404(id)
            if user_role=="user3":
                work_to_show.user3_evaluation_db = form.user_evaluation.data
                work_to_show.user3_evaluation_explanation_db = form.user_evaluation_explanation.data
                work_to_show.user3_evaluation_date_db = dt_string
            elif user_role=="user4":
                work_to_show.user4_evaluation_db = form.user_evaluation.data
                work_to_show.user4_evaluation_explanation_db = form.user_evaluation_explanation.data
                work_to_show.user4_evaluation_date_db = dt_string
            elif user_role=="user5":
                work_to_show.user5_evaluation_db = form.user_evaluation.data
                work_to_show.user5_evaluation_explanation_db = form.user_evaluation_explanation.data
                work_to_show.user5_evaluation_date_db = dt_string
            elif user_role=="user6":
                work_to_show.user6_evaluation_db = form.user_evaluation.data
                work_to_show.user6_evaluation_explanation_db = form.user_evaluation_explanation.data
                work_to_show.user6_evaluation_date_db = dt_string
            elif user_role=="user7":
                work_to_show.user7_evaluation_db = form.user_evaluation.data
                work_to_show.user7_evaluation_explanation_db = form.user_evaluation_explanation.data
                work_to_show.user7_evaluation_date_db = dt_string
            elif user_role=="user8":
                work_to_show.user8_evaluation_db = form.user_evaluation.data
                work_to_show.user8_evaluation_explanation_db = form.user_evaluation_explanation.data
                work_to_show.user8_evaluation_date_db = dt_string
            elif user_role=="user9":
                work_to_show.user9_evaluation_db = form.user_evaluation.data
                work_to_show.user9_evaluation_explanation_db = form.user_evaluation_explanation.data
                work_to_show.user9_evaluation_date_db = dt_string
            elif user_role=="user10":
                work_to_show.user10_evaluation_db = form.user_evaluation.data
                work_to_show.user10_evaluation_explanation_db = form.user_evaluation_explanation.data
                work_to_show.user10_evaluation_date_db = dt_string
            
            
            db.session.commit()
            
            return render_template("approval_entry.html", form=form, work_to_show = work_to_show, user_role = user_role)

    if request.method == "GET":
        work_to_show = Works_db.query.get_or_404(id)
        if user_role=="user2":
            form = Technical_entry()
            return render_template("technical_entry.html", form=form, work_to_show=work_to_show, active_user=active_user, user_role = user_role)
        else:
            form = Approval_entry()
            return render_template("approval_entry.html", form=form, work_to_show=work_to_show, active_user=active_user, user_role = user_role)


#///// VIEW ALL WORKS //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/view_all_works', methods=["GET", "POST"])
@login_required
def view_all_works(): #Viewing pending works for relevant department or staff or role.
    active_user = Staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    all_works = Works_db.query.order_by(Works_db.id).all()
    return render_template("view_all_works.html", all_works=all_works, user_name = user_name, user_role=user_role)

#///// VIEW ALL WORKS //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#///// ADD NEW WORK VERSION //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/add_new_work_version/<int:id>', methods=["GET", "POST"])
@login_required
def add_new_work_version(id): #Viewing pending works for relevant department or staff or role.
    active_user = Staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    work_to_add_version = Works_db.query.get_or_404(id)
    form = Work_entry()
    
    if request.method == 'GET':
        
        form.customer_name.data = work_to_add_version.customer_name_db
        form.customer_drawing.data = work_to_add_version.customer_drawing_db
        form.offer_demand_type.data = work_to_add_version.offer_demand_type_db
        form.mechanical_process.data = work_to_add_version.mechanical_process_db
        form.heat_barrier.data = work_to_add_version.heat_barrier_db
        form.demand_for_31_certificate.data = work_to_add_version.demand_for_31_certificate_db
        form.profile_length.data = work_to_add_version.profile_length_db
        form.compound.data = work_to_add_version.compound_db
        form.condition.data = work_to_add_version.condition_db
        form.surface.data = work_to_add_version.surface_db
        form.additional_equipment.data = work_to_add_version.additional_equipment_db
        form.additional_equipment_explanation.data = work_to_add_version.additional_equipment_explanation_db
        form.visible_surface.data = work_to_add_version.visible_surface_db
        form.elocsal_coating_thickness.data = work_to_add_version.elocsal_coating_thickness_db
        form.hanging_print.data = work_to_add_version.hanging_print_db
        form.hanging_print_explanation.data = work_to_add_version.hanging_print_explanation_db
        form.order_amount_in_kg.data = work_to_add_version.order_amount_in_kg_db
        form.profile_section_measure_tolerance.data = work_to_add_version.profile_section_measure_tolerance_db
    
        return render_template("add_new_work_version.html", form=form) 

    if request.method == 'POST':
        #YENİ VERSİYONU YERİNE KAYDEDECEĞİZ ŞİMDİ.. HADİ BAKALIM... (Bu işlem 17.12.21'de tamamlandı)
        #Şimdi sırada, eski versiyonu işlemden çıkartmak için bir akış/yöntem bulmak var. 19.12.21
        print("We still do have the id of original/previous version of the work; which is: ", id)
        old_work_version_to_cancel=work_to_add_version = Works_db.query.get_or_404(id)
        current_asistal_id = work_to_add_version.asistal_id_db
        old_version_number=work_to_add_version.version_db
        new_version_number=old_version_number+1
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        current_sales_rep = work_to_add_version.sales_rep_db
        if form.validate_on_submit():
            print("form vaidate???")
            modified_work = Works_db(  
                    
            version_db = new_version_number,
            sales_rep_db =current_sales_rep,     #Otomatik olarak gelmeli. Kontrol edilecek.
            asistal_id_db = current_asistal_id, #new_asistal_ref,
            customer_name_db =form.customer_name.data,
            customer_drawing_db =form.customer_drawing.data,
            offer_demand_type_db =form.offer_demand_type.data,
            mechanical_process_db =form.mechanical_process.data,
            heat_barrier_db =form.heat_barrier.data,
            demand_for_31_certificate_db =form.demand_for_31_certificate.data,
            profile_length_db =form.profile_length.data,
            compound_db =form.compound.data,
            condition_db =form.condition.data,
            surface_db =form.surface.data,
            additional_equipment_db =form.additional_equipment.data,
            additional_equipment_explanation_db =form.additional_equipment_explanation.data,
            visible_surface_db =form.visible_surface.data,
            elocsal_coating_thickness_db =form.elocsal_coating_thickness.data,
            hanging_print_db =form.hanging_print.data,
            hanging_print_explanation_db =form.hanging_print_explanation.data,
            order_amount_in_kg_db =form.order_amount_in_kg.data,
            profile_section_measure_tolerance_db =form.profile_section_measure_tolerance.data,
            
            user1_evaluation_db = form.sales_dept_approval.data, #Satış
            user2_evaluation_db = "Beklemede", #Teknik ofis
            user3_evaluation_db = "Beklemede", #Ekstrüzyon
            user4_evaluation_db = "Beklemede", #Eloksal
            user5_evaluation_db = "Beklemede", #Boyahane
            user6_evaluation_db = "Beklemede", #Mekanik işlem
            user7_evaluation_db = "Beklemede", #Isı bariyer
            user8_evaluation_db = "Beklemede",
            user9_evaluation_db = "Beklemede",
            user10_evaluation_db = "Beklemede",
            user1_evaluation_date_db = dt_string     )
            
            db.session.add(modified_work)
            db.session.commit()
            
            last_work = Works_db.query.order_by(Works_db.id.desc()).first()
            if form.mechanical_process.data=="Yok":
                last_work.user6_evaluation_db = "Onayla"
            if form.heat_barrier.data=="Yok":
                last_work.user7_evaluation_db = "Onayla"
            if form.surface.data=="Pres":
                last_work.user4_evaluation_db = "Onayla"
                last_work.user5_evaluation_db = "Onayla"
            if form.surface.data=="Eloksal":
                last_work.user5_evaluation_db = "Onayla"
            if form.surface.data=="Toz Boya":
                last_work.user4_evaluation_db = "Onayla"
            #Diğerleri

            db.session.commit()
            #Hey Tansu!
            #User1 herhangi bir işe yeni bir versiyon oluşturursa, otomatik olarak eski versiyona Red kaydetmeli ve açıklamasını da buna göre otomatik olarak yapmalı.
            old_work_version_to_cancel.user1_evaluation_db="Reddet"
            old_work_version_to_cancel.user1_evaluation_explanation_db="Yeni versiyon girişinden ötürü iptal edilmiştir."
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            old_work_version_to_cancel.user1_evaluation_date_db=dt_string
            db.session.commit()
            
            flash("Yeni çalışma başarılı biçimde kaydedildi! Teşekkürler!", "success")
            all_works = Works_db.query.order_by(Works_db.date_added_db).all()
            return render_template("add_new_work_version.html", form=form, all_works = all_works) # - HTML kısmı kaldı

        else:
            flash("İşin kaydında bir sorun oluştu. Lütfen IT Yöneticisi ile temasa geçiniz.", 'error')
            return render_template("add_new_work_version.html")
    

#////
    return render_template("index.html")



#///// ADD NEW WORK VERSION //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#//////////////////////////////// gösterge panosu

@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard(): #Viewing pending works for relevant department or staff or role.
    active_user = Staff_db.query.filter_by(id=active_user_id).first()
    user_email = active_user.email_db
    user_name = active_user.name_db
    user_role = active_user.role_db
    

    if user_role=="user20":
        print("Hello user 20")
        #all_works = Works_db.query.order_by(Works_db.date_added_db).all()
        #print(type(all_works))
        #print(all_works[0].customer_name_db)
        
        engine = create_engine("mysql+pymysql://tansubaktiran:Avz9p9&9Dgsu_099@193.111.73.99/tansubaktiran")
        #engine = create_engine("mysql+pymysql://sql11460522:ycvXfE6mjZ@sql11.freemysqlhosting.net/sql11460522")
            
        
        dbconnection = engine.connect()

        works_data = pandas.read_sql("select * from works_db", dbconnection)
        print(works_data.head())
        #print(works_data.describe())
        total_length = works_data.shape[0]
        """total_pres =
        total_paint =
        total_eloksal =
        total_weight_offered =
        accept_ratio =
        total_kg_offered ="""

        print(total_length)
        
        return render_template("index.html")
    else:
        flash("Gösterge ekranı sadece yönetici personel erişimine açıktır. İyi çalışmalar dileriz.", 'error')
        return render_template("index.html")
    


#//////////////////////////////// gösterge panosu
@app.route("/login", methods=['GET', 'POST'])
def login():
    
    name=None
    
    global active_user_id
    active_user_id = None

    if current_user.is_authenticated:
        print("User is ALREADY LOGGED IN")
        return redirect(url_for('index'))
    form = Login()
    if form.validate_on_submit():
        #????????????????????????????????? test password for oguz@oguz.com - 159oguz78
        # tansu@tansu.com - 1234 / derya@derya.com - 1234
                
        print("Form validated")
        user = Staff_db.query.filter_by(name_db=form.name.data).first()
        #Eğer şifre doğru olsa bile aranan user'in emaili yanlış ise hata veriyordu çünkü user objesini bulamadığı için 
        # o userın emailini de bulamıyordu. passsword_db attribute yok diyordu. Bu şekilde if kontrolü ile çalışıyor.
        if user:
            password = user.password_db
            print("passcheck hashed", password)
            #password_check = form.password.data
            password_check = bcrypt.check_password_hash(password, form.password.data)
            print(password_check)
            #print("passcheck", password_check)
        
        if user and password_check:
            print("/////////Found this user and his password is correct!!!////// and hashing technique is used!! ;)")
            login_user(user)            
            print("User seems to be logged in beybisi..")
            flash('Login Successful. Have a nice day!!', 'success')
            active_user_id = int(user.id)
            print("////////////",active_user_id, type(active_user_id))
            print(current_user)
            #render_template('index.html', title='Login', form=form, name=name, active_user_id = active_user_id)
            return redirect(url_for('index'))
            
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
    return render_template('login.html', title='Login', form=form, name=name)

@app.route("/logout")
def logout():
    logout_user()
    print("The user should have been LOGGED OUT NOW!!!")
    flash('Logout successful. Thank you for using the system', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
