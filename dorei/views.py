from django.shortcuts import render, redirect

from django.http import HttpResponse
from dorei.models import *

from django.contrib import messages
from django.db import connection

from django.contrib.auth import authenticate
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as djUser

from datetime import datetime

from django.urls import reverse

import json

def insert_using_raw_sql(sql):
    print('sql - ', sql)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        return True
    except Exception as e:
        print(e)
        return False

def update_using_raw_sql(sql):
    print('sql - ', sql)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        return True
    except Exception as e:
        print(e)
        return False

def select_using_raw_sql(sql):
    print('sql - ', sql)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)
        return []
    results = cursor.fetchall()
    #print(results)
    l = []
    for  i in range(len(results)):
        dict = {}
        field = 0
        while True:
            try:
                dict[cursor.description[field][0]] = str(results[i][field])
                field = field +1
            except IndexError as e:
                break
        l.append(dict)
    return l


def logIn_user(request):

    if request.method == "POST":
        email = request.POST.get("email")
        results = select_using_raw_sql("SELECT du.user_id,du.password FROM dorei_user AS du WHERE du.email_address='" + str(email) + "'")

        if results:
            for user in results:
                if user['password'] == request.POST.get("password"):
                    #return render(request, 'user_ui.html', {'current_user':user['user_id']})
                    login_user = authenticate(request,username=user['user_id'], password=user['password'])
                    djlogin(request, login_user)
                    #return redirect(reverse('transaction', kwargs={"user_id": user['user_id']}))
                    return redirect(reverse('transaction'))
        else:
            messages.error(request, 'Email id or password does not match!')

    return render(request, 'logInUser.html')


def logIn_manager(request):
    #djlogout(request)

    if request.method == "POST":
        email = request.POST.get("email")
        results = select_using_raw_sql("SELECT dm.email_address,dm.password FROM dorei_manager AS dm WHERE dm.email_address='" + str(email) + "'")
        print(results,email)
        if results:
            for user in results:
                if user['password'] == request.POST.get("password"):
                    login_user = authenticate(request,username=user['email_address'], password=user['password'])
                    djlogin(request, login_user)
                    return redirect(reverse('manage'))
        else:
            messages.error(request, 'Email id or password does not match!')

    return render(request, 'logInManager.html')

