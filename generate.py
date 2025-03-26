import os
import markdown
from datetime import datetime
import re

def read_diary_template():
    # 個別の日記エントリー用テンプレート
    with open('diary-template.html', 'r', encoding='utf-8') as f:
        return f.read()

def read_index_template():
    # 一覧ページ用テンプレート
    with open('diary-index-template.html', 'r', encoding='utf-8') as f:
        return f.read()

def extract_date_from_filename(filename):
    # ファイル名から日付を抽出 (YYYY-MM-DD.md)
    match = re.match(r'(\d{4}-\d{2}-\d{2})\.md', filename)
    if match:
        date_str = match.group(1)
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            return date.strftime('%Y年%m月%d日')
        except ValueError:
            print(f'警告: 無効な日付形式のファイル: {filename}')
            return None
    return None

def convert_markdown_to_html(md_file):
    try:
        # Markdownファイルを読み込む
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # MarkdownをHTMLに変換
        html_content = markdown.markdown(md_content)
        
        # テンプレートを読み込む
        template = read_diary_template()
        
        # 日付を抽出
        date = extract_date_from_filename(os.path.basename(md_file))
        if not date:
            print(f'エラー: ファイル名から日付を抽出できません: {md_file}')
            return
        
        # HTMLを生成
        html = template.replace('{{content}}', html_content)
        html = html.replace('{{date}}', date)
        
        # 生成時間を取得
        generation_time = datetime.now().strftime('%Y年%m月%d日 %H時%M分%S秒')
        html += f'\n<!-- このファイルは{generation_time}に生成されました -->'
        
        # 出力ディレクトリの確認と作成
        os.makedirs('diary', exist_ok=True)
        
        # 出力ファイル名を生成
        output_file = os.path.join('diary', os.path.basename(md_file).replace('.md', '.html'))
        
        # HTMLファイルを保存
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f'生成完了: {output_file}')
        
    except Exception as e:
        print(f'エラー: ファイル処理中にエラーが発生しました: {md_file}')
        print(f'エラー内容: {str(e)}')

def generate_diary_index():
    try:
        # diary-mdディレクトリ内のファイルを取得して日付順にソート
        md_files = []
        for filename in os.listdir('diary-md'):
            if filename.endswith('.md'):
                with open(os.path.join('diary-md', filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                    title = content.split('\n')[0].replace('# ', '')
                date = extract_date_from_filename(filename)
                if date:
                    md_files.append((filename, date, title))
        
        # 日付の新しい順にソート
        md_files.sort(reverse=True)
        
        # diary.htmlを読み込む
        with open('diary.html', 'r', encoding='utf-8') as f:
            html = f.read()
        
        # エントリーリストを生成
        entries_html = ''
        for filename, date, title in md_files:
            link = f'diary/{filename.replace(".md", ".html")}'
            entries_html += f'''
            <div class="diary-entry">
                <div class="diary-date">{date}</div>
                <div class="diary-content">
                    <h2><a href="{link}">{title}</a></h2>
                </div>
            </div>
            '''
        
        # エントリーリストを挿入
        html = html.replace('{{entries}}', entries_html)
        
        # diary.htmlを保存
        with open('diary.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print('diary.htmlの生成完了')
        
    except Exception as e:
        print(f'エラー: diary.htmlの生成中にエラーが発生しました')
        print(f'エラー内容: {str(e)}')

def main():
    # 個別の日記エントリーのHTML生成
    for filename in os.listdir('diary-md'):
        if filename.endswith('.md'):
            md_file = os.path.join('diary-md', filename)
            convert_markdown_to_html(md_file)
    
    # インデックスページの生成
    generate_diary_index()

if __name__ == '__main__':
    main() 
