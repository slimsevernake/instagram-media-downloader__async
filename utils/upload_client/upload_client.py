import asyncio
import aiofiles
from data.config import SESSION_DIR, DOWNLOAD_DIR
from http3 import AsyncClient
import logging
from telegram_upload.client import *


class UploadClient(TelegramClient):
    def __init__(self, session_name, api_id, api_hash, proxy=None, loop: asyncio.AbstractEventLoop = None, ):
        super().__init__(SESSION_DIR + session_name, api_id, api_hash, proxy=proxy)

    async def start(
            self,
            phone=lambda: click.prompt('Please enter your phone', type=phone_match),
            password=lambda: getpass.getpass('Please enter your password: '),
            *,
            bot_token=None, force_sms=False, code_callback=None,
            first_name='New User', last_name='', max_attempts=3):
        return await super().start(phone=phone, password=password, bot_token=bot_token, force_sms=force_sms,
                                   first_name=first_name, last_name=last_name, max_attempts=max_attempts)

    @staticmethod
    async def get_file(url: str, filename: str) -> str:
        logging.info('Downloading file from ' + url)
        if not os.path.exists(DOWNLOAD_DIR):
            os.mkdir(DOWNLOAD_DIR)
        client = AsyncClient()
        resp = await client.get(url)
        if resp.status_code == 200:
            f = await aiofiles.open(DOWNLOAD_DIR + filename, mode='wb')
            await f.write(await resp.read())
            await f.close()
            logging.info('File is downloaded')
            return DOWNLOAD_DIR + filename

    async def send_files(self, entity, files: list, delete_on_success=False,
                         force_file=False, caption=None, thumbnail=None):
        file_ids = []
        for file in files:
            if isinstance(file, File):
                name = file_name = file.file_name
                file_size = file.file_size
                force_file = True
            else:
                file_name = os.path.basename(file)
                file_size = os.path.getsize(file)
                name = '.'.join(file_name.split('.')[:-1])
            name = name.split('/')[-1]
            logging.info(f'Uploading "{file_name}", {file_size}')
            thumb = None
            if thumbnail is None and not isinstance(file, File):
                try:
                    thumb = get_file_thumb(file)
                except ThumbError as e:
                    click.echo('{}'.format(e), err=True)
            elif thumbnail is not False:
                if not isinstance(thumbnail, str):
                    raise TypeError('Invalid type for thumbnail: {}'.format(type(thumbnail)))
                elif not os.path.lexists(thumbnail):
                    raise TelegramInvalidFile('{} thumbnail file does not exists.'.format(thumbnail))
                thumb = thumbnail
            file_caption = truncate(caption if caption is not None else name, CAPTION_MAX_LENGTH)
            try:
                if force_file or isinstance(file, File):
                    attributes = [DocumentAttributeFilename(file_name)]
                else:
                    attributes = get_file_attributes(file)
                try:
                    message = await self.send_file(entity, file, thumb=thumb,
                                                   file_size=file_size if isinstance(file, File) else None,
                                                   caption=file_caption, force_document=force_file,
                                                   attributes=attributes)
                    # if hasattr(message.media, 'document') and file_size != message.media.document.size:
                    #     raise TelegramUploadDataLoss(
                    #         'Remote document size: {} bytes (local file size: {} bytes)'.format(
                    #             message.media.document.size, file_size))
                finally:
                    logging.info(f'Uploaded "{file_name}", {file_size}')
            finally:
                if thumb:
                    os.remove(thumb)
            if delete_on_success:
                logging.info(f'Deleting "{file_name}"')
                os.remove(file)
            file_ids.append(pack_bot_file_id(message.media))
        return file_ids