@login_required()
def manage(request):

    total_charity = select_using_raw_sql("SELECT SUM(dm.amount) FROM dorei_money AS dm")

    books_donated = select_using_raw_sql("SELECT COUNT(db.isbn) FROM dorei_bookdonate AS db WHERE db.is_collected=1")
    #books_lended = select_using_raw_sql("SELECT COUNT(db.isbn) FROM dorei_bookrequest AS db WHERE db.is_delivered=1")
    stationery_donated = select_using_raw_sql("SELECT SUM(ds.quantity) FROM dorei_stationerydonate AS ds WHERE ds.is_collected=1")
    #stationery_lended = select_using_raw_sql("SELECT SUM(ds.quantity) FROM dorei_stationeryrequest AS ds WHERE ds.is_delivered=1")

    book_donors = select_using_raw_sql("SELECT COUNT(DISTINCT(db.user_id)) FROM dorei_bookdonate AS db WHERE db.is_collected=1")
    #book_receivers = select_using_raw_sql("SELECT COUNT(DISTINCT(db.user_id)) FROM dorei_bookrequest AS db WHERE db.is_delivered=1")
    stationery_donors = select_using_raw_sql("SELECT SUM(ds.user_id) FROM dorei_stationerydonate AS ds WHERE ds.is_collected=1")
    #stationery_receivers = select_using_raw_sql("SELECT SUM(ds.user_id) FROM dorei_stationeryrequest AS ds WHERE ds.is_delivered=1")

    stationery_stats = select_using_raw_sql("SELECT ds.stationery_id AS stationery_id, ds.stationery_name AS stationery_name, ds.tot_quantity AS tot_quantity FROM dorei_stationery AS ds")
    stationery_donation_stats = select_using_raw_sql("SELECT ds.stationery_id AS stationery_id, ds.stationery_name AS stationery_name, SUM(dsd.quantity) AS total_donated FROM dorei_stationery AS ds, dorei_stationerydonate as dsd WHERE ds.stationery_id=dsd.stationery_id AND dsd.is_collected=1 GROUP BY ds.stationery_id, ds.stationery_name")
    #stationery_request_stats = select_using_raw_sql("SELECT ds.stationery_name AS stationery_name, SUM(dsd.quantity) AS total_requests FROM dorei_stationery AS ds, dorei_stationeryrequest as dsd WHERE ds.stationery_id=dsd.stationery_id AND dsd.is_delivered=1 GROUP BY ds.stationery_id, ds.stationery_name")
    print(stationery_donation_stats)

    pending_book_requests = select_using_raw_sql("SELECT dbd.user_id AS user, dbd.isbn AS isbn, dbd.t_time AS t_time FROM dorei_bookdonate  AS dbd WHERE dbd.is_collected <> 1")
    pending_statinery_requests = select_using_raw_sql("SELECT dsd.user_id AS user, ds.stationery_id AS stationery, dsd.t_time AS t_time, dsd.quantity AS quantity  FROM dorei_stationerydonate AS dsd, dorei_stationery AS ds WHERE ds.stationery_id=dsd.stationery_id AND dsd.is_collected <> 1")

    data = {
            'total_charity':total_charity[0]['SUM(dm.amount)'],
            'books_donated':books_donated[0]['COUNT(db.isbn)'],
            #'books_lended':books_lended[0]['COUNT(db.isbn)'],
            'stationery_donated':stationery_donated[0]['SUM(ds.quantity)'],
            #'stationery_lended':stationery_lended[0]['SUM(ds.quantity)'],
            'book_donors':book_donors[0]['COUNT(DISTINCT(db.user_id))'],
            #'book_receivers':book_receivers[0]['COUNT(DISTINCT(db.user_id))'],
            'stationery_donors':stationery_donors[0]['SUM(ds.user_id)'],
            #'stationery_receivers':stationery_receivers[0]['SUM(ds.user_id)'],
            'stationery_stats':stationery_stats,
            'stationery_donation_stats':stationery_donation_stats,
            #'stationery_request_stats':stationery_request_stats,
            'pending_book_requests':pending_book_requests,
            'pending_statinery_requests':pending_statinery_requests,
        }
    return render(request, 'manager_ui.html', data)

def approve_book_donation(request, user_id, isbn):
    command = "UPDATE dorei_bookdonate SET is_collected=1 WHERE user_id="+str(user_id)+" AND isbn="+str(isbn)
    update_using_raw_sql(command)
    return redirect('/dorei/manage/')

def approve_stationery_donation(request, user_id, stationery_id, t_time, quantity):
    print(t_time)
    command1 = "UPDATE dorei_stationerydonate SET is_collected=1 WHERE user_id="+str(user_id)+" AND stationery_id="+str(stationery_id)+" AND t_time=\""+str(t_time)+"\""
    command2 = "UPDATE dorei_stationery SET tot_quantity=tot_quantity+"+str(quantity)+" WHERE stationery_id="+str(stationery_id)
    update_using_raw_sql(command1)
    update_using_raw_sql(command2)
    return redirect('/dorei/manage/')


