from db.db_select import get_course_by_instructor

def list_course_by_instructor(ctx, json_payload):
    logger = ctx["logger"]
    db_courses = ctx["db_courses"]
    match = {}
    query = json_payload['instructor']
    logger.debug('query: {0}'.format(query))
    match = get_course_by_instructor(db_courses, query)
    logger.debug('{0}'.format(match))
    return match
