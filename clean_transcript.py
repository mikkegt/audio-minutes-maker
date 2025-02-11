import os
import re

def clean_transcript(input_dir, output_file):
    """
    文字起こしファイルを読み込み、文を整形して1つのファイルにまとめます
    """
    all_content = []
    
    # ファイルを順番に処理
    files = sorted([f for f in os.listdir(input_dir) if f.endswith('.txt')])
    
    for filename in files:
        with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 長い文章を分割（句点で区切る）
        sentences = re.split('[。?！]', content)
        
        # 各文を処理
        for sentence in sentences:
            # 基本的なクリーニング
            text = sentence.strip()
            
            # フィラーや短すぎる文を除外
            if text and len(text) > 5 and not re.match(r'^(うーん|えーと|あの|えっと|ええと|んー|まあ|そうですね|はい|ごめんなさい|すみません)$', text):
                # 重複している部分を削除
                if text not in all_content:
                    all_content.append(text)
    
    # 結果を書き出し
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_content:
            f.write(line + "。\n")  # 句点と改行を追加
    
    print(f"処理が完了しました。合計{len(all_content)}文を保存しました。")
    return all_content

if __name__ == "__main__":
    input_dir = "transcripts"
    output_file = "cleaned_transcript.txt"
    cleaned_content = clean_transcript(input_dir, output_file)