def signUp(request):

    djlogout(request)

    if request.method == "POST":
        results = select_using_raw_sql("SELECT * FROM dorei_user")
        print("Working.....")
        print(results)

        FirstName = request.POST.get("first_name")
        MiddleName = request.POST.get("middle_name")
        LastName = request.POST.get("last_name")
        Email = request.POST.get("email")
        HouseNo = request.POST.get("house_no")
        StreetNo = request.POST.get("street_no")
        StreetName = request.POST.get("street_name")
        City = request.POST.get("city")
        State = request.POST.get("state")
        PostalCode = request.POST.get("zipcode")
        Password = request.POST.get("password")

        if User.objects.filter(email_address__exact=Email).exists():
            messages.error(request, 'This email address has been taken!')
            return render(request, 'SignUp.html')

        if request.POST.get("password") != request.POST.get("repeat_password"):
            messages.error(request, 'Password does not match!')
            return render(request, 'SignUp.html')

        '''i = "dorei_user(postal_code,first_name,middle_name,last_name,email_address,house_number,street_number,street_name,city,state,password)"
        j = "values("+str(PostalCode)+",'"+str(FirstName)+"','"+str(MiddleName)+"','"+str(LastName)+"','"+str(Email)+"','"+str(HouseNo)+"','"+str(StreetNo)+"','"+str(StreetName)+"','"+str(City)+"','"+str(State)+"','"+str(Password)+"')"


        command = "INSERT INTO " + i +" "+ j
        if insert_using_raw_sql(command):
            # insert phone number
            my_dict = select_using_raw_sql("SELECT du.user_id,du.password FROM dorei_user AS du WHERE du.email_address='" + str(Email) + "'")
            print(my_dict)

            new_user = djUser.objects.create_user(
                    username=my_dict[0]['user_id'] , password=my_dict[0]['password']
                )
            messages.success(request, 'Your account has been created successfully!')
            return redirect('/dorei/logInUser/')
        else:
            messages.error(request, 'Internal error! Try again.')
            return redirect('/dorei/signUp/')'''

        try :
            user = User.objects.create(email_address=Email, first_name=FirstName, middle_name=MiddleName,
                last_name=LastName, house_number=HouseNo, street_number=StreetNo, street_name=StreetName,
                city=City, state=State, postal_code=PostalCode, password=Password)

            my_dict = select_using_raw_sql("SELECT du.user_id,du.password FROM dorei_user AS du WHERE du.email_address='" + str(Email) + "'")
            print(my_dict)

            new_user = djUser.objects.create_user(
                    username=my_dict[0]['user_id'] , password=my_dict[0]['password']
                )
        except Exception as e:
                print(e)
                messages.error(request, 'Internal error! Try again.')
                return redirect('/dorei/signUp/')
        messages.success(request, 'Your account has been created successfully!')
        return render(request, 'logInUser.html')

    else:
        return render(request, 'SignUp.html')

@login_required()
def signOut(request):
    djlogout(request)
    return redirect('/dorei/logInUser/')


@login_required()
def transaction(request):

    user_id = request.user
    username = select_using_raw_sql("SELECT first_name FROM dorei_user as du WHERE du.user_id = "+ str(user_id))

    total_charity = select_using_raw_sql("SELECT SUM(dm.amount) FROM dorei_money AS dm")

    books_donated = select_using_raw_sql("SELECT COUNT(db.isbn) FROM dorei_bookdonate AS db WHERE db.is_collected=1")
    stationery_donated = select_using_raw_sql("SELECT SUM(ds.quantity) FROM dorei_stationerydonate AS ds WHERE ds.is_collected=1")

    book_donors = select_using_raw_sql("SELECT COUNT(DISTINCT(db.user_id)) FROM dorei_bookdonate AS db WHERE db.is_collected=1")
    stationery_donors = select_using_raw_sql("SELECT SUM(ds.user_id) FROM dorei_stationerydonate AS ds WHERE ds.is_collected=1")

    recent_book_donation = select_using_raw_sql("SELECT UPPER(du.first_name) AS name,UPPER(db.title) AS title,dbd.t_time AS t_time\
     FROM dorei_bookdonate AS dbd, dorei_book AS db, dorei_user AS du\
     WHERE dbd.is_collected=1 AND du.user_id=dbd.user_id AND db.isbn=dbd.isbn ORDER BY dbd.t_time DESC LIMIT 5")
    recent_stationery_donation = select_using_raw_sql("SELECT UPPER(du.first_name) AS name,UPPER(ds.stationery_name) AS category,dsd.quantity AS quantity,dsd.t_time AS t_time\
     FROM dorei_stationerydonate AS dsd, dorei_stationery AS ds, dorei_user AS du\
     WHERE dsd.is_collected=1 AND du.user_id=dsd.user_id AND ds.stationery_id=dsd.stationery_id ORDER BY dsd.t_time DESC LIMIT 5")

    results = select_using_raw_sql("SELECT * FROM dorei_stationerydonate")
    print(json.dumps(results,indent=4))

    results = select_using_raw_sql("SELECT * FROM dorei_stationery")
    print(json.dumps(results,indent=4))

    data = {
            'id':username[0]['first_name'],
            'charity':total_charity[0]['SUM(dm.amount)'],
            'books_donated':books_donated[0]['COUNT(db.isbn)'],
            'stationery_donated':stationery_donated[0]['SUM(ds.quantity)'],
            'book_donors':book_donors[0]['COUNT(DISTINCT(db.user_id))'],
            'stationery_donors':stationery_donors[0]['SUM(ds.user_id)'],
            'recent_book_donation':recent_book_donation,
            'recent_stationery_donation':recent_stationery_donation,
        }
    return render(request, 'user_ui.html', data)

