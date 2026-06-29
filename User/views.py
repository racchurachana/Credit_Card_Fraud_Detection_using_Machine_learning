from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Credit_Card
import json


def index(request):
    return render(request, "index.html")


def adminlogin(request):
    if request.method == "POST":
        un = request.POST['uname']
        ps = request.POST['psw']
        user = auth.authenticate(username=un, password=ps)
        if user is not None and user.is_superuser:
            auth.login(request, user)
            return HttpResponseRedirect('adminhome')
        else:
            messages.info(request, "Invalid Credentials")
            return render(request, "adminlogin.html")
    return render(request, "adminlogin.html")


def register(request):
    if request.method == "POST":
        first = request.POST['fname']
        last = request.POST['lname']
        uname = request.POST['uname']
        em = request.POST['email']
        ps = request.POST['psw']
        ps1 = request.POST['psw1']
        if ps == ps1:
            if User.objects.filter(username=uname).exists():
                messages.info(request, "Username Exists")
                return render(request, "register.html")
            elif User.objects.filter(email=em).exists():
                messages.info(request, "Email exists")
                return render(request, "register.html")
            else:
                user = User.objects.create_user(
                    first_name=first, last_name=last,
                    username=uname, email=em, password=ps
                )
                user.save()
                return HttpResponseRedirect("login")
        else:
            messages.info(request, "Password not Matching")
            return render(request, "register.html")
    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        uname = request.POST['uname']
        ps = request.POST['psw']
        user = auth.authenticate(username=uname, password=ps)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('data')
        else:
            messages.info(request, "Invalid Credentials")
            return render(request, "login.html")
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def data(request):
    if request.method == "POST":
        category_input = request.POST['cat']
        amount = float(request.POST['amt'])
        latitude = float(request.POST['lat'])
        longitude = float(request.POST['long'])
        mlatitude = float(request.POST['mlat'])
        mlongitude = float(request.POST['mlong'])
        job_input = request.POST['job']

        import pandas as pd
        import numpy as np
        from sklearn.preprocessing import LabelEncoder
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
        from sklearn.ensemble import RandomForestClassifier

        df = pd.read_csv("static/dataset/CreditCard.csv")

        le_cat = LabelEncoder()
        le_job = LabelEncoder()
        df['category_enc'] = le_cat.fit_transform(df['category'])
        df['job_enc'] = le_job.fit_transform(df['job'])

        category_enc = le_cat.transform([category_input])[0] if category_input in le_cat.classes_ else 0
        job_enc = le_job.transform([job_input])[0] if job_input in le_job.classes_ else 0

        feature_cols = ['amt', 'lat', 'long', 'merch_lat', 'merch_long', 'category_enc', 'job_enc']
        X = df[feature_cols]
        y = df['is_fraud']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)

        accuracy = round(accuracy_score(y_test, rf.predict(X_test)) * 100, 2)

        pred_data = np.array([[amount, latitude, longitude, mlatitude, mlongitude, category_enc, job_enc]])
        prediction = rf.predict(pred_data)[0]
        prediction_data = "Fraud" if prediction == 1 else "No Fraud"

        # ── Chart data for browser graphs ────────────────────────────────────
        # 1. Pie chart: fraud vs no fraud counts
        fraud_counts = df['is_fraud'].value_counts()
        pie_labels = ['No Fraud', 'Fraud']
        pie_values = [int(fraud_counts.get(0, 0)), int(fraud_counts.get(1, 0))]

        # 2. Bar chart: top 10 jobs with fraud
        top_jobs = df[df['is_fraud'] == 1]['job'].value_counts().head(10)
        bar_labels = top_jobs.index.tolist()
        bar_values = top_jobs.values.tolist()

        # 3. Model accuracy comparison
        from sklearn.linear_model import LogisticRegression
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.naive_bayes import GaussianNB
        lr = LogisticRegression(max_iter=1000)
        knn = KNeighborsClassifier()
        nb = GaussianNB()
        lr.fit(X_train, y_train)
        knn.fit(X_train, y_train)
        nb.fit(X_train, y_train)
        acc_lr  = round(accuracy_score(y_test, lr.predict(X_test)) * 100, 2)
        acc_knn = round(accuracy_score(y_test, knn.predict(X_test)) * 100, 2)
        acc_nb  = round(accuracy_score(y_test, nb.predict(X_test)) * 100, 2)
        acc_rf  = accuracy

        model_names  = ['Logistic Regression', 'KNN', 'Naive Bayes', 'Random Forest']
        model_scores = [acc_lr, acc_knn, acc_nb, acc_rf]

        cc = Credit_Card.objects.create(
            category=category_input, amount=amount,
            latitude=latitude, longitude=longitude,
            merchant_latitude=mlatitude, merchant_longitude=mlongitude,
            jobs=job_input, prediction=prediction_data,
        )
        cc.save()

        return render(request, "predict.html", {
            "category": category_input, "job": job_input,
            "latitude": latitude, "longitude": longitude,
            "mlatitude": mlatitude, "mlongitude": mlongitude,
            "amount": amount, "prediction": int(prediction),
            "prediction_data": prediction_data, "accuracy": accuracy,
            "pie_labels": json.dumps(pie_labels),
            "pie_values": json.dumps(pie_values),
            "bar_labels": json.dumps(bar_labels),
            "bar_values": json.dumps(bar_values),
            "model_names": json.dumps(model_names),
            "model_scores": json.dumps(model_scores),
        })

    return render(request, "data.html")


def predict(request):
    return render(request, "predict.html")


def adminhome(request):
    cc = Credit_Card.objects.all()
    return render(request, "adminhome.html", {"cc": cc})
