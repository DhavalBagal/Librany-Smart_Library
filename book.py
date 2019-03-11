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

        #Create a pyrebase object with the required configurations
        firebase = pyrebase.initialize_app(config)

        #Create database object which will be referenced for all the required transactions to be performed.
        self.db = firebase.database()

        #Create an authorization object
        auth = firebase.auth()

        try:
            self.user = auth.sign_in_with_email_and_password("dhavalbagal99@gmail.com", "Dhaval123")
        except :
            print("Invalid credentials or no Internet connectivity!")
            sys.exit(1)

    #Input is userid and bookid. The task is to update book and user details
    def update_details(self,userid, bookid):

        #Get details of the book associated with bookid
        book = self.db.child("BOOKS").child(bookid).get(self.user['idToken']).val()

        #Since the book is issued, we need to change its availability to Unavailable and set Issued_By to the userid who has issued the book.
        self.db.child("BOOKS").child(bookid).update({'Availability':'Unavailable', 'Issued_By':userid, 'Location':' '},self.user['idToken'])

        #Get details of the user associated with userid
        usr = self.db.child("USERS").child(userid).get(self.user['idToken']).val()

        #Get the number of books issued currently by the user.
        count = usr["No_of_Books_Issued"]

        #Increment the count by 1, since the No_of_Books_Issued should now be incremented
        temp = {'Book'+str(count+1) : bookid}
        self.db.child("USERS").child(userid).update({'No_of_Books_Issued':(count+1)}, self.user['idToken'])

        #Update the bookid of the issued book in that user's node
        self.db.child("USERS").child(userid).child("Books_Issued").update(temp, self.user['idToken'])

    def issue(self, userid, bookid):
 
        book = self.db.child("BOOKS").child(bookid).get(self.user['idToken']).val()

        #If the bookid that is recognised by the cam is present in the database, then do the following
        if book is not None:
            avail = book["Availability"]

            #If book is available, then do the following, else return 'IssueFailed'
            if avail == 'Available':
                usr = self.db.child("USERS").child(userid).get(self.user['idToken']).val()

                #If the identified userid exists in the database, then do the following,
                if usr is not None:
                    allowance = usr["Issue_Allowance"]
                    issued = usr["No_of_Books_Issued"]

                    
                    #If user has already issued say 2 books, then he cannot issue any book further
                    #Since those 2 books need to be returned first.
                    
                    if issued < allowance:

                        #Add the transaction details to the TRANSACTION table
                        Issue_ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d@%H:%M:%S')

                        key=bookid+"@"+userid+"@"+Issue_ts
                    
                        transaction ={'UserId':userid, 'BookId':bookid, 'Issue_ts':Issue_ts, 'Return_ts':' '}

                        self.db.child("TRANSACTIONS").child(key).set(transaction, self.user['idToken'])

                        #Update book and user details after the TRANSACTION table is updated
                        self.update_details(userid, bookid)

                        return "IssueDone"
                    else :
                        return "AllowanceExceeded"

        return "IssueFailed"


    def returnbook(self, bookid):
        book = self.db.child("BOOKS").child(bookid).get(self.user['idToken']).val()

        #If bookid recognised is present in the database and is currently issued by someone (i.e its availability is 'Unavailable')
        #This is because in subsequent frames acquired by the cam the same qrcode will be detected and hence to avoid DB transactions each time for each frame, we check the availability.
        if book is not None and book["Availability"]=="Unavailable":
            
            uid = book["Issued_By"]

            #Update the availability status and issued by field
            self.db.child("BOOKS").child(bookid).update({'Availability':'Available', 'Issued_By':' '}, self.user['idToken'])

            usr = self.db.child("USERS").child(uid).get(self.user['idToken']).val()

            #Decrement the count which maintains the number of books currently the user has.
            n = usr["No_of_Books_Issued"]-1
            self.db.child("USERS").child(uid).update({'No_of_Books_Issued':n},self.user['idToken'])

            #Remove the bookid which is returned from the Books_Issued field
            for k, val in usr["Books_Issued"].items():
                if val==bookid:
                    self.db.child("USERS").child(uid).child("Books_Issued").child(k).remove(self.user['idToken'])

            transactions = self.db.child("TRANSACTIONS").get(self.user['idToken']).val()

            #Update the return timestamp for the current transaction associated with that book in the TRANSACTION table.
            for k1, k2 in transactions.items():
                temp = bookid+"@"+uid
                if temp in k1 and k2["Return_ts"]==" ":

                    Return_ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d@%H:%M:%S')
                    
                    self.db.child('TRANSACTIONS').child(k1).update({'Return_ts':Return_ts}, self.user['idToken'])

    def updatelocation(self, bookid, loc):
        
        #Get details of the book associated with bookid
        book = self.db.child("BOOKS").child(bookid).get(self.user['idToken']).val()

        if book['Availability']=='Available':
        
            #Update location of the bookid
            self.db.child("BOOKS").child(bookid).update({'Location':loc},self.user['idToken'])
    










        