@login_required()
def donate_money(request):

    user_id = request.user

    if request.method == "POST":
        MoneyId = Money.objects.all().count() + 1
        UserId = user_id
        Time =  datetime.now()
        TransactionId = request.POST.get("t_id")
        Amount = request.POST.get("amount")

        i = "dorei_money(money_id,user_id,t_time,amount,transaction_id)"
        j = "values("+str(MoneyId)+","+str(UserId)+",'"+str(Time)+"',"+str(Amount)+",'"+str(TransactionId)+"')"

        command = "INSERT INTO " + i +" "+ j
        if insert_using_raw_sql(command):
            results = select_using_raw_sql("SELECT * FROM dorei_money")
            print(json.dumps(results,indent=4))
            messages.success(request, 'Thank you for donating money.')
            return redirect(reverse('transaction'))
        else:
            messages.error(request, 'Internal error! Try again.')

    return render(request, 'donate_money.html')

@login_required()
def donate_book(request):

    user_id = request.user
    if request.method == "POST":

        system_messages = messages.get_messages(request)
        for message in system_messages:
            del message


        Isbn = Book.objects.all().count() + 1
        Author = request.POST.get("author")
        Subject = request.POST.get("subject")
        Title = request.POST.get("title")
        Edition = request.POST.get("edition")
        Grade = request.POST.get("class")

        i = "dorei_book(isbn, author, subject, title, edition, grade)"
        j = "values('"+str(Isbn)+"','"+str(Author)+"','"+str(Subject)+"','"+str(Title)+"',"+str(Edition)+","+str(Grade)+")"

        command1 = "INSERT INTO " + i +" "+ j

        UserId = user_id
        Time =  datetime.now()

        i = "dorei_bookdonate(user_id, isbn, t_time, is_collected)"
        j = "values("+str(UserId)+",'"+str(Isbn)+"','"+str(Time)+"','False')"

        command2 = "INSERT INTO " + i +" "+ j

        if insert_using_raw_sql(command1) and insert_using_raw_sql(command2):
            results = select_using_raw_sql("SELECT * FROM dorei_book")
            print(json.dumps(results,indent=4))

            results = select_using_raw_sql("SELECT * FROM dorei_bookdonate")
            print(json.dumps(results,indent=4))

            messages.success(request, 'Thank you for donating Book(s).')
            return redirect(reverse('transaction'))
        else:
            messages.error(request, 'Internal error! Try again.')
    return render(request, 'donate_book.html')

@login_required()
def donate_stationery(request):

    user_id = request.user

    if request.method == "POST":
        StationeryId = Stationery.objects.all().count() + 1
        StationeryName = request.POST.get("stationery_name")
        Quantity = request.POST.get("tot_quantity")

        i = "dorei_stationery(stationery_id, stationery_name, tot_quantity)"
        j = "values("+str(StationeryId)+",'"+str(StationeryName)+"',"+str(Quantity)+")"

        command1 = "INSERT INTO " + i +" "+ j

        UserId = user_id
        Time =  datetime.now()

        i = "dorei_stationerydonate(user_id, stationery_id, t_time, quantity, is_collected)"
        j = "values("+str(UserId)+","+str(StationeryId)+",'"+str(Time)+"',"+str(Quantity)+",'False')"

        command2 = "INSERT INTO " + i +" "+ j

        if insert_using_raw_sql(command1) and insert_using_raw_sql(command2):
            results = select_using_raw_sql("SELECT * FROM dorei_stationery")
            print(json.dumps(results,indent=4))

            results = select_using_raw_sql("SELECT * FROM dorei_stationerydonate")
            print(json.dumps(results,indent=4))

            messages.success(request, 'Thank you for donating Item(s).')
            return redirect(reverse('transaction'))
        else:
            messages.error(request, 'Internal error! Try again.')
    return render(request, 'donate_stationery.html')

def request(request):
    return render(request, 'request.html')
