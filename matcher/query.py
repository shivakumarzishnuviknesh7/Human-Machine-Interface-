from db.db_select import get_course_by_instructor, get_course_general

def list_course_by_instructor(ctx, json_payload):
    logger = ctx["logger"]
    db_courses = ctx["db_courses"]
    match = {}
    query = json_payload['instructor']
    logger.debug('query: {0}'.format(query))
    match = get_course_by_instructor(db_courses, query)
    logger.debug('{0}'.format(match))
    return match

def list_course_general(ctx, json_payload):
    logger = ctx["logger"]
    db_courses = ctx["db_courses"]
    match = {}
    query = json_payload['title']
    logger.debug('query: {0}'.format(query))
    match = get_course_general(db_courses, query)
    logger.debug('{0}'.format(match))
    return match
