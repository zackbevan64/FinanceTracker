from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


def get_db_connection():
    connection = psycopg2.connect(
        user="test",
        password="testpassword",
        host="localhost",
        port="5432",
        database="dev",
    )
    return connection


@app.route("/transactions", methods=["GET"])
def get_transactions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM dev.transactions;")
    transactions = cur.fetchall()
    cur.close()
    conn.close()

    transactionList = []
    for transaction in transactions:
        transactionList.append(
            {
                "transactionID": transaction[0],
                "accountID": transaction[1],
                "amount": transaction[2],
                "transactionDate": transaction[3],
            }
        )
    return jsonify(transactionList)


@app.route("/transactions", methods=["POST"])
def add_transaction():
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO dev.transactions (accountid, amount, transactionDate) VALUES (%s, %s, %s)",
            (data["accountID"], data["amount"], data["transactionDate"]),
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Transaction added!"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cur
        conn.close()


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Finance Tracker API!"})


if __name__ == "__main__":
    app.run(debug=True)
