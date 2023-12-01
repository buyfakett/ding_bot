from util.yaml_util import read_yaml
import requests


def develop_nginx(expression, param_flag):
    nginxs = read_yaml('nginx', 'config.yaml')
    nginx_url = read_yaml('nginx-url', 'config.yaml')
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
