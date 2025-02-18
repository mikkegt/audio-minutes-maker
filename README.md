# 🎙️ Audio Minutes Maker
音声ファイル（MP3）を分割し、Whisperを使用して文字起こしを行うツールです。

## ✨ 機能
- 🔪 MP3ファイルの分割（指定した時間間隔で分割）
- 📝 Whisperを使用した文字起こし
- ✂️ 文字起こしテキストの整形（フィラー除去、重複除去など）

## 🛠️ 環境構築

### 📋 必要なもの
- Python 3.11以上
- Homebrew (macOS)

### 🚀 セットアップ手順

1. 🍯 リポジトリのクローン
```bash
git clone git@github.com:mikkegt/audio-minutes-maker.git
cd audio-minutes-maker
```

2. 🐍 Python仮想環境の作成と有効化
```bash
python3.11 -m venv venv
source venv/bin/activate
```

3. 📦 必要なパッケージのインストール
```bash
pip install pydub openai-whisper torch ffmpeg-python
```

4. 🎵 ffmpegのインストール（macOS）

現在の環境を確認:
```bash
arch
````
arm64の場合:
```bash
brew install ffmpeg
```
i386 の場合（Rosetta2の場合）：
```bash
arch -arm64 zsh
brew install ffmpeg
```
⚠️ ：M1/M2 Macでは、ARM64ネイティブ環境での実行を推奨します。

## 🎯 使用方法
1. 📁 入力ファイルの準備
- 処理したいMP3ファイルをプロジェクトのルートディレクトリに配置
- split_mp3.py の以下の部分を実際のファイル名に変更：
```python
if __name__ == "__main__":
    input_file = "your_audio_file.mp3"  # ここを実際のファイル名に変更
    output_dir = "split_audio"
    split_mp3(input_file, output_dir, chunk_minutes=5)
```

2. ✂️ MP3ファイルの分割
```bash
python split_mp3.py
```
- デフォルトでは5分間隔で分割
- 分割されたファイルは `split_audio` フォルダに保存されます

4. 🎯 文字起こし
```bash
python transcribe.py
```
- 分割されたファイルを順次処理
- 文字起こし結果は `transcripts` フォルダに保存されます

5. 📝 テキストの整形
```bash
python clean_transcript.py
```
- 分割されたテキストファイルを統合
- 文字起こしされたテキストを整形
- フィラーや重複を除去
- 結果は `cleaned_transcript.txt` に保存

## ⚙️ 設定のカスタマイズ

### 🕒 分割時間の変更
`split_mp3.py` の以下の部分を修正:
```python
split_mp3(input_file, output_dir, chunk_minutes=5)  # 5を希望の分数に変更
```

### 🔧 Whisperモデルの変更
`transcribe.py` の以下の部分を修正:
```python
transcribe_audio(input_dir, output_dir, model_name="medium")  # モデル名を変更
```
利用可能なモデル: "tiny", "base", "small", "medium", "large"

## 🧹 環境の破棄

1. 仮想環境の終了
```bash
deactivate
```

2. 仮想環境の削除
```bash
rm -rf venv
```

3. ffmpegのアンインストール（必要な場合）
```bash
arch -arm64 brew uninstall ffmpeg # Rosetta2で動いてたら
# または
brew uninstall ffmpeg
```

## ⚠️ 注意事項
- 処理時間は音声の長さやモデルサイズによって変動します
- large モデルは高精度ですが、より多くのリソースと時間を必要とします

## 🎭 話者分離機能

音声ファイルから話者を識別し、誰が何を言ったかを区別する機能を追加しました。

### 📋 追加で必要なもの
- Hugging Faceアカウントとアクセストークン
- 追加のPythonパッケージ

### 🚀 セットアップ手順

1. 追加パッケージのインストール
```bash
pip install pyannote.audio python-dotenv
```

2. Hugging Faceアカウントの作成と設定
   - [Hugging Face](https://huggingface.co/join)でアカウント作成
   - Settings → Access Tokensからトークンを作成
   - 以下のモデルへのアクセス許可を得る（「Agree and access repository」をクリック）：
     - [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
     - [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0)

3. 環境変数の設定
   - `.env.template`をコピーして`.env`ファイルを作成
   ```bash
   cp .env.template .env
   ```
   - `.env`ファイルを編集し、Hugging Faceトークンを設定
   ```
   HF_TOKEN=your_token_here
   ```

### 🎯 話者分離機能の使用方法

1. 入力ファイルの準備（通常版と同様）

2. 話者分離付き文字起こしの実行
```bash
python transcribe_diarize.py
```

3. 出力ファイル
   - `diarized_transcripts/<ファイル名>_diarized.txt` - 話者情報付きのテキスト形式
   - `diarized_transcripts/<ファイル名>_diarized.json` - 詳細な話者・時間情報のJSON形式

### 📊 出力形式の例
```
[00:01:25.340 --> 00:01:35.120] SPEAKER_00: こんにちは、本日の会議を始めましょう。
[00:01:36.580 --> 00:01:42.750] SPEAKER_01: はい、よろしくお願いします。まず最初の議題についてですが...
```

### ⚠️ 注意事項
- 初回実行時はモデルのダウンロードに時間がかかります
- 複数の話者がいる場合、区別の精度は録音状態に依存します
- 各話者には自動的に「SPEAKER_00」「SPEAKER_01」などの識別子が割り当てられます
- 最良の結果を得るには、クリアな音声と話者間の十分な音響的差異が必要です
