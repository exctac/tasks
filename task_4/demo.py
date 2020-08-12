import os
import json

from task_4.user_chunks import build_unique_user_chunks


def run():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(base_dir, 'data/input.csv')) as file:
        print(json.dumps(build_unique_user_chunks(file), indent=2))


if __name__ == '__main__':
    run()
