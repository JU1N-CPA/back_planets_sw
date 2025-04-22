def parse_comma_field(field):
    return [val.strip() for val in field.split(',') if val.strip()]

def join_comma_field(lst):
    return ', '.join(sorted(set(lst)))  # Optional: deduplicate and sort
