#from bs4 import BeautifulSoup
from pathlib import Path
import sys
import yaml

""" Example contents.yaml:

title: 
abstract: This is a sample abstract
samples:
  - original: data/original.wav
    modified: data/modified.wav
    pitch_curve: data/canvas.png
    text: This is a test sentence. (1)
    emotion: 'Neutral'
"""

"""
HTML Layout:

page-title
header-title
sub-title
abstract
paper-url
sample-list
"""

class Tag:
    @staticmethod
    def title(text: str):
        return "<title>{text}</title>" 

    @staticmethod
    def paragraph(s: str):
        return "<p>{text}</p>"

    @staticmethod
    def audio(path: str):
        return f'<audio  controls style="width: 190px;"><source src="{path}"/>Your browser does not support the audio element.</audio>'
    
    @staticmethod    
    def text(text: str):
        return f'<td style="vertical-align : middle;text-align:center;">{text}</td>'
   
    @staticmethod
    def image(path: str):
        return f'<img src="{path}" width="60%" height="60%"/>'
   
    @staticmethod
    def table_entry(tag: str):
        return f'<td style="vertical-align : middle;text-align:center;">{tag}</td>'
    
    def table_row(cols: list[str]):
        row  = '<tr>\n'
        for entry in cols:
            row += f'\t{Tag.table_entry(entry)}\n'
        row += '</tr>'
        return row 
        
def create_table_entry(sample: dict):
    try:
        text = sample['text'] 
        emotion = sample['emotion'] 
        pitch_curve = Tag.image(sample['pitch_curve'])  
        audio_original = Tag.audio(sample['original'])
        audio_modified = Tag.audio(sample['modified'])
    except KeyError as e:
        print(f'Unable to process entry due to missing key: {e}')
        exit(1)
    return Tag.table_row([emotion, text, pitch_curve, audio_original, audio_modified])
    
def create_table(sample_list: list[dict]):
    body = ""
    for sample in sample_list:
        body += create_table_entry(sample)
    return body
    
         
# Auto-matically replaced
class Html:
    def __init__(self, path: str):
        self.html_parser = None

        with open(TEMPLATE_PATH, 'r') as f:
            self.html_parser = BeautifulSoup(f, 'html.parser')
        assert self.html_parser

    def apply_contents(self, path: str):
        with open(path, 'r') as f:
            contents = yaml.safe_load(f)

    def update_title():
        pass

    def update_abstract():
        pass

    def update_paper_url():
        pass

    def update_sample_list():
        pass


def main(content):
    data_dir = Path(content['data_dir'])
    for entry in content['samples']:
        for key in ['pitch_curve', 'original', 'modified']:
            entry[key] = data_dir / entry[key]
    sample_table = create_table(content['samples'])
    with open('sample_table_dump.html', 'w') as f:
        f.writelines(sample_table)           

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: [template_path] [content_path]')
        exit(1)
        
    template_path =  sys.argv[1]
    content_path = sys.argv[2]
    with open(content_path, 'r') as yf:
        content = yaml.safe_load(yf)
        
    main(content)
    