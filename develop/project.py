from util.yaml_util import read_yaml
import requests


def develop_project(expression, param_flag):
    projects = read_yaml('project', 'config.yaml')
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
