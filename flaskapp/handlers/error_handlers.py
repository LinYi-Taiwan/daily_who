from flask import jsonify


def method_not_allowed(e):
    return jsonify({
        "status": 405,
        "message": "Method Not Alloweㄇd",
        "data": {"data": None}
    }), 405


def page_not_found(e):
    return jsonify({
        "status": 404,
        "message": "Page Not Found",
        "data": {"data": None}
    }), 404


def internal_server_error(e):
    return jsonify({
        "status": 500,
        "message": "Internal Server Error",
        "data": {"data": None}
    }), 500
