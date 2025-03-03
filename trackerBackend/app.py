from flask import Flask, jsonify, request

import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)


def get_db_connection():
    connection = psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )
    return connection


@app.route("/transactions", methods=["GET"])
def get_transactions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions;")
    transactions = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(transactions)


@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (accountid, ammount) VALUES (%s, %s)",
        (
            data["accountid"],
            data["ammount"],
        ),
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Transaction added!"})


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Finance Tracker API! test"})


if __name__ == "__main__":
    app.run(debug=True)
