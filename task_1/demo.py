from task_1.zipper import zipper


def run():
    cases = [
        (1, 2, ' chars == numbs'),
        (3, 4, ' chars < numbs '),
        (4, 3, ' numbs > chars '),
        (5, 6, ' chars > numbs'),
    ]

    for i, j, exp in cases:
        print(f'Pairs of f{i}.txt {exp} f{j}.txt.')

        with open(f'data/f{i}.txt') as f1, \
                open(f'data/f{j}.txt') as f2:
            for pair in zipper(f1, f2):
                print(pair)

        print()


if __name__ == '__main__':
    run()
