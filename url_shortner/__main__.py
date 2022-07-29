import argparse

from aiohttp.web import run_app

from url_shortner.app import create_app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--env-file', type=str, required=False)
    run_app(create_app(parser.parse_args()))
