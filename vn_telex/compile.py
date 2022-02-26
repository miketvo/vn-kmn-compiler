import string

VOWELS = 'aeiouăâêôơưyAEIOUĂÂÊÔƠƯY'
ACCENTED_VOWELS = 'ăâêôơưĂÂÊÔƠƯáéíóúắấếốớứýÁÉÍÓÚẮẤẾỐỚỨÝàèìòùằầềồờừỳÀÈÌÒÙẰẦỀỒỜỪỲảẻỉỏủẳẩểổởửỷẢẺỈỎỦẲẨỂỔỞỬỶãẽĩõũẵẫễỗỡữỹÃẼĨÕŨẴẪỄỖỠỮỸạẹịọụặậệộợựỵẠẸỊỌỤẶẬỆỘỢỰỴ'

IN_PATH = './raw/latin-quoc-ngu-syllables.txt'
OUT_PATH = './compiled/out.kmn'
content = [
    'begin Unicode > use(main)\n',
    '\n',
    'group(main) using keys\n'
]


if __name__ == '__main__':
    rules = []
    inf = open(IN_PATH, 'r', encoding='utf-8')
    for syllable in inf:
        for char in syllable:
            if char in ACCENTED_VOWELS:
                content.append('    ' + syllable)
    inf.close()

    outf = open(OUT_PATH, 'w', encoding='utf-8')
    outf.writelines(content)
    outf.close()
