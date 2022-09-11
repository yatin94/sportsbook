
from models import Sport
from app import db


def get_all_sports():
    """
    - Purpose:
    - Args:
    - Returns
        - all_sports(list)
    """
    all_sports = Sport.get_all_sports()
    all_sports_dict = [dict(id=i[0], name=i[1], slug=i[2]) for i in all_sports]
    return all_sports_dict


def get_filtered_sport(slug=None, name=None, is_active=None, slug_like=None, name_like=None, name_start=None, slug_start=None, event_threshold=None, **kwargs):
    """
    - Purpose:
    - Args:
    - Returns:
    """
    print(event_threshold)
    filtered_sports = Sport.filtered_sport(slug, name, is_active, slug_like, name_like, name_start, slug_start, event_threshold)
    filtered_sports = [dict(id=i[0], name=i[1], slug=i[2]) for i in filtered_sports]
    return filtered_sports



def get_sport_id_from_sports_slug(slug):
    """
    - Purpose:
    - Args:
    - Returns:
    """
    result = Sport.get_sports_id_by_slug(slug=slug)
    if not result:
        raise Exception("No Such sport Slug found")
    return result[0], result[1]



def validate_sports_slug(slug):
    """
    - Purpose:
    - Args:
    - Returns:
    """
    result = Sport.get_sports_id_by_slug(slug=slug)
    if result:
        raise Exception("Slug already exists")



def create_sports_record(name, slug):
    """
    - Purpose:
    - Args:
    - Returns:
    """
    try:
        validate_sports_slug(slug)
        Sport.create_sport(name, slug)
        return {"message": "Sports Successfull Inserted"}
    except Exception as exec:
        return {"errMessage": str(exec)}, 400


def update_sports_record(slug, name=None, is_active=None):
    try:
        sport_id = Sport.get_sports_id_by_slug(slug)
        if sport_id:
            sport_id = sport_id[0]
            Sport.update_sports_by_id(sport_id, name, is_active)
            return {"message": "Sports Successfull Updated"}
        else:
            raise Exception("Not a valid slug")
    
    except Exception as exec:
        return {"errMessage": str(exec)}, 400



