import asyncio
import logging
import argparse

import telethon.tl.types
from telethon import TelegramClient
from yaml import safe_load


async def callback(current, total):
    print('Downloaded', current, 'out of', total,
          'bytes: {:.2%}'.format(current / total))


async def main(config):
    parser = argparse.ArgumentParser('telegram-download-script')
    parser.add_argument('m', help='Telegram link to the message', metavar='message', type=str, action='store')
    parser.add_argument('p', help='Path to download folder', metavar='path', type=str, action='store',
                        default=config['default_path'])
    parser.add_argument('-v', '--verbose', help='Display logs', action='count')
    args = parser.parse_args()

    if args.verbose >= 2:
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=config['log_level'])
        logger = logging.getLogger(__name__)

    client = TelegramClient(**config['telethon_settings'])
    assert await client.start()

    if args.m and 'https://t.me/' in args.m:
        url = str(args.m).split('/')
        mess = await client.get_messages(telethon.tl.types.PeerChannel(int(url[4])), ids=int(url[5]))
        file = await client.download_media(message=mess,
                                           file=f'{args.p}/{mess.file.name}',
                                           progress_callback=callback if args.verbose else None
                                           )


if __name__ == '__main__':
    with open("config.yml", 'r') as f:
        config = safe_load(f)
        asyncio.run(main(config=config))
