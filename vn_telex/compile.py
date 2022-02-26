import re
import vn_telex.utils.charcases as charcases
import vn_telex.utils.vntelex as vntelex
import vn_telex.utils.progbar as progbar

IN_PATH = './raw/latin-quoc-ngu-syllables.txt'
OUT_PATH = './compiled/out.kmn'
MODIFIERS = list('sfrxjwoa')

header = [
    'begin Unicode > use(main)\n',
    '\n',
    'group(main) using keys\n'
]

content = []


if __name__ == '__main__':
    rules = []

    print(f'Loading syllables database at {IN_PATH} ... ', end='')
    inf_len = sum(1 for line in open(IN_PATH, 'r', encoding='utf-8'))
    inf = open(IN_PATH, 'r', encoding='utf-8')
    print('[DONE]')
    print(f'Analyzing syllables... ')
    count = 0
    rule_count = 0
    for syllable in inf:
        count += 1
        syllable = syllable.strip()
        if not re.search('^[a-zA-Z@._]*[a-zA-z0-9]$', syllable):
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
                        percentage=round(count / inf_len * 100),
                        message=f'({count}/{inf_len}) {syllable}: {sequence}'
                    )
            else:
                progbar.print_bar(
                    percentage=round(count / inf_len * 100),
                    message=f'({count}/{inf_len}) {syllable}'
                )
    inf.close()
    progbar.print_done(f'Analyzing complete. Found {count} syllable(s). Generated {rule_count} rule(s).')

    print(f'Cleaning up ruleset bases... ')
    for i in range(len(rules)):
        for j in range(len(rules)):
            if i != j and rules[i]['base'] == rules[j]['base'] + rules[j]['modifier']:
                progbar.print_bar(
                    percentage=round(i / len(rules) * 100),
                    message=f'({i}/{len(rules)}) base: {rules[i]["base"]} -> {rules[j]["result"]}'
                )
                rules[i]['base'] = rules[j]['result']
            else:
                progbar.print_bar(
                    percentage=round(i / len(rules) * 100),
                    message=f'({i}/{len(rules)}) base: {rules[i]["base"]}'
                )
    progbar.print_done(f'Cleaning complete.')

    content.sort()
    outf = open(OUT_PATH, 'w', encoding='utf-8')
    outf.writelines(header)
    outf.writelines(content)
    outf.close()
