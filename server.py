import logging
import ctx
from quart_cors import cors
from quart import Quart, request, jsonify
from pyfiglet import Figlet
from matcher.sbert import vectorise_text
from matcher.query import list_course_by_instructor, list_course_general

logging.getLogger('asyncio').setLevel(logging.ERROR)  # remove asyncio logging

# Initialize the app
app = Quart(__name__)
app = cors(app, allow_origin="*")

# Display server banner
f = Figlet(font='slant')
print(f.renderText('S E R V E R'))

# Global context
ctx = ctx.handler()
logger = ctx["logger"]

@app.route('/vectorise/', methods=['POST'])
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
    @return: a JSON file with dimension, llm model, text to vectorise, and the numerical vector for each text within
    the vectorise array
    """
    if request.is_json:
        data_json = await request.get_json()
        resp = vectorise_text(ctx, data_json)
    else:
        resp = jsonify({'error': 'Well-formed JSON is required, please check request'})
        logger.debug('{}'.format(resp))
    return resp

@app.route('/course_by_instructor/', methods=['POST'])
async def course_by_instructor():
    if request.is_json:
        data_json = await request.get_json()
        resp = list_course_by_instructor(ctx, data_json)
    else:
        resp = jsonify({'error': 'Well-formed JSON is required, please check request'})
        logger.debug('{}'.format(resp))
    return resp

@app.route('/course_general/', methods=['POST'])
async def course_general():
    if request.is_json:
        data_json = await request.get_json()
        resp = list_course_general(ctx, data_json)
    else:
        resp = jsonify({'error': 'Well-formed JSON is required, please check request'})
        logger.debug('{}'.format(resp))
    return resp

# Do not use this in production, run the app as follows: $ hypercorn server:app
app.run(host="0.0.0.0", debug=False, port=3000)
