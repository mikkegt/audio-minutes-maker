import os
from pathlib import Path
from dotenv import load_dotenv


def load_environment_variables():
    """
    .envファイルから環境変数を読み込みます
    """
    # プロジェクトのルートディレクトリにある.envファイルを探す
    env_path = Path('.') / '.env'

    # .envファイルが存在する場合は読み込む
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print(f".envファイルを読み込みました: {env_path.absolute()}")
    else:
        print("警告: .envファイルが見つかりません。環境変数を直接設定してください。")

    # 必要な環境変数を確認
    required_vars = ['HF_TOKEN']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        print(f"警告: 以下の環境変数が設定されていません: {', '.join(missing_vars)}")
        print("スクリプトの実行に問題が発生する可能性があります。")

    return os.environ.get('HF_TOKEN')


if __name__ == "__main__":
    # テスト実行
    token = load_environment_variables()
    if token:
        masked_token = token[:4] + '*' * (len(token) - 8) + token[-4:]
        print(f"HF_TOKEN: {masked_token}")
    else:
        print("HF_TOKENが設定されていません。")
