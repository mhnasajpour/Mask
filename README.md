# Mask
MASK, a project to control covid-19 and reduce deaths and diseases caused by it.

>*Visit website:* **https://mhnasajpour.pythonanywhere.com/**

## 0. Introduction

Mask has 3 type of accounts: ***Admin*** - ***General user*** - ***Business owner***.

These three types of people try to help reduce the disease in the whole society by following a series of policies.

## 1. Installation

```
git clone https://github.com/mhnasajpour/Mask.git
cd Mask

pip install virtualenv
python -m virtualenv venv
venv\Scripts\activate

pip install -r requirements.txt
```
> Now you have to copy file in the same destination.
```
xcopy backend\config\.env-sample backend\config\.env
```
> Go to path `backend\config\.env` and fill this file with your information.
```
cd backend
python manage.py migrate
python manage.py runserver
```
The project was run. You can see it by going to the URL http://127.0.0.1:8000/

## 2. APIs
To see the list of APIs, you can refer to URL http://127.0.0.1:8000/swagger/

![AUTH](https://github.com/mhnasajpour/Mask/blob/main/APIs/Auth_APIs.png)
![USER](https://github.com/mhnasajpour/Mask/blob/main/APIs/User_APIs.png)
![PLACE](https://github.com/mhnasajpour/Mask/blob/main/APIs/Place_APIs.png)
![HOSPITAL](https://github.com/mhnasajpour/Mask/blob/main/APIs/Hospital_APIs.png)
![MANAGER](https://github.com/mhnasajpour/Mask/blob/main/APIs/Manager_APIs.png)
