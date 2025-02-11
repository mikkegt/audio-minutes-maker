import os
import whisper
import time

def transcribe_audio(input_dir, output_dir, model_name="medium"):
    """
    指定されたディレクトリ内の音声ファイルを文字起こしします
    
    Parameters:
    input_dir (str): 入力音声ファイルのディレクトリ
    output_dir (str): 出力テキストファイルのディレクトリ
    model_name (str): 使用するWhisperモデル名（"tiny", "base", "small", "medium", "large"）
    """
    # 出力ディレクトリがなければ作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # モデルの読み込み
    print(f"モデル {model_name} を読み込んでいます...")
    model = whisper.load_model(model_name)
    
    # 入力ディレクトリ内のMP3ファイルを処理
    mp3_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.mp3')])
    
    for mp3_file in mp3_files:
        input_path = os.path.join(input_dir, mp3_file)
        output_path = os.path.join(output_dir, f"{os.path.splitext(mp3_file)[0]}.txt")
        
        print(f"\n{mp3_file} の文字起こしを開始します...")
        start_time = time.time()
        
        # 文字起こしの実行
        result = model.transcribe(
            input_path,
            language="ja",  # 日本語を指定
            fp16=False,     # M1 Macの場合、fp16=Falseの方が安定することがあります
            verbose=True
        )
        
        # 結果の保存
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        elapsed_time = time.time() - start_time
        print(f"{mp3_file} の文字起こしが完了しました（所要時間: {elapsed_time:.1f}秒）")

if __name__ == "__main__":
    input_dir = "split_audio"
    output_dir = "transcripts"
    transcribe_audio(input_dir, output_dir, model_name="medium")  # mediumモデルを使用
