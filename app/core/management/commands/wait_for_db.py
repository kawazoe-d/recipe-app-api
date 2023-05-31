"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                # BaseCommand.check
                # システム チェック フレームワークを使用して、潜在的な問題がないか Django プロジェクト全体を検査します。
                # 重大な問題は CommandError として発生します。警告は stderr に出力されます。マイナーな通知は stdout に出力されます。
                # この場合は、settings.pyのDATABASESで指定されている'default'に接続されているかどうかを確認している
                self.check(databases=["default"])
                # 'default'に接続されていたらTrueに変更してループから抜ける
                db_up = True
            except (Psycopg2OpError, OperationalError):
                # エラーを拾った場合は、まだ接続できていないことを標準出力する
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
