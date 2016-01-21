from html.parser import HTMLParser
import os.path as os_path
import cv2

class Parser(HTMLParser):
    """ Parser that grabs the HOCR bbox
    """
    def __init__(self):
        self.boxes = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        is_word = False
        box = None
        for attr in attrs:
            if attr[0] =='class' and attr[1] =='ocrx_word':
                is_word = True
            elif attr[0] =='title' and attr[1].startswith('bbox'):
                box_str = attr[1].split(';')[0]
                box_str = list(map(int,box_str.split(' ')[1:]))
                box = ((box_str[0],box_str[1]),(box_str[2],box_str[3]))
        if not is_word:
            return
        self.boxes.append(box)

def get_hocr_boxes(file):
    """Gets a list of HOCR bbox
    Args:
        file (string): Hocr file
    Returns:
        Tuple: The box with ( (top_x,top_y),(bottom_x),(bottom_y))
    """
    parser = Parser()
    with open(file,'r',encoding='utf-8') as f:
        content = f.read()
        parser.feed(content)
    return parser.boxes

def remove_text(hocr,in,out):
    """Put a white rectangle on hocr box
    Args:
        hocr(str): hocr file
        in(str): input img path
        out(str):ouput img path
    """
    boxes = get_hocr_boxes(hocr)
    img = cv2.imread(in)
    for box in boxes:
        cv2.rectangle(img,box[0],box[1],(255,255,255),-1)
    cv2.imwrite(out,img)
