#!/usr/bin/env python3

import argparse
import base64
import binascii
import io

from flask import Flask, request, Response
import jsonpickle
from PIL import Image

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)


@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a, b):
    response = {'sum': str(a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request

    # Convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)

        response = {
            'width': img.size[0],
            'height': img.size[1]
        }
    except:
        response = {'width': 0, 'height': 0}

    response_pickled = jsonpickle.encode(response)
    return Response(
        response=response_pickled,
        status=200,
        mimetype="application/json"
    )


@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    body = request.json

    try:
        a = body["a"]
        b = body["b"]

        a_len = len(a)
        b_len = len(b)

        if not isinstance(a, list) or not isinstance(b, list):
            raise TypeError

    except KeyError:
        return Response(
            response = jsonpickle.encode({
                "error": "Body does not contain 'a', 'b', or both."
            }),
            status = 400,
            mimetype = "application/json"
        )

    except TypeError:
        return Response(
            response = jsonpickle.encode({
                "error": "Either 'a', 'b', or both are not arrays."
            }),
            status = 400,
            mimetype = "application/json"
        )

    if a_len != b_len:
        return Response(
            response = jsonpickle.encode({
                "error": "Length of 'a' does not match length of 'b':"
                        f"len(a) = {a_len}, len(b) = {b_len}"
            }),
            status = 400,
            mimetype = "application/json"
        )

    dot_product = 0.0
    try:
        for i in range(a_len):
            dot_product += float(a[i]) * float(b[i])

    except ValueError:
        return Response(
            response = jsonpickle.encode({
                "error": "'a' or 'b' contains an invalid element."
            }),
            status = 400,
            mimetype = "application/json"
        )

    return Response(
        response = jsonpickle.encode({
            "dotproduct": f"{dot_product}"
        }),
        status = 200,
        mimetype = "application/json"
    )


@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    body = request.json
    
    try:
        image_b64 = body["image"]

        buffer = io.BytesIO( base64.b64decode(image_b64) )
        with Image.open(buffer) as image:
            response = {
                'width': image.size[0],
                'height': image.size[1]
            }

    except KeyError:
        return Response(
            response = jsonpickle.encode({
                "error": "Body does not contain 'image'."
            }),
            status = 400,
            mimetype = "application/json"
        )

    except (TypeError, ValueError, binascii.Error):
        return Response(
            response = jsonpickle.encode({
                "error": "Invalid 'image' value."
            }),
            status = 400,
            mimetype = "application/json"
        )

    except:
        response = {'width': 0, 'height': 0}

    return Response(
        response = jsonpickle.encode(response),
        status = 200,
        mimetype = "application/json"
    )

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Flask REST server'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port on which to run the server (default: 5000)'
    )

    args = parser.parse_args()

    # Start Flask app
    app.run(host='0.0.0.0', port=args.port)
