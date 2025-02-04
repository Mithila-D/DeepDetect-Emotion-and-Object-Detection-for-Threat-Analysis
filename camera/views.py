from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from .models import User
import cv2
import os
import torch
from deepface import DeepFace
 
yolo_model_path = os.path.join(settings.BASE_DIR, 'yolov5')
model = torch.hub.load(yolo_model_path, 'yolov5s', source='local')
video_path = os.path.join(settings.BASE_DIR, 'video', 'residence_security_camera_footage.mp4')

def detect_objects():
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        detected_frame = results.render()[0]

        _, jpeg = cv2.imencode('.jpg', detected_frame)

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    cap.release()

def index(request):
    return render(request, 'camera/index.html')

def video_feed(request):
    return StreamingHttpResponse(detect_objects(), content_type='multipart/x-mixed-replace; boundary=frame')

def object_detect(request):
    return render(request, 'camera/ObjectDetect.html')

def signup_view(request):
    if request.method == 'POST':
        UserName = request.POST.get('UserName')
        Password = request.POST.get('Password')
        if User.objects.filter(UserName=UserName).exists():
            messages.error(request, 'Username already taken. Please choose a different one.')
            return redirect('signup')  
        try:
            hashed_password = make_password(Password)
            user = User(UserName=UserName, Password=hashed_password)
            user.save()
            messages.success(request, 'User registered successfully. You can now log in.')
            return redirect('signin')  
        except IntegrityError:
            messages.error(request, 'An error occurred during registration. Please try again.')
            return redirect('signup') 
    return render(request, 'camera/SignUp.html') 

def login_view(request):
    if request.method == 'POST':
        UserName = request.POST.get('UserName')
        Password = request.POST.get('Password')
        try:
            user = User.objects.get(UserName=UserName)
            if check_password(Password, user.Password):
                return redirect('dashboard')   
            else:
                messages.error(request, 'Incorrect password. Please try again.')
                return redirect('signin')
        except User.DoesNotExist:
            messages.error(request, 'User not found or incorrect credentials.')
            return redirect('signin')
    return render(request, 'camera/SignIn.html')  

def dashboard(request):
    return render(request, 'camera/Dashboard.html')

def analyze_emotions(request):
    image_path = os.path.join(settings.MEDIA_ROOT, 'disguist.jpg')
    result = DeepFace.analyze(image_path, actions=['emotion'])
    emotions = result[0]['emotion']  

    context = {
        'emotions': emotions,
        'image_url': settings.MEDIA_URL + 'disguist.jpg', 
    }

    return render(request, 'camera/emotions.html', context)


from django.shortcuts import render

def buttons(request):
    return render(request, 'camera/alarm.html')
