import db as database
def get_db():
    db = database.AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()