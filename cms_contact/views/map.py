from collections import defaultdict


def get_coords(element, privacy=False):
    place = None
    if privacy and element.address_privacy == 'ONLYREGION':
        place = element.address.region
    elif element.address:
        place = element.address.city or element.address.region
    if not place or (privacy and element.address_privacy == 'HIDDEN'):
        return
    return place.location.coords


def group_by_coord(elements, value_fn=lambda x: x, key_fn=lambda x: x):
    data = defaultdict(list)
    for element in elements:
        coords = get_coords(element)
        if not coords:
            continue
        coords = key_fn(coords)
        data[coords].append(value_fn(element))
    return data
