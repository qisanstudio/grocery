import sys
import json
from os.path import basename, splitext


class MDDoc:

    COMMENT_BEGIN_FLAG = '<__COMMENT__BEGIN__FLAG__>'

    def __init__(self):
        self.md_struct = list()

    def line(self, content):
        self.md_struct.append(content + '\n')

    def br(self):
        self.line('')

    def block(self, content):
        self.line(content)
        self.br()

    def italic(self, content):
        self.block('*{0}*'.format(content))

    def bold(self, content):
        self.block('**{0}**'.format(content))

    def text(self, content):
        self.block(content)

    def hr(self):
        self.block('----------------')

    def title(self, content, level=1):
        self.block('#'*level + ' ' + content)

    def table(self, columns_name, rows):
        self.line('|{0}|'.format('|'.join(columns_name)))
        self.line('---'.join(list('|'*(len(columns_name) + 1))))
        if rows:
            for i in rows:
                self.line('|{0}|'.format('|'.join(i)))
        else:
            self.line('|'*(len(columns_name) + 1))
        self.br()

    def code_block(self, code, language=''):
        self.line('```{0}'.format(language))
        for i in code.split('\n'):
            self.line(i.replace('\n', ''))
        self.line('```')
        self.br()

    def comment_begin(self):
        self.line(self.COMMENT_BEGIN_FLAG)

    def comment_end(self):
        i = -1
        while True:
            if self.md_struct[i].startswith(self.COMMENT_BEGIN_FLAG):
                self.md_struct[i] = '\n'
                break
            self.md_struct[i] = self.md_struct[i]
            i -= 1
        self.br()

    def output(self):
        self.hr()
        return ''.join(self.md_struct)


def get_rows(raw, keys):
    result = list()
    for i in raw:
        result.append([i.get(k, '') for k in keys])
    return result


def parse(in_file, out_file):
    doc = MDDoc()

    with open(in_file) as f:
        collection = json.load(f)

    # The basic info.
    doc.title(collection['info']['name'])
    doc.line(collection['info'].get('description', ""))

    # API
    for api in collection['item']:
        doc.title(api['name'], 2)
        request = api['request']
        url = request['url']['raw'] if isinstance(request['url'], dict) \
            else request['url']
        url = url.replace('{{HOST}}', '')
        doc.code_block(
            '{0} {1}'.format(request['method'], url)
        )
        doc.block(request['description'])

        # Request information.
        doc.title('Request', 4)
        doc.comment_begin()
        if isinstance(request['url'], dict):
            # Request Query
            doc.bold('Query')
            rows = get_rows(
                request['url'].get('query', ''),
                ['key', 'value', 'description']
            )
            doc.table(['Key', 'Value', 'Description'], rows)

        # Request Header
        if request['header']:
            doc.bold('Header')
            rows = get_rows(
                request['header'],
                ['key', 'value', 'description']
            )
            doc.table(['Key', 'Value', 'Description'], rows)

        # Request Body
        if request['body']:
            content = request['body'][request['body']['mode']]
            if request['body']['mode'] == 'file' and isinstance(content, dict):
                content = content.get('src', '')

            if content:
                doc.bold('Body')
                if request['body']['mode'] in ['formdata', 'urlencoded']:
                    rows = get_rows(
                        request['body'][request['body']['mode']],
                        ['key', 'value', 'type', 'description']
                    )
                    doc.table(['Key', 'Value', 'Type', 'Description'], rows)
                elif request['body']['mode'] == 'raw':
                    doc.code_block(request['body']['raw'])
                elif request['body']['mode'] == 'file':
                    doc.text(request['body']['file']['src'])

        doc.comment_end()

        # Response example.
        doc.title('Examples:', 4)
        doc.comment_begin()
        for response in api['response']:
            doc.bold('Example: {0}'.format(response['name']))
            doc.comment_begin()

            # Original Request
            request = response['originalRequest']

            # Request URL
            url = request['url']['raw'] if isinstance(request['url'], dict) \
                else request['url']
            doc.code_block(
                '{0} {1}'.format(request['method'], url)
            )

            # Request Query
            doc.bold('Request')
            doc.comment_begin()
            if isinstance(request['url'], dict):
                doc.bold('Query')
                rows = get_rows(
                    request['url'].get('query', ''),
                    ['key', 'value', 'description']
                )
                doc.table(['Key', 'Value', 'Description'], rows)

            # Request Header
            if request['header']:
                doc.bold('Header')
                rows = get_rows(
                    request['header'],
                    ['key', 'value', 'description']
                )
                doc.table(['Key', 'Value', 'Description'], rows)

            # Request Body
            if request['body']:
                content = request['body'][request['body']['mode']]
                if request['body']['mode'] == 'file' and \
                        isinstance(content, dict):
                    content = content.get('src', '')

                if content:
                    doc.bold('Body')
                    if request['body']['mode'] in ['formdata', 'urlencoded']:
                        rows = get_rows(
                            content,
                            ['key', 'value', 'type', 'description']
                        )
                        doc.table(
                            ['Key', 'Value', 'Type', 'Description'], rows
                        )
                    elif request['body']['mode'] == 'raw':
                        doc.code_block(request['body']['raw'])
                    elif request['body']['mode'] == 'file':
                        doc.text(request['body']['file']['src'])

            doc.comment_end()

            doc.hr()

            # Response
            doc.bold('Response')
            doc.comment_begin()
            # doc.bold('Header')
            # header_rows = [[i['key'], i['value']] for i in response['header']]
            # doc.table(['Key', 'Value'], header_rows)
            doc.bold('Body')
            doc.code_block(json.dumps(json.loads(response['body']), indent=2))
            doc.comment_end()

            doc.comment_end()
        doc.comment_end()
        doc.hr()

    with open(out_file, 'w+') as f:
        f.write(doc.output())


def execute():
    in_file = sys.argv[1]

    if len(sys.argv) > 2:
        out_file = sys.argv[2]
    else:
        out_file = splitext(basename(in_file))[0] + '.md'

    parse(in_file, out_file)


if __name__ == '__main__':
    execute()

