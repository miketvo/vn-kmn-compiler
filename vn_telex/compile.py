import re
import vn_telex.utils.charcases as charcases
import vn_telex.utils.vntelex as vntelex
import vn_telex.utils.progbar as progbar

IN_PATH = './test/latin-quoc-ngu-syllables.txt'
OUT_PATH = './compiled/out.kmn'
MODIFIERS = list('sfrxjwoa')

header = [
    'begin Unicode > use(main)\n',
    '\n',
    'group(main) using keys\n'
]

content = []


if __name__ == '__main__':
    syllables = []

    print(f'Loading syllables database at {IN_PATH} ... ', end='')
    inf = open(IN_PATH, 'r', encoding='utf-8')
    for line in inf:
        syllables.append(line.strip())
    inf.close()
    print('[DONE]')



    print('Analyzing syllables... ')
    rules = []
    syllable_count = 0
    rule_count = 0
    for syllable in syllables:
        syllable_count += 1
        if not re.search('^[a-zA-Z]*[a-zA-z]$', syllable):
            sequences = vntelex.gen_key_sequences(syllable)
            for sequence in sequences:
                sequence = "".join(sequence.split())
                if sequence[-1] in MODIFIERS:
                    rule = {
                        'base': sequence[:-1],
                        'modifier': sequence[-1],
                        'result': syllable
                    }
                    rules.append(rule)
                    rule_count += 1
                    progbar.print_bar(
                        percentage=round(syllable_count / len(syllables) * 100),
                        message=f'({syllable_count}/{len(syllables)}) {syllable}: {sequence}'
                    )
            else:
                progbar.print_bar(
                    percentage=round(syllable_count / len(syllables) * 100),
                    message=f'({syllable_count}/{len(syllables)}) {syllable}'
                )
    progbar.print_done(
        f'Analyzing complete. Loaded {syllable_count}/{len(syllables)} syllable(s). Generated {rule_count} rule(s).'
    )

    print('Cleaning up ruleset bases... ')
    del_list = []
    for i in range(len(rules)):
        progbar.print_bar(
            percentage=round(i / len(rules) * 100),
            message=f'({i}/{len(rules)}) base: {rules[i]["base"]}'
        )
        for syllable in syllables:
            if rules[i]['base'] in vntelex.gen_key_sequences(syllable):
                progbar.print_bar(
                    percentage=round(i / len(rules) * 100),
                    message=f'({i}/{len(rules)}) base: {rules[i]["base"]} -> {syllable}'
                )
                rules[i]['base'] = syllable
            else:
                del_list.append(i)
    progbar.print_done(f'Cleaning complete.')

    print('Deleting incorrect rules... ', end='')
    for index in del_list:
        del(rules[index])
    print('[DONE]')

    print('Generating Keyman code... ')
    for i in range(len(rules)):
        code = f"    '{rules[i]['base']}' + '{rules[i]['modifier'].lower()}' > '{rules[i]['result']}'\n"
        content.append(code)
        progbar.print_bar(
            percentage=round(i / len(rules) * 100),
            message=f'({i}/{len(rules)}) {code}'
        )
        code = f"    '{rules[i]['base']}' + '{rules[i]['modifier'].upper()}' > '{rules[i]['result']}'\n"
        content.append(code)
        progbar.print_bar(
            percentage=round(i / len(rules) * 100),
            message=f'({i}/{len(rules)}) {code}'
        )
    progbar.print_done(f'Code generated.')

    print('Saving Keyman code... ', end='')
    outf = open(OUT_PATH, 'w', encoding='utf-8')
    outf.writelines(header)
    outf.writelines(content)
    outf.close()
    print('[DONE]')
