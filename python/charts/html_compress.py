import html
import re


def compress_html(html_content: str) -> str:
    """
    压缩HTML内容，移除注释、空白，并简化变量名和属性。
    
    Args:
        html_content (str): 原始HTML内容
        
    Returns:
        str: 压缩后的HTML内容
    """
    h = html_content
    
    # 移除注释
    h = re.sub(r'<!--.*?-->', '', h, flags=re.DOTALL)
    h = re.sub(r'/\*.*?\*/', '', h, flags=re.DOTALL)
    
    # 移除所有空白
    h = re.sub(r'\s+', ' ', h)
    
    # 移除标签间的空格
    h = re.sub(r'>\s+<', '><', h)
    
    # 压缩CSS/JSON空格
    h = re.sub(r':\s+', ':', h)
    h = re.sub(r';\s+', ';', h)
    h = re.sub(r',\s+', ',', h)
    h = re.sub(r'\s*{\s*', '{', h)
    h = re.sub(r'\s*}\s*', '}', h)
    
    # 简化HTML属性
    h = h.replace('class="chart-container"', 'class="c"')
    
    # 替换UUID
    uuids = re.findall(r'[a-f0-9]{32}', h)
    if uuids:
        u = uuids[0]
        h = h.replace(u, 'u')
    
    # 替换变量名
    h = re.sub(r'var chart_\w+', 'var c', h)
    h = re.sub(r'var option_\w+', 'var o', h)
    h = re.sub(r'chart_\w+', 'c', h)
    h = re.sub(r'option_\w+', 'o', h)
    h = re.sub(r"'[a-f0-9]{32}'", "'u'", h)
    
    # 转义HTML
    result = html.escape(h.strip(), quote=True)
    
    return result


def compress_html_file(input_file: str, output_file: str) -> None:
    """
    读取HTML文件，压缩后保存到新文件。
    
    Args:
        input_file (str): 输入HTML文件路径
        output_file (str): 输出HTML文件路径
    """
    with open(input_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    compressed_html = compress_html(html_content)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(compressed_html)
