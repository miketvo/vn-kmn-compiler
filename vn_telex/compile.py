from numba import jit  # Utilize nVidia CUDA, delete this line if your graphic card doesn't support it
import re
import vn_telex.utils.charcases as charcases
import vn_telex.utils.vntelex as vntelex
import vn_telex.utils.progbar as progbar


HEADER_PATH = './raw/header.kmn'
IN_PATH = './raw/latin-quoc-ngu-rhymes.txt'
OUT_PATH = './compiled/out.kmn'
MODIFIERS = list('sfrxjwoa')


@jit(forceobj=True)  # Utilize nVidia CUDA, delete this line if your graphic card doesn't support it
def main():
    syllables = []

    print(f'Loading syllables database at {IN_PATH} ... ', end='')
    inf = open(IN_PATH, 'r', encoding='utf-8')
    for line in inf:
        syllables.append(line.strip())
    inf.close()
    print('[DONE]')

    print('Generating uppercase/lowercase syllable permutations... ', end='')
    additions = []
    for syllable in syllables:
        permutations = charcases.gen_case_permutations(syllable)
        for permutation in permutations:
            additions.append(permutation)
    for addition in additions:
        syllables.append(addition)
    syllables.sort()
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
    is_del = [True] * len(rules)
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
                is_del[i] = False
    progbar.print_done(f'Cleaning complete.')

    print('Deleting incorrect rules... ', end='')
    rules_filtered = []
    for i in range(len(is_del)):
        if not is_del[i]:
            rules_filtered.append(rules[i])
    print(f'[DONE] {len(rules_filtered)} rule(s) left.')
    # rules_filtered = rules

    print('Generating Keyman code... ')
    content = []
    for i in range(len(rules_filtered)):
        code = f"    '{rules_filtered[i]['base']}' + '{rules_filtered[i]['modifier'].lower()}' > '{rules_filtered[i]['result']}'\n"
        content.append(code)
        progbar.print_bar(
            percentage=round(i / len(rules_filtered) * 100),
            message=f'({i}/{len(rules_filtered)}) {code[:-1]}'
        )
        code = f"    '{rules_filtered[i]['base']}' + '{rules_filtered[i]['modifier'].upper()}' > '{rules_filtered[i]['result']}'\n"
        content.append(code)
        progbar.print_bar(
            percentage=round(i / len(rules_filtered) * 100),
            message=f'({i}/{len(rules_filtered)}) {code[:-1]}'
        )
    progbar.print_done(f'Code generated.')

    print('Saving Keyman code... ', end='')
    header = []
    headerf = open(HEADER_PATH, 'r', encoding='utf-8')
    for line in headerf:
        header.append(line)
    headerf.close()
    outf = open(OUT_PATH, 'w', encoding='utf-8')
    outf.writelines(header)
    outf.writelines(content)
    outf.close()
    print('[DONE]')


if __name__ == '__main__':
    main()
