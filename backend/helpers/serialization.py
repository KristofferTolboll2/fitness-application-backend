def to_json_trainer(x):
    certifications = [to_json_certificate(certificate) for certificate in x.certifications]
    return {
        'id': str(x.trainer_uuid),
        'email': x.email,
        'first_name': x.first_name,
        'last_name': x.last_name,
        'rating': x.rating,
        'certifications': certifications
    }


def to_json_certificate(x):
    return {
        'id': x.certification_id,
        'name': x.name,
        'description': x.description,
        'score': x.score
    }