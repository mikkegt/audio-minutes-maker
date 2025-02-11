from pydub import AudioSegment
import math
import os

def split_mp3(input_file, output_dir, chunk_minutes=5):
    """
    MP3ファイルを指定した分数で分割します
    
    Parameters:
    input_file (str): 入力MP3ファイルのパス
    output_dir (str): 出力ディレクトリのパス
    chunk_minutes (int): 分割する時間（分）
    """
    # 出力ディレクトリがなければ作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # MP3ファイルを読み込み
    audio = AudioSegment.from_mp3(input_file)
    
    # 分割サイズを計算（ミリ秒）
    chunk_length_ms = chunk_minutes * 60 * 1000
    chunks = math.ceil(len(audio) / chunk_length_ms)
    
    # ファイル名から拡張子を除いた部分を取得
    filename = os.path.splitext(os.path.basename(input_file))[0]
    
    # 指定時間ごとに分割して保存
    for i in range(chunks):
        start_time = i * chunk_length_ms
        end_time = min((i + 1) * chunk_length_ms, len(audio))
        
        chunk = audio[start_time:end_time]
        chunk_name = f"{filename}_part{i+1:03d}.mp3"
        output_path = os.path.join(output_dir, chunk_name)
        
        # MP3として保存
        chunk.export(output_path, format="mp3")
        print(f"Created: {chunk_name}")

# 使用例
if __name__ == "__main__":
    input_file = "250210_1013.MP3"  # 入力ファイル名
    output_dir = "split_audio"  # 出力ディレクトリ
    split_mp3(input_file, output_dir, chunk_minutes=5)  # 5分ごとに分割
