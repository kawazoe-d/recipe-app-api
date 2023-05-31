"""
Test costom Django management commands.
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# patchのデコレーターを定義
# テスト対象のプログラムの中で呼び出される関数について、
# 未完成などの理由から取得したい戻り値が得られない場合に
# 想定される戻り値をテスト実施者が設定できるモジュール
@patch('core.management.commands.wait_for_db.Command.check')
class CommandsTests(SimpleTestCase):
    """"Test commands."""

    # @patchで生成されたオブジェクトを引数に渡す
    def test_wait_for_db_ready(self, patched_check):
        """Test waitting for database if database ready."""
        # patchオブジェクトに戻り値を設定
        patched_check.return_value = True

        # コマンドを叩く
        call_command('wait_for_db')

        # assert_called_once_with()  指定した引数で1回だけ呼ばれたか
        patched_check.assert_called_once_with(databases=['default'])

    # 引数で渡すpatchは近い方から書いていく
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # side_effect には iterable を設定することができ、
        # テスト対象のコードを実行するたびに、違う値がモックに設定されるようなテストを行える
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # call_count  呼ばれた回数
        self.assertEqual(patched_check.call_count, 6)
        # assert_called_with  最後に呼ばれた時の引数が一致するか
        patched_check.assert_called_with(databases=['default'])
