
from datetime import date
import datetime
from logging import exception
from os import close
from flask import Flask, redirect,url_for,request,render_template,session,flash
from pyasn1_modules.rfc2459 import Time
import pyrebase
import matplotlib.pyplot as plt
import numpy as np
import model

import csv

app=Flask(__name__)
app.secret_key='Rudy'


firebaseconfig={
    'apiKey': "AIzaSyA3FLZXYndXaAkOUteApp5rgMwgdDmwa5M",
    'authDomain': "helpdesk2-c58b5.firebaseapp.com",
    'databaseURL':"https://helpdesk2-c58b5-default-rtdb.firebaseio.com/",
    'projectId': "helpdesk2-c58b5",
    'storageBucket': "helpdesk2-c58b5.appspot.com",
    'messagingSenderId': "915657124265",
    'appId': "1:771226759182:web:702b81ae207c5f61164c5f"
    # 'measurementId': "G-XXEXL7TEVW"
}
firebase=pyrebase.initialize_app(firebaseconfig)
db=firebase.database()
opencount=len(db.child("Tickets").order_by_child("STATUS").equal_to("Opened").get().val())
closecount=len(db.child("Tickets").order_by_child("STATUS").equal_to("Closed").get().val())
medi=len(db.child("Tickets").order_by_child("SEVERITY").equal_to("Medium").get().val())
loww=len(db.child("Tickets").order_by_child("SEVERITY").equal_to("Low").get().val())
urgg=len(db.child("Tickets").order_by_child("SEVERITY").equal_to("High").get().val())
ramcount=len(db.child("Tickets").order_by_child("CREATED BY").equal_to("Roshan").get().val())
rahulcount=len(db.child("Tickets").order_by_child("CREATED BY").equal_to("Ahmed").get().val())
rmcount=db.child("Tickets").order_by_child("CREATED BY").equal_to("ram").get()
rammedium=0
ramlow=0
ramurgent=0
for i in rmcount.each():
    if i.val()["SEVERITY"]=="Medium":
        rammedium+=1
    elif i.val()["SEVERITY"]=="Low":
        ramlow+=1
    else:
        ramurgent+=1
# print(rammedium)
# print(ramlow)
# print(ramurgent)


# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = ['Medium', 'Low', 'High']
sizes = [medi, loww, urgg]
# explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
#         shadow=True, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# plt.savefig("static/images/chart.png")
plt.close()



# with open("datasets/datecheck2.csv", 'r') as file:
#     csv_file = csv.DictReader(file)
#     for row in csv_file:
#         db.child("Tickets").push(dict(row))
#         # print(dict(row))

now1=None
today1=None

@app.route('/',methods=["GET","POST"])
def home():
    username=None
    passw=None
    session['uname']=None
    # msg="Ivalid username and password"
    if request.method=="POST":
        username=request.form['username']
        passw=request.form['upwd']
        session["username"]=username
        # peo=db.child("users").get()
        peo=db.child("users").order_by_child("email").equal_to(username).get()
        print(username)
        print(passw)
        for i in peo.each():
            # print(i.val())
            if i.val()['pwd']==passw:
                # print("hi")
                session["uname"]=i.val()['name']
                if i.val()['designation']=='Manager':
                    return redirect(url_for('manager'))
                else:
                    return redirect(url_for('agent'))
            else:
                # pass
                flash('invalid username and password','danger')
                return render_template("index.html")
    else:
        return render_template("index.html")
    return render_template("index.html")

@app.route('/manager',methods=["GET","POST"])
def manager():
    li=[]
    usern=None
    uemail=None
    upwd=None
    desig=None
    now1=None
    today1=None
    flagg=session['uname']
    if request.method=="POST":
        if request.form.get("crtbtn")=="Create":
            usern=request.form["usern"]
            uemail=request.form["uemail"]
            upwd=request.form["upwd"]
            desig=request.form["desig"]
            data={'designation':desig,'name':usern,'email':uemail,'pwd':upwd}
            db.child("users").push(data)
            return redirect(url_for('manager'))

        elif request.form.get("updatebtn")=="Update":
            cusid=request.form["cusid"]
            cusphone=request.form["cusphone"]
            closedby=request.form["closedby"]
            now1=datetime.datetime.now()
            today1=date.today()
            try:
                up=db.child("Tickets").order_by_child("PHONE NO").equal_to(cusphone).get()
                for i in up.each():
                    if i.val()["PHONE NO"]==cusphone and i.val()["CUSTOMER ID"]==cusid:
                        db.child("Tickets").child(i.key()).update({"STATUS":"Closed","CLOSED":str(now1),"DATECLOSED":str(today1)})
                    else:
                        pass
                flash("Ticket Closed Successfully")
                return redirect(url_for('manager'))
            except:
                flash("Invalid Data's")
                return redirect(url_for('manager'))
            return redirect(url_for('manager'))
            
    else:
        if flagg !=None:
            #bar chartc
            # x = np.array(["Opened", "Closed"])
            x=["opened","Closed"]
            y=[opencount,closecount]
            # y = np.array([opencount, closecount])
            # plt.bar(x,y)
            # plt.savefig("static/images/ucount.png")
            # plt.close()
            newtickets=db.child("Tickets").order_by_child("STATUS").equal_to("Opened").get()
            for i in newtickets.each():
                li.append(list([i.val()["CUSTOMER ID"],i.val()["PRODUCT NAME"],i.val()["ISSUES"],i.val()["CREATED BY"],i.val()["OPENED"],i.val()["SEVERITY"],i.val()["STATUS"]]))
            print(li)
            model.data1.head()
            print(model.dummy.head(1))
            print(model.dummy.tail(1))
            model.data1.describe()
            # print(type(data.head()))
            return render_template("manager.html",flagg_=flagg,datta=li,dum=model.dum1,dd1=model.dum2,labels=labels,sizes=sizes,x=x,y=y)
        else:
            flash("Please sign in","success")
            return redirect(url_for('home'))
    return render_template("manager.html",flagg_=session["username"])

