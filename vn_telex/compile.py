import re
import utils.vntelex
import utils.charcases


IN_PATH = './raw/latin-quoc-ngu-syllables.txt'
OUT_PATH = './compiled/out.kmn'

header = [
    'begin Unicode > use(main)\n',
    '\n',
    'group(main) using keys\n'
]

content = []


if __name__ == '__main__':
    rules = []
    inf = open(IN_PATH, 'r', encoding='utf-8')
    for syllable in inf:
        syllable.strip()
        if not re.search('^[a-zA-Z@._]*[a-zA-z0-9]$', syllable):
            content.append('    ' + syllable)
    inf.close()

    content.sort()

    outf = open(OUT_PATH, 'w', encoding='utf-8')
    outf.writelines(header)
    outf.writelines(content)
    outf.close()
