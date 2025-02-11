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
