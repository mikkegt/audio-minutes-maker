import os
import whisper
import time
import torch
from pyannote.audio import Pipeline
import json
from datetime import timedelta
from load_env import load_environment_variables


def format_timedelta(seconds):
    """秒数をHH:MM:SS.mmm形式に変換"""
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


def diarize_and_transcribe(input_file, output_dir, model_name="medium", hf_token=None):
    """
    音声ファイルを話者分離し、文字起こしします

    Parameters:
    input_file (str): 入力音声ファイルのパス
    output_dir (str): 出力テキストファイルのディレクトリ
    model_name (str): 使用するWhisperモデル名
    hf_token (str): Hugging Faceトークン（Noneの場合は環境変数から取得）
    """
    # 出力ディレクトリがなければ作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 出力ファイル名の設定
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_path = os.path.join(output_dir, f"{base_name}_diarized.txt")
    output_json = os.path.join(output_dir, f"{base_name}_diarized.json")

    print(f"\n{base_name}の話者分離と文字起こしを開始します...")
    start_time = time.time()

    # Hugging Faceトークンの取得
    if hf_token is None:
        hf_token = os.environ.get("HF_TOKEN")
        if hf_token is None:
            raise ValueError(
                "Hugging Faceトークンが必要です。パラメータで指定するか、HF_TOKEN環境変数を設定してください。")

    # 話者分離のパイプラインをロード
    print("話者分離モデルをロードしています...")
    diarization_pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token
    )

    # GPUが利用可能ならGPUを使用
    if torch.cuda.is_available():
        diarization_pipeline = diarization_pipeline.to(torch.device("cuda"))

    # 話者分離の実行
    print("話者分離を実行中...")
    diarization_result = diarization_pipeline(input_file)

    # WhisperモデルをCPUに明示的に割り当て（話者分離とGPUを競合させないため）
    device = "cpu"
    print(f"文字起こしモデル {model_name} をロードしています...")
    whisper_model = whisper.load_model(model_name, device=device)

    # 文字起こしの実行
    print("文字起こしを実行中...")
    transcription = whisper_model.transcribe(
        input_file,
        language="ja",
        fp16=False,
        verbose=True
    )

    # 話者分離結果と文字起こし結果を統合
    segments = []
    speaker_turns = []

    # 話者分離の結果を整理
    for turn, _, speaker in diarization_result.itertracks(yield_label=True):
        speaker_turns.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker
        })

    # 文字起こしの各セグメントに話者情報を付与
    for segment in transcription["segments"]:
        segment_start = segment["start"]
        segment_end = segment["end"]

        # このセグメントに最も重なっている話者を特定
        best_speaker = None
        best_overlap = 0

        for turn in speaker_turns:
            overlap_start = max(segment_start, turn["start"])
            overlap_end = min(segment_end, turn["end"])

            if overlap_end > overlap_start:
                overlap_duration = overlap_end - overlap_start
                if overlap_duration > best_overlap:
                    best_overlap = overlap_duration
                    best_speaker = turn["speaker"]

        # 話者情報を付与したセグメントを追加
        segments.append({
            "start": segment_start,
            "end": segment_end,
            "speaker": best_speaker,
            "text": segment["text"]
        })

    # 結果をJSONに保存
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({"segments": segments}, f, ensure_ascii=False, indent=2)

    # 読みやすいテキスト形式で保存
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in segments:
            start_str = format_timedelta(segment["start"])
            end_str = format_timedelta(segment["end"])
            speaker = segment["speaker"] if segment["speaker"] else "不明"
            f.write(f"[{start_str} --> {end_str}] {speaker}: {segment['text']}\n")

    elapsed_time = time.time() - start_time
    print(f"{base_name}の処理が完了しました（所要時間: {elapsed_time:.1f}秒）")
    print(f"結果を保存しました: {output_path} および {output_json}")


if __name__ == "__main__":
    # 環境変数を読み込み
    hf_token = load_environment_variables()

    # 環境変数から設定を取得（設定されていない場合はデフォルト値を使用）
    model_name = os.environ.get("WHISPER_MODEL", "medium")
    output_dir = os.environ.get("OUTPUT_DIR", "diarized_transcripts")
    input_file = os.environ.get("INPUT_FILE", None)

    if input_file and os.path.exists(input_file):
        # 単一ファイルの処理
        diarize_and_transcribe(input_file, output_dir, model_name, hf_token)
    else:
        # 複数ファイルの処理
        input_dir = "split_audio"
        print(f"{input_dir}ディレクトリ内の全MP3ファイルを処理します...")
        for filename in os.listdir(input_dir):
            if filename.endswith((".mp3", ".MP3")):
                input_file = os.path.join(input_dir, filename)
                diarize_and_transcribe(input_file, output_dir, model_name, hf_token)
