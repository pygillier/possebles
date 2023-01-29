from mastodon import Mastodon
from backend.settings import app_settings
import logging

logger = logging.getLogger(__name__)

class MastodonService:

    cli: Mastodon

    def __init__(self):
        self.cli = Mastodon(
            client_secret=app_settings.mastodon_client_secret,
            access_token=app_settings.mastodon_access_token,
            api_base_url=app_settings.mastodon_api_url
        )

    def publish(self, entries: list):

        for entry in entries:
            logger.info(entry)
            # self.cli.status_post(
            #     status=f"[{entry.title}], published"
            # )
