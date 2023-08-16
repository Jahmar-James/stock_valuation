#app/init_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, configure_mappers
from sqlalchemy_continuum import VersioningManager
from app.dao.models.base import Base

from config import Config

engine = create_engine(Config.DB_TEST)
SessionLocal = sessionmaker(bind=engine)

# Just importing these will make sure the models are loaded and associated with Base.
from app.dao.models import User, Configuration, Dividend, Document, HistoricalMetrics, HistoricalPrice, Holding, Stock, Sector, ValuationModel, UserPortfolio, Transaction

configure_mappers()

if __name__ == "__main__":
    choice = input("Do you want to create tables? (yes/no): ").strip().lower()
    if choice == 'yes':
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")


        print("Versioning manager initialized successfully!")
    else:
        print("Operation aborted.")
