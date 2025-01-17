from ie_serving.server.constants import INVALID_FORMAT, COLUMN_SIMPLIFIED, \
    COLUMN_FORMAT, ROW_SIMPLIFIED, ROW_FORMAT


def _evaluate_inputs(inputs):
    if type(inputs) is list and inputs:
        return COLUMN_SIMPLIFIED
    elif type(inputs) is dict and inputs.keys():
        return COLUMN_FORMAT
    return INVALID_FORMAT


def _evaluate_instances(instances, model_input_key_names):
    if type(instances) is list and instances:
        for instance in instances:
            # if any instance is not dict, treat instances as
            # simple formatted
            if not type(instance) is dict:
                return ROW_SIMPLIFIED
            # keys of every instance in full row format must match model's
            # inputs keys names, otherwise it's invalid
            if set(instance.keys()) != set(model_input_key_names):
                return INVALID_FORMAT
        return ROW_FORMAT
    return INVALID_FORMAT


def get_input_format(request_body, model_input_key_names):
    if 'inputs' in request_body.keys() and 'instances' in \
            request_body.keys():
        return INVALID_FORMAT

    if 'inputs' in request_body.keys():
        return _evaluate_inputs(request_body['inputs'])
    elif 'instances' in request_body.keys():
        return _evaluate_instances(request_body['instances'],
                                   model_input_key_names)
    return INVALID_FORMAT
