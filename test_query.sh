#!/bin/sh
curl -X 'POST' \
  'http://127.0.0.1:8000/get_form?query=spam_email%3Dspam%40example.com&query=spam_phone%3D%2B71233211212&query=spam_date%3D2022-01-01&query=spam_text%3Dlorem' \
  -H 'accept: application/json' \
  -d '' &&
curl -X 'POST' \
  'http://127.0.0.1:8000/get_form?query=spam_email%3Dspam%40example.com&query=spa_phone%3D%2B799&query=spam_date%3D2022-01-01&query=spam_text%3Dlorem' \
  -H 'accept: application/json' \
  -d '' &&
curl -X 'POST' \
  'http://127.0.0.1:8000/get_form?query=customer_email%3Dcust%40example.com&query=customer_phone%3D%2B7123321222&query=spam_date%3D2022-01-01&query=spam_text%3Dlorem' \
  -H 'accept: application/json' \
  -d '' &&
  curl -X 'POST' \
  'http://127.0.0.1:8000/get_form?query=customer_email%3Dcust%40example.com&query=customer_phone%3D%2B7123321222&query=created%3D2022-01-01&query=customer_text%3Dlorem' \
  -H 'accept: application/json' \
  -d '' && 
  curl -X 'POST' \
  'http://127.0.0.1:8000/get_form?query=user_email%3Dust%40example.com&query=user_phone%3D%2B71233212212&query=last_login%3D2022-01-01&query=about%3Dtextsfwe' \
  -H 'accept: application/json' \
  -d ''
