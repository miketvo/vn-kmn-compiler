from shared.KeymanRule import KeymanRule

BASE = 'uo'
CORRECTION = {
    'uơ': ['q', 'h', 'th'],
    'ươ': ['ph', 'ch']
}


def generate(modifier=None):
    if modifier is None:
        raise ValueError("Must provide a modifier")
    rules = []

    return rules


if __name__ == '__main__':
    all_rules = generate(modifier='%TEST%')
    for i in range(len(all_rules)):
        print(f'{i}. {all_rules[i].base} + {all_rules[i].modifier} = {all_rules[i].result}')
