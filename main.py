# !/usr/bin/env python

import argparse
import logging
from dingtalk_stream import AckMessage
import dingtalk_stream
from util.yaml_util import read_yaml
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 定义模型类
Base = declarative_base()


def setup_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(name)-8s %(levelname)-8s %(message)s [%(filename)s:%(lineno)d]'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def develop_nginx(expression, param_flag):
    nginxs = read_yaml('nginx', 'config')
    nginx_url = read_yaml('nginx-url', 'config')
    response = ''
    flag = 0
    if param_flag:
        response += '更新nginx配置：'
        for nginx in nginxs:
            response += '\n' + '更新 ' + nginx['server-name'] + ' 请回复：@jenkins服务一键上线 2 ' + str(nginx['id'])
    else:
        for nginx in nginxs:
            if expression == str(nginx['id']):
                try:
                    data = {
                        'ServerNameList': nginx['server-name']
                    }
                    requests.get(str(nginx_url), json=data, verify=False)
                except:
                    response = '调用上线接口成功'
                else:
                    response = '调用更新nginx配置接口成功， ' + str(nginx['server-name']) + ' 正在更新！'
            else:
                flag += 1
            if flag == nginx['id']:
                response = '没有该服务器'
    return response


def develop_project(expression, param_flag):
    projects = read_yaml('project', 'config')
    response = ''
    flag = 0
    if param_flag:
        response += '上线项目：'
        for project in projects:
            response += '\n' + '上线 ' + project['name'] + ' 请回复：@jenkins服务一键上线 1 ' + str(project['id'])
    else:
        for project in projects:
            if expression == str(project['id']):
                try:
                    requests.get(str(project['url']), verify=False)
                except:
                    response = '调用上线接口成功'
                else:
                    response = '调用上线接口成功， ' + str(project['name']) + ' 正在上线！'
            else:
                flag += 1
            if flag == project['id']:
                response = '没有该项目'
    return response


class CalcBotHandler(dingtalk_stream.ChatbotHandler):
    def __init__(self, logger: logging.Logger = None):
        super(dingtalk_stream.ChatbotHandler, self).__init__()
        if logger:
            self.logger = logger

    async def process(self, callback: dingtalk_stream.CallbackMessage):
        incoming_message = dingtalk_stream.ChatbotMessage.from_dict(callback.data)
        expression = incoming_message.text.content.strip()
        response = ''
        if expression == '':
            response += '请选择你要执行的操作(部分操作需提供参数)'
            response += '\n'
            response += '\n' + '范例1: @jenkins服务一键上线 1 1'
            response += '\n' + '1.直接上服务'
            response += '\n' + '2.更新nginx配置'
        else:
            parts = expression.split(" ")
            if len(parts) > 2:
                response = '参数数量错误'
            else:
                param_flag = False
                choose_ability = parts[0]
                if len(parts) == 1:
                    param_flag = True
                    choose_project = ''
                else:
                    choose_project = parts[1]
                if choose_ability == '1':
                    response = develop_project(choose_project, param_flag)
                elif choose_ability == '2':
                    response = develop_nginx(choose_project, param_flag)
                else:
                    response = '参数错误'

        self.reply_text(response, incoming_message)

        return AckMessage.STATUS_OK, 'OK'


def main():
    logger = setup_logger()

    credential = dingtalk_stream.Credential(read_yaml('client_id', 'config'),
                                            read_yaml('client_secret', 'config'))
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_callback_handler(dingtalk_stream.chatbot.ChatbotMessage.TOPIC, CalcBotHandler(logger))
    client.start_forever()


class Project(Base):
    __tablename__ = 'develop_project'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)


class Nginx(Base):
    __tablename__ = 'develop_nginx'
    id = Column(Integer, primary_key=True, index=True)
    server_name = Column(String(255), nullable=False)


if __name__ == '__main__':
    db_user = read_yaml('user', 'db')
    db_password = read_yaml('password', 'db')
    db_host = read_yaml('host', 'db')
    db_port = read_yaml('port', 'db')
    db_database = read_yaml('database', 'db')
    DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
    engine = create_engine(DATABASE_URL)
    # 创建表
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    session.close()
    main()
