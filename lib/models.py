from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# Name convention for foreign keys
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

# Basing class for declarative models
Base = declarative_base(metadata=metadata)

# Database URL and session setup
DATABASE_URL = 'sqlite:///freebies.db'  # SQLite database URL
engine = create_engine(DATABASE_URL, echo=True)  # echo=True to log SQL queries
Session = sessionmaker(bind=engine)
session = Session()


# Company Model
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    founding_year = Column(Integer(), nullable=False)

    # Relationships
    freebies = relationship('Freebie', backref='company', cascade="all, delete-orphan")
    devs = relationship('Dev', secondary='dev_freebies', backref='companies')

    def __repr__(self):
        
        return f'<Company {self.name}>'

    @classmethod
    def oldest_company(cls):
        
        return session.query(cls).order_by(cls.founding_year).first()

    def give_freebie(self, dev, item_name, value):
        
        freebie = Freebie(dev_id=dev.id, company_id=self.id, item_name=item_name, value=value)
        session.add(freebie)
        session.commit()


# Dev Model
class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)

    # Relationships
    freebies = relationship('Freebie', backref='dev', cascade="all, delete-orphan")

    def __repr__(self):
        
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        
        if freebie.dev_id == self.id:
            freebie.dev_id = dev.id
            session.commit()


# Freebie Model
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String(), nullable=False)
    value = Column(Integer(), nullable=False)
    dev_id = Column(Integer(), ForeignKey('devs.id'), nullable=False)
    company_id = Column(Integer(), ForeignKey('companies.id'), nullable=False)

    def __repr__(self):
        
        return f'<Freebie {self.item_name} from {self.company.name}>'

    def print_details(self):
        
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"


# Association Table for Many-to-Many Relationship (Dev <-> Company)
class DevFreebies(Base):
    __tablename__ = 'dev_freebies'

    dev_id = Column(Integer(), ForeignKey('devs.id'), primary_key=True)
    company_id = Column(Integer(), ForeignKey('companies.id'), primary_key=True)

    # Relationships (optional, if you want to access directly)
    dev = relationship('Dev', backref='dev_freebies')
    company = relationship('Company', backref='dev_freebies')


# Initialize the database (create tables)
def initialize_db():
    
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    initialize_db()
