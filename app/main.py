from flask import Flask, Response, jsonify, request
from faker import Faker
import csv
import os
import requests

app = Flask(__name__)
fake = Faker()


@app.route('/requirements/')
def requirements():
    file_path = 'requirements.txt'
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return Response(file_content, content_type='text/plain')
    except Exception as e:
        return str(e)



@app.route('/users/generate', methods=['GET', 'POST'])
def generate_users():
    count = int(request.args.get('count', 100))
    users = [{'name': fake.name(), 'email': fake.email()} for i in range(count)]
    return jsonify(users)


@app.route('/')
def calculate_average():
    total_height = 0
    total_weight = 0
    num_rows = 0

    file_path = os.path.join('static', 'hw.csv')
    if not os.path.exists(file_path):
        return "Файл не найдено"

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)


        for row in reader:
            if len(row) >= 2:
                height = float(row[0])
                weight = float(row[1])
                total_height += height
                total_weight += weight
                num_rows += 1


    if num_rows > 0:
        avg_height = total_height / num_rows
        avg_weight = total_weight / num_rows
        return f"Средний рост: {avg_height:.2f} см<br>Средний вес: {avg_weight:.2f} кг"
    else:
        return "Недостаточно данных"


@app.route('/space/')
def space():
    url = 'http://api.open-notify.org/astros.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        number_of_astronauts = data['number']
        return f'Количество космонавтов на орбите: {number_of_astronauts}'
    else:
        return 'Ошибка'


if __name__ == '__main__':
    app.run(debug=True)



