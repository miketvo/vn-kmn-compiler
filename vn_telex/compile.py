OUT_PATH = './compiled/out.kmn'
content = [
    'begin Unicode > use(main)\n',
    '\n',
    'group(main) using keys\n'
]


if __name__ == '__main__':
    out = open(OUT_PATH, 'w')
    out.writelines(content)
    out.close()
