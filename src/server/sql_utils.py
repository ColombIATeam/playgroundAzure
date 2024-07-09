from sqlmodel import Session, select
from api.common.dependency_container import DependencyContainer

class SQL_Utils():
    
    def __init__(self) -> None:
        DC = DependencyContainer()
        DC.initialize()
        
        self.DC = DC
    
    def sql_session(self):
        return Session(self.DC._database_engine)

    def select_table(self,type_class):
        with self.sql_session() as session:
            try:
                statement = select(type_class)
                results = session.exec(statement)
                return results.all()
            except Exception as e:
                return f"An error occurred: {str(e)}"
            finally:
                session.close()
                
    def insert_data(self, data, session):
            try:
                session.add(data)
                session.commit()
            except Exception as e:
                return f"An error occurred: {str(e)}"

