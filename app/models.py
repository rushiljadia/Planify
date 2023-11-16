from flask import Flask, jsonify, request
import uuid


class User:
    def sign_up(self):
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get("name"),
            "password": request.form.get("email"),
        }

        return jsonify(user), 200
