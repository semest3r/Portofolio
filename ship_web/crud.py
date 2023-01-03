from sqlalchemy.orm import Session

def db_get_all(models, limit, skip, db:Session):
    return db.query(models).offset(skip).limit(limit).all()

def db_get_filter(models, models_filter, filter, db: Session):
    return db.query(models).filter(models_filter == filter).first()

def db_filter(models, models_filter, filter, db: Session):
    return db.query(models).filter(models_filter == filter)


def db_search(models, filter, limit, skip, db:Session):
    return db.query(models).filter(filter).offset(skip).limit(limit).all()