python3 -m venv env

source env/bin/activate

pip3 install -r requirements.txt

python3 app.py




curl --header "Content-Type: application/json" \
--request POST \
--data '{ "user_name": "test", "password": "test" }' \
http://127.0.0.1:5007/login


curl --location 'http://127.0.0.1:5007/products' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJ0ZXN0IiwiZXhwIjoxNzM1MjY0NTU2fQ.JFVG5UJT1VCQqVRrxMGYM6hZo9SCsxPCL_dnOLrO8PE'


https://jwt.io/