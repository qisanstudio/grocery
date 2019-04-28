# -*- coding: utf-8 -*-
import re
import sys
import csv
import click
import requests


HEADERS = {"cookie": "frequently_used_emojis=soccer; remember_user_token=W1sxNF0sIiQyYSQxMCRqdy9vUVpQQWtGQVZETU5RTVVtRXVPIiwiMTU0ODY4MzQ3Ni45NTc1MTg2Il0%3D--1fbc35a2dec299c478417b1d8c14ce1f26f8a675; _gitlab_session=574e01addd3e40a5adfd2e924f8252da; event_filter=all; sidebar_collapsed=true"}
HOST_URL_FORMAT = 'https://gitlab.city-home.cn/FE/croissant/raw/{branch}/src/utils/api.js'
BUN_URL_FORMAT = 'https://gitlab.city-home.cn/FE/bun/raw/{branch}/utils/api.js'


@click.group()
def cli():
    pass


class ParseAPIJS(object):

    def __init__(self, raw_doc):
        self.raw_doc = raw_doc


class ParseHOSTAPIJS(ParseAPIJS):
    '''
    文件结构：
    api.js
        app1
         |--func1
         |    |--func_name
         |    |--func_url
         |    |--func_method
         |    |--func_comment
         |           |--func_cn_name
         |           |--func_params
         |--func2
         |    |--func_name
         |    |--func_url
         |    |--func_method
         |    |--func_comment
         |           |--func_cn_name
         |           |--func_params
        app2
         .
         .
         .
    '''
    # BUG
    # 1. 没有注释的参数还不能取出来

    APP_RE = r'export\s+const\s+(?P<app_name>\w+)\s+\=\s+\{(?P<app_content>.+?)\n\}\;'
    APP_CONTENT_RE = r'(?P<func_name>\w+)\(context\, data\, callback\, errorCallback\)\s+\{(?P<func_body>.*?)\n\s+\}\,'
    APP_FUNC_URL_RE = r'const\s+url\s+\=\s+\`(?P<func_url>.+)\`\;'
    APP_FUNC_METHOD_RE = r'context\.axios\.(?P<func_method>.+)\(url\).+\;'
    APP_FUNC_COMMENT_RE = r'\/\*(?P<func_comment>.+)\*\/'
    APP_FUNC_COMMENT_CN_NAME_RE = r'(?P<cn_name>[\u4e00-\u9fa5]+)'
    APP_FUNC_COMMENT_PARAM_RE = r'\s+\*\s+(?P<key>\w+)\:\s+(?P<value>\w+)\,\s+(\/\/\s*(?P<cn_param>.+))?'

    def parse_app_func_comment(self, func_comment_doc):
        d = {}
        m = re.search(self.APP_FUNC_COMMENT_CN_NAME_RE, func_comment_doc)
        if m:
            d.update(m.groupdict())
        params = re.findall(self.APP_FUNC_COMMENT_PARAM_RE, func_comment_doc)
        if params:
            d['params'] = [{'key': i[0], 'value': i[1], 'cn': i[3]} for i in params]

        return d

    def parse_app_func_body(self, func_body_doc):
        d = {}
        m = re.search(self.APP_FUNC_URL_RE, func_body_doc)
        if m:
            d.update(m.groupdict())
        m = re.search(self.APP_FUNC_METHOD_RE, func_body_doc)
        if m:
            d.update(m.groupdict())
        m = re.search(self.APP_FUNC_COMMENT_RE, func_body_doc, re.DOTALL)
        if m:
            func_comment = m.groupdict()['func_comment']
            d.update(self.parse_app_func_comment(func_comment))

        return d

    def parse_app_content(self, app_content_doc):
        l = []
        funcs = re.findall(self.APP_CONTENT_RE, app_content_doc, re.DOTALL)
        for func_name, func_body in funcs:
            d = {}
            d['func_name'] = func_name
            d.update(self.parse_app_func_body(func_body))
            l.append(d)

        return l

    def run(self):
        l = []
        apps = re.findall(self.APP_RE, self.raw_doc, re.DOTALL)
        for app_name, app_content in apps:
            d = {}
            d['app_name'] = app_name
            d['funcs'] = self.parse_app_content(app_content)
            l.append(d)

        return l

    def get_urls(self):
        l = []
        apps = self.run()
        for app in apps:
            for func in app['funcs']:
                l.append(func.get('func_url', ''))
        return l

    def to_csv(self):
        writer = csv.writer(sys.stdout, delimiter=',')
        writer.writerow(['app_name', 'func_name', 'func_url', 'func_method', 'func_cname', 'func_params'])
        apps = self.run()

        for app in apps:
            for func in app['funcs']:
                writer.writerow([app['app_name'],
                                 func['func_name'],
                                 func.get('func_url', ''),
                                 func.get('func_method', ''),
                                 func['cn_name'],
                                 func.get('params', '')])


class ParseBUNAPIJS(ParseAPIJS):
    '''
    文件结构：
    api.js
        func1
         |--func_name
         |--func_url
         |--func_comment
         |      |--func_cn_name
         |      |--func_method
         |      |--func_params
        func2
         .
         .
         .
    '''
    # TODO
    # 1. params中的 query 和 data没有解析

    FUNC_RE = r'const\s+(?P<func_name>\w+)\s+\=\s+\(params\)\s+\=\>\s+\{(?P<app_content>.+?)\n\}\;'
    FUNC_URL_RE = r'wxRequest\(params\,\s+\`(?P<func_url>.+)\`\)\;'
    FUNC_COMMENT_RE = r'\/\*(?P<func_comment>.+)\*\/'

    FUNC_COMMENT_METHOD_RE = r'\*\s+method\:\s+\'(?P<func_method>.+)\'\,'
    FUNC_COMMENT_CN_NAME_RE = r'(?P<func_cnname>[\u4e00-\u9fa5]+)'
    # FUNC_COMMENT_QUERY_RE = r'\s+\*\s+(?P<key>\w+)\:\s+(?P<value>\w+)\,\s+(\/\/\s*(?P<cn_param>.+))?'
    # FUNC_COMMENT_DATA_RE = r'\s+\*\s+(?P<key>\w+)\:\s+(?P<value>\w+)\,\s+(\/\/\s*(?P<cn_param>.+))?'

    def parse_func_comment(self, comment_doc):
        d = {}
        m = re.search(self.FUNC_COMMENT_METHOD_RE, comment_doc)
        if m:
            d.update(m.groupdict())
        m = re.search(self.FUNC_COMMENT_CN_NAME_RE, comment_doc)
        if m:
            d.update(m.groupdict())

        return d

    def parse_func_body(self, body_doc):
        d = {}
        m = re.search(self.FUNC_URL_RE, body_doc)
        if m:
            d.update(m.groupdict())

        m = re.search(self.FUNC_COMMENT_RE, body_doc, re.DOTALL)
        if m:
            comment_doc = m.groupdict()['func_comment']
            d.update(self.parse_func_comment(comment_doc))

        return d

    def run(self):
        l = []
        funcs = re.findall(self.FUNC_RE, self.raw_doc, re.DOTALL)
        for func_name, func_body in funcs:
            d = {}
            d['func_name'] = func_name
            d.update(self.parse_func_body(func_body))
            l.append(d)

        return l

    def get_urls(self):
        l = []
        funcs = self.run()
        for func in funcs:
            l.append(func.get('func_url', ''))
        return l

    def to_csv(self):
        writer = csv.writer(sys.stdout, delimiter=',')
        writer.writerow(['func_name', 'func_url', 'func_method', 'func_cname', 'func_params'])
        funcs = self.run()

        for func in funcs:
            writer.writerow([func['func_name'],
                             func['func_url'],
                             func.get('func_method', ''),
                             func.get('func_cnname', '')])


@click.command()
@click.option('--branch', default='master')
def host(branch):
    resp = requests.get(HOST_URL_FORMAT.format(branch=branch), headers=HEADERS)
    parser = ParseHOSTAPIJS(resp.text)
    parser.to_csv()


@click.command()
@click.option('--branch', default='master')
def bun(branch):
    resp = requests.get(BUN_URL_FORMAT.format(branch=branch), headers=HEADERS)
    parser = ParseBUNAPIJS(resp.text)
    parser.to_csv()


@click.command()
@click.option('--branch', default='master')
def merge(branch):
    bun_resp = requests.get(BUN_URL_FORMAT.format(branch=branch), headers=HEADERS)
    bun_parser = ParseBUNAPIJS(bun_resp.text)
    bun_urls = bun_parser.get_urls()
    bun_urls = [re.sub(r'\$\{.*?\}', '', url) for url in bun_urls]

    host_resp = requests.get(HOST_URL_FORMAT.format(branch=branch), headers=HEADERS)
    host_parser = ParseHOSTAPIJS(host_resp.text)
    host_urls = host_parser.get_urls()
    host_urls = [re.sub(r'\$\{.*?\}', '', url) for url in host_urls]

    for url in bun_urls:
        if url in host_urls:
            print(url)


cli.add_command(host)
cli.add_command(bun)
cli.add_command(merge)


if __name__ == '__main__':
    cli()
