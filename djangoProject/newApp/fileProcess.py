import os
import shutil
from django.conf import settings

from spire.pdf import PdfDocument
from spire.pdf import PdfTextExtractOptions
from spire.pdf import PdfTextExtractor


def processFile(fileName,filePath):
    #判断文档格式
    parts=fileName.split('.')
    fileType=parts[-1]

    if fileType=='pdf':
        save_path=extractPdf(fileName,filePath)
        text=paragrathSplit(save_path,fileType)
        return text
    elif fileType=='txt':
        save_path=extractTxt(fileName,filePath)
        text = paragrathSplit(save_path, fileType)
        return text
    else:
        print("no such file type")
        return []

def extractTxt(fileName,filePath):
    # 设置保存路径
    save_path = os.path.join(settings.BASE_DIR, 'newApp', 'static', 'processedfiles', fileName)
    # 保存
    shutil.copyfile(filePath, save_path)
    return save_path


def extractPdf(fileName,filePath):
    # 创建PdfDocument类的对象并加载PDF文件
    pdf = PdfDocument()
    pdf.LoadFromFile(filePath)

    # 创建一个字符串对象来存储文本
    extracted_text = ""

    # 创建PdfExtractor对象
    extract_options = PdfTextExtractOptions()
    # 设置使用简单提取方法
    extract_options.IsSimpleExtraction = True

    # 循环遍历文档中的页面
    for i in range(pdf.Pages.Count):
        # 获取页面
        page = pdf.Pages.get_Item(i)
        # 创建PdfTextExtractor对象，并将页面作为参数传递
        text_extractor = PdfTextExtractor(page)
        # 从页面中提取文本
        text = text_extractor.ExtractText(extract_options)
        # 将提取的文本添加到字符串对象中
        extracted_text += text

    # 获取文件名和扩展名
    file_name_without_ext, file_extension = os.path.splitext(fileName)
    # 新的文件名，扩展名为txt
    newFileName = file_name_without_ext + ".txt"

    # 设置保存路径
    save_path = os.path.join(settings.BASE_DIR, 'newApp', 'static', 'processedfiles', newFileName)

    # 将提取的文本写入文本文件
    with open(save_path, "w",encoding='utf-8') as file:
        file.write(extracted_text)

    # 删除水印
    with open(save_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # 去掉前72个字符
    modified_content = content[72:]
    # 将修改后的内容写回文件
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)

    pdf.Close()

    return save_path

def paragrathSplit(filePath,fileType):
    #打开文件并读取内容
    with open(filePath,'r',encoding='utf-8') as file:
        content = file.read()

    #分割文本
    sentences=content.split('.')
    if sentences[-1]=='':
        sentences=sentences[:-1]

    #段落列表
    paragraphs=[]
    for i in range(0,len(sentences),5):
        paragraph='.'.join(sentences[i:i+5])+'.'
        if fileType=='pdf':  paragraph = paragraph.replace('\n', '')  # 移除换行符
        para_dict={}
        para_dict['id']=i/5+1
        para_dict['direction']="英译中"
        para_dict['origin']=paragraph
        para_dict['target']=""
        para_dict['notes']=""
        paragraphs.append(para_dict)

    return paragraphs
