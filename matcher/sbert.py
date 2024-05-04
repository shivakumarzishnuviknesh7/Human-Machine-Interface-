from db import db_select


def vectorise_text(ctx, json_payload):
    """
    This method returns the vector representation of a string for a given model
    @param ctx: contexter
    @param json_payload: string to vectorise
    @return: json with componenys language_model, dimension, vector
    """
    logger = ctx["logger"]
    llm_name = ctx["llm_name"]
    embedder = ctx["st_object_model"]
    device = ctx["torch_device"]
    lang = json_payload["language"].strip().lower()
    logger.debug('GET /sbert_get_vector/{}'.format(json_payload))

    match = {}
    cnt = 0
    for query in json_payload['vectorise']:
        query_embedding = embedder.encode(query, device=device, show_progress_bar=False)
        dim = len(query_embedding)
        vector = query_embedding.tolist()
        match[cnt] = {
            'llm': llm_name,
            'dimension': dim,
            'language': lang,
            'text': query,
            'vector': vector
        }
        cnt += 1
        logger.debug('{0}'.format(match))

    return match


