# Online Quiz
![developer](https://img.shields.io/badge/Developed%20By%20%3A-Droos%20Chuck-blue)
---
# Online Quiz Platform Overview

Welcome to our **Online Quiz Platform**! This comprehensive system is designed to enhance the learning experience through interactive quizzes and assessments. Our platform caters to three distinct user roles: **Administrators**, **Teachers**, and **Students**. Each role has unique functionalities tailored to meet their specific needs.

## Key Features

### Administrator Portal
- **User Management**: Easily manage user accounts for teachers and students.
- **Analytics Dashboard**: Access detailed reports on quiz performance and user engagement.
- **Content Control**: Create, edit, and delete quizzes across various subjects.
- **Create Admin account** using command: ```py manage.py createsuperuser```


### Teacher Portal
- **Quiz Creation**: Design and customize quizzes with various question types.
- **Grading Tools**: Efficiently grade quizzes and provide feedback to students.
- **Progress Tracking**: Monitor student performance and track their progress over time.

### Student Portal
- **Access Quizzes**: Take quizzes at your convenience from any device.
- **Instant Feedback**: Receive immediate results and feedback on your performance.
- **Study Resources**: Access additional materials to help improve your knowledge and skills.

Join us in transforming the educational landscape with our interactive quiz platform, fostering a collaborative learning environment for all users!

---

## HOW TO RUN THIS PROJECT
- Install Python(3.7.6) (Dont Forget to Tick Add to Path while installing Python)
- Open Terminal and Execute Following Commands :
```
python -m pip install -r requirements. txt
```
- Download This Project Zip Folder and Extract it
- Move to project folder in Terminal. Then run following Commands :
```
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```
- Now enter following URL in Your Browser Installed On Your Pc
```
http://127.0.0.1:8000/
```

## CHANGES REQUIRED FOR CONTACT US PAGE
- In settins.py file, You have to give your email and password
```
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'your email password'
EMAIL_RECEIVING_USER = 'youremail@gmail.com'
```

## Drawbacks/LoopHoles
- Admin/Teacher can add any number of questions to any course, But while adding course, admin provide question number.


## Feedback
Any suggestion and feedback is welcome. You can message me on facebook
- [Contact on Facebook](https://fb.com/Droos.Chuck)
- [Subscribe my Channel DroosChuck On Youtube](https://youtube.com/DroosChuck)


