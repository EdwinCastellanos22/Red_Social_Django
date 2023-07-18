from django.shortcuts import render, redirect
import pyrebase
from django.core.files.storage import FileSystemStorage


# Setting Firebase
config = {
    "apiKey": "AIzaSyA2Ig4L5cSJHIgE1UCWj6y5Iizu5w_aJpQ",
    "authDomain": "django-api-730e4.firebaseapp.com",
    "projectId": "django-api-730e4",
    "storageBucket": "django-api-730e4.appspot.com",
    "messagingSenderId": "611779181554",
    "appId": "1:611779181554:web:d6839ce3da55ac88be496b",
    "measurementId": "G-L0RP3PSEJV",
    "databaseURL": "https://django-api-730e4-default-rtdb.firebaseio.com/"
}
firebase= pyrebase.initialize_app(config)
auth= firebase.auth()
database= firebase.database()
storage= firebase.storage()

# Create your views here.


def check(request):
    framework= database.child('Data').child('Framework').get().val()
    return render(request, 'check.html', {
        'Framework': framework,
    })

def updateImage(request):
    if request.method == 'POST' and request.FILES['image']:
        file= request.FILES['image']
        fs= FileSystemStorage()
        filename= fs.save(file.name, file)
        storage.child('images/'+file.name).put("media/"+file.name)
        print("File Uploaded!!")
        return redirect('/check')
    else:
        return render(request, 'check.html')
