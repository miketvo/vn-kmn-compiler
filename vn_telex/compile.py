from timeit import default_timer as timer
import vn_telex.utils.progbar as progbar
import vn_telex.utils.charcases as charcases
import vn_telex.utils.vnrhymes as vnr


HEADER_PATH = './raw/header.kmn'
OUT_PATH = './compiled/out.kmn'
MODIFIERS = list('sfrxjwoa')


def main():
    start_time = timer()

    print('Generating Vietnamese rhymes... ', end='')
    rhymes = vnr.generate()
    print(f'{len(rhymes)} generated. [DONE]')

    print('Generating uppercase and lowercase permutations... ', end='')
    rhymes_cases = []
    for i in range(len(rhymes)):
        permutation_matrix = charcases.gen_case_permutations_matrix(len(rhymes[i].base))
        for permutation_line in permutation_matrix:
            base = charcases.apply_case(rhymes[i].base, permutation_line)
            result = charcases.apply_case(rhymes[i].result, permutation_line)
            rhymes_cases.append(vnr.TelexRhyme(base, rhymes[i].modifier.lower(), result))
            rhymes_cases.append(vnr.TelexRhyme(base, rhymes[i].modifier.upper(), result))
            progbar.print_bar(
                percentage=round(i / len(rhymes) * 100),
                message=f'({i}/{len(rhymes)}) Processing {rhymes[i].result}'
            )
    progbar.print_done(f'{len(rhymes_cases)} generated. [DONE]')

    print('Generating Keyman code... ')
    content = []
    for i in range(len(rhymes_cases)):
        code = f"    '{rhymes_cases[i].base}' + '{rhymes_cases[i].modifier}' > '{rhymes_cases[i].result}'\n"
        content.append(code)
        progbar.print_bar(
            percentage=round(i / len(rhymes_cases) * 100),
            message=f'({i}/{len(rhymes_cases)}) {code[:-1]}'
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
    print(f'[DONE]\n\nTime elapsed: {round(timer() - start_time, 3)}s. ', end='')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nProcess interrupted.')
    finally:
        print('Process terminated.')
