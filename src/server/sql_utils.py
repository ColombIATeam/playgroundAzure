from api.common.dependency_container import DependencyContainer
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  
from sqlalchemy.orm import sessionmaker  
 

class SQL_Utils():  
      
    def __init__(self) -> None:  
        # Initialize the asynchronous engine  
        #self._database_url = "mssql+aiomssql://username:password@your_server/your_database"  
        DC = DependencyContainer()
        DC.initialize()
        
        self.DC = DC
        self._engine = self.DC._database_engine 
  
    async def get_session(self):  
        # Create an asynchronous session  
        async_session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)  
        return async_session()  
  
    async def select_table(self, type_class):  
        async with self._engine.begin() as conn:  
            try:  
                result = await conn.execute(select(type_class))  
                return result.all()  
            except Exception as e:  
                return f"An error occurred: {str(e)}"  
  
    async def insert_data(self, data, session):  
        async with session.begin():  
            try:  
                session.add(data)  
            except Exception as e:  
                return f"An error occurred: {str(e)}"  