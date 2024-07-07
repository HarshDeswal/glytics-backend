# app.py
from flask import Flask, request, jsonify,make_response
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import cast, Date
from sqlalchemy.sql import text
import pandas as pd
from flask_cors import CORS,cross_origin
import os
from datetime import datetime
from functools import wraps
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://vercel.com/harshdeswals-projects/glytics-frontend"}})
API_TOKEN = "12345"

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != API_TOKEN:
            return make_response(jsonify({"message": "Token is missing or invalid!"}), 403)
        return f(*args, **kwargs)
    return decorator

@app.route('/upload_csv/', methods=['POST'])
@token_required
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    df = pd.read_csv(file)

    # Dynamically create the table schema
    table_name = 'data'
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    return jsonify({"message": "File uploaded successfully","headers":df.columns.tolist()})

@app.route('/query/', methods=['GET'])
@token_required
def query_data():
    session = SessionLocal()
    table = Table('data', metadata, autoload_with=engine)
    query = session.query(table)

    filters = request.args.to_dict()
    for key, value in filters.items():
        if key.endswith('__gt'):
            column_name = key[:-4]
            query = query.filter(table.c[column_name] > value)
        elif key.endswith('__lt'):
            column_name = key[:-4]
            query = query.filter(table.c[column_name] < value)
        elif key.endswith('__gte'):
            column_name = key[:-5]
            query = query.filter(table.c[column_name] >= value)
        elif key.endswith('__lte'):
            column_name = key[:-5]
            query = query.filter(table.c[column_name] <= value)
        elif key.endswith('__eq'):
            column_name = key[:-4]
            query = query.filter(table.c[column_name].like(f"{value}%"))
        elif key.endswith('__max'):
            column_name = key[:-5]
            query = query.with_entities(func.max(table.c[column_name]))
        elif key.endswith('__min'):
            column_name = key[:-5]
            query = query.with_entities(func.min(table.c[column_name]))
        elif key.endswith('__sum'):
            column_name = key[:-5]
            query = query.with_entities(func.sum(table.c[column_name]))
        elif 'date' in key:
            # column_name = key.split('__')[0]
            date_value = datetime.strptime(value, '%Y-%m-%d')
            column = cast(table.c[column_name], Date)
            if key.endswith('__gt'):
                query = query.filter(column > date_value)
            elif key.endswith('__eq'):
                query = query.filter(column == date_value)
            elif key.endswith('__lt'):
                query = query.filter(column < date_value)
            elif key.endswith('__gte'):
                query = query.filter(column >= date_value)
            elif key.endswith('__lte'):
                query = query.filter(column <= date_value)
        elif isinstance(value, str):
            query = query.filter(table.c[key].like(f"%{value}%"))
        else:
            query = query.filter(table.c[key] == value)

    results = query.all()
    session.close()

    # Convert the results to a list of lists
    lst = []
    for val in results:
        lst1 = []
        for val2 in val:
            lst1.append(val2)
        lst.append(lst1)

    return jsonify({"results": lst})

if __name__ == '__main__':
    if not os.path.exists('./test.db'):
        metadata.create_all(engine)
    app.run(host='0.0.0.0', port=8000)
