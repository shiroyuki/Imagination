def foo(entity_a, entity_b, mixed_value, optional_entity = None):
    score = 0

    if entity_a and entity_b and mixed_value:
        score += 1

    if optional_entity:
        score += 1

    return score
