# -*- coding: utf-8 -*-            
# @Author : buyfakett
# @Time : 2023/11/30 20:32

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 定义模型类
Base = declarative_base()


class Project(Base):
    __tablename__ = 'develop_project'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)



