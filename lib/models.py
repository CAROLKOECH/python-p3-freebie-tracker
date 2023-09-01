from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    # Define the relationship between Company and Freebie
    freebies = relationship("Freebie", back_populates="company")
    
    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        # Create a new Freebie associated with this company and the given dev
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        return freebie

    @classmethod
    def oldest_company(cls, session):
        # Return the Company instance with the earliest founding year
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    
    # Define the relationship between Dev and Freebie
    freebies = relationship("Freebie", back_populates="dev")
    
    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        # Check if any of the freebies associated with the dev has the given item_name
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, other_dev, freebie):
        # Change the freebie's dev to be the given dev if it belongs to the current dev
        if freebie.dev == self:
            freebie.dev = other_dev

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    
    # Define foreign key relationships to Dev and Company
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))
    
    # Define the relationships between Freebie and Dev/Company
    dev = relationship("Dev", back_populates="freebies")
    company = relationship("Company", back_populates="freebies")
    
    def __repr__(self):
        return f'<Freebie {self.item_name}>'

    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'