@app.route('/agent',methods=["GET","POST"])
def agent():
    cid=None
    cname=None
    cphone=None
    Mname=None
    cate=None
    cissue=None
    seve=None
    check=[]
    usermedium=0
    userlow=0
    userhigh=0
    if request.method=="POST":
        if request.form.get("tckbtn")=="Submit":
            today=date.today()
            now=datetime.datetime.now()
            cid=request.form["cid"]
            cname=request.form["cname"]
            cphone=request.form["cphone"]
            Mname=request.form["Mname"]
            cate=request.form["cate"]
            cissue=request.form["cissue"]
            seve=request.form["seve"]
            try:
                data={'CUSTOMER ID':cid,'CUSTOMER NAME':cname,'PHONE NO':cphone,'PRODUCT NAME':Mname,'PRODUCT CATEGORY':cate,'ISSUES':cissue,'SEVERITY':seve,'CREATED BY':session['uname'],'OPENED':str(now),'CLOSED':0,'DATE-OPENED':str(today),'DATECLOSED':0,'Hours':0,'Days':0,'STATUS':'Opened'}
                db.child("Tickets").push(data)
                # print(data)
                flash("Ticket Created Successfully","success")
                return redirect(url_for('agent'))
            except:
                flash("Unable to create ticket","danger")
            return redirect(url_for('agent'))
        elif request.form.get("updatebtn")=="Update":
            cusphone=request.form["cusphone"]
            cusid=request.form["cusid"]
            now1=datetime.datetime.now()
            today1=date.today()
            try:
                up=db.child("Tickets").order_by_child("PHONE NO").equal_to(cusphone).get()
                for i in up.each():
                    if i.val()["PHONE NO"]==cusphone and i.val()["CUSTOMER ID"]==cusid:
                        db.child("Tickets").child(i.key()).update({"STATUS":"Closed","CLOSED":str(now1),"DATECLOSED":str(today1)})
                    else:
                        pass
                flash("Ticket Closed Successfully")
                return redirect(url_for('agent'))
            except:
                flash("Invalid Data's")
            return redirect(url_for('agent'))
        return redirect(url_for('agent'))
    else: 
        signas=session['uname']
        print(signas)
        iss=db.child("Tickets").order_by_child("CREATED BY").equal_to(signas).get()
        for i in iss.each():
            # print(i.val())
            if i.val()["CREATED BY"]==signas and i.val()["STATUS"]=="Opened":
                check.append(list([i.val()["CUSTOMER ID"],i.val()["PRODUCT NAME"],i.val()["PRODUCT CATEGORY"],i.val()["ISSUES"],i.val()["SEVERITY"],i.val()["STATUS"]]))
                with open("chem.csv","w")as file:
                    writer=csv.DictWriter(file,fieldnames=['CUSTOMER ID','CUSTOMER NAME','PHONE NO','PRODUCT NAME','PRODUCT CATEGORY','ISSUES','CREATED BY','SEVERITY','OPENED','CLOSED','DATE-OPENED','DATECLOSED','Hours','Days','STATUS'])
                    writer.writeheader()
                    writer.writerow(i.val())
            else:
                pass
            if i.val()["CREATED BY"]==signas:
                if i.val()["SEVERITY"]=="Medium":
                    usermedium+=1
                elif i.val()["SEVERITY"]=="Low":
                    userlow+=1
                else:
                    userhigh+=1
        return render_template("agent.html",check=check,signas=signas,usermedium=usermedium,userlow=userlow,userhigh=userhigh)

if __name__=='__main__':

    app.run(debug=True)
