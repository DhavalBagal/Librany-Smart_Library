import pyrebase
import sys
import datetime
import time

class Book:

    def __init__(self):

        config = {
          "apiKey": "AIzaSyBxhmLuQ30yH1gVnTTPC7LYuQrpzfxEK4E",
          "authDomain": "librany-dde7b.firebaseapp.com",
          "databaseURL": "https://librany-dde7b.firebaseio.com/",
          "storageBucket": "librany-dde7b.appspot.com",
          "serviceAccount": "librany-dde7b-firebase-adminsdk-fct8b-9a20d0a7ee.json"
            }
        firebase = pyrebase.initialize_app(config)

        self.db = firebase.database()

        auth = firebase.auth()

        try:
            self.user = auth.sign_in_with_email_and_password("dhavalbagal99@gmail.com", "Dhaval123")
        except :
            print("Invalid username or password!")
            sys.exit(1)

    def update_details(self,userid, bookid):

        book = self.db.child("BOOKS").child(bookid).get(self.user['idToken']).val()
    
        self.db.child("BOOKS").child(bookid).update({'Availability':'Unavailable', 'Issued_By':userid},self.user['idToken'])

        usr = self.db.child("USERS").child(userid).get(self.user['idToken']).val()
        count = usr["No_of_Books_Issued"]
        temp = {'Book'+str(count+1) : bookid}
        self.db.child("USERS").child(userid).update({'No_of_Books_Issued':(count+1)}, self.user['idToken'])
        self.db.child("USERS").child(userid).child("Books_Issued").update(temp, self.user['idToken'])

    def issue(self, userid, bookid):
 
        book = self.db.child("BOOKS").child(bookid).get(self.user['idToken']).val()
        if book is not None:
            avail = book["Availability"]
    
            if avail == 'Available':
                usr = self.db.child("USERS").child(userid).get(self.user['idToken']).val()

                if usr is not None:
                    allowance = usr["Issue_Allowance"]
                    issued = usr["No_of_Books_Issued"]

                    if issued < allowance:
                        Issue_ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d@%H:%M:%S')

                        key=bookid+"@"+userid+"@"+Issue_ts
                    
                        transaction ={'UserId':userid, 'BookId':bookid, 'Issue_ts':Issue_ts, 'Return_ts':' '}

                        self.db.child("TRANSACTIONS").child(key).set(transaction, self.user['idToken'])

                        self.update_details(userid, bookid)

                        return "IssueDone"
                    else :
                        return "AllowanceExceeded"

        return "IssueFailed"


    def returnbook(self, bookid):
        book = self.db.child("BOOKS").child(bookid).get(self.user['idToken']).val()

        if book is not None and book["Availability"]=="Unavailable":
            uid = book["Issued_By"]
            self.db.child("BOOKS").child(bookid).update({'Availability':'Available', 'Issued_By':' '}, self.user['idToken'])

            usr = self.db.child("USERS").child(uid).get(self.user['idToken']).val()
            n = usr["No_of_Books_Issued"]-1
            self.db.child("USERS").child(uid).update({'No_of_Books_Issued':n},self.user['idToken'])

            for k, val in usr["Books_Issued"].items():
                if val==bookid:
                    self.db.child("USERS").child(uid).child("Books_Issued").child(k).remove(self.user['idToken'])

            transactions = self.db.child("TRANSACTIONS").get(self.user['idToken']).val()

            for k1, k2 in transactions.items():
                temp = bookid+"@"+uid
                if temp in k1 and k2["Return_ts"]==" ":

                    Return_ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d@%H:%M:%S')
                    
                    self.db.child('TRANSACTIONS').child(k1).update({'Return_ts':Return_ts}, self.user['idToken'])

