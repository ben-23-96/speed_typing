from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('sqlite:///highscores.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Highscore(Base):
    __tablename__ = 'highscores'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)


Base.metadata.create_all(engine)


class HighscoreDatabase():
    def __init__(self) -> None:
        pass

    def add_new_highscore(self, name, score):
        """adds a new highscore to the database using the name and score inputs"""
        new_highscore = Highscore(name=name, score=score)
        session.add(new_highscore)
        session.commit()

    def top_10_highscores(self):
        """retrieves the top 10 highscores from the highscores database"""
        highscores = session.query(Highscore).order_by(
            Highscore.score.desc()).limit(10)
        return highscores
