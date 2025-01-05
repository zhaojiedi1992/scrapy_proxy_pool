from engine_v2.engine import Engine
import argparse


parser=argparse.ArgumentParser(description='scrapy_proxy_pool')
parser.add_argument('--processor', type=str, help='processor to run')
args = parser.parse_args()

if __name__ == '__main__':
    # if processor set, just run it
    if args.processor:
        getattr(Engine(), f'run_{args.processor}')()
    else:
        Engine().run()
