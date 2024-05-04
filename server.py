import logging

import ctx
from quart_cors import *
from quart import Quart, request, jsonify
from pyfiglet import Figlet
from matcher.sbert import vectorise_text

logging.getLogger('asyncio').setLevel(logging.ERROR)  # remove asyncio logging
# --------------------------------------------------------
app = Quart(__name__)
app = cors(app, allow_origin="*")

f = Figlet(font='slant')
print(f.renderText('S E R V E R'))
# --------------------------------------------------------------------------
# GLOBAL CONTEXT
ctx = ctx.handler()
logger = ctx["logger"]
# --------------------------------------------------------------------------


@app.route('/vector/', methods=['GET'])
async def vectorise():
    """
    {
        "language": "en",
        "vectorise": [
            "Text A to vectorise",
            "Text B to vectorise",
            "Text C to vectorise"
        ]
    }
    @return: a JSON file with dimension, llm model, text to vectorise, and the numerical vector for eact text within
    the vectorise array
    """
    if request.is_json:
        data_json = await request.get_json()
        resp = vectorise_text(ctx, data_json)
    else:
        resp = jsonify('{Well formed JSON is requiered, please check request}')
        logger.debug('{}'.format(resp))
    return resp


# do not use this in production, run the app as follows: $ hypercorn server:app
app.run(host="127.0.0.1", debug=False, port=3000)
