from bs4 import BeautifulSoup
from matplotlib.pyplot import gcf
import io
from pathlib import Path
import win32com.client
import matplotlib.pyplot as plt

class Svg:
    visio = None
    def __init__(self,svg_path):
        self.svg_path = Path(svg_path).resolve()
    def to_vsd(self,vsdx_path = None,clipboard = False):
        if vsdx_path is None:
            vsdx_path = self.svg_path.with_suffix(".vsdx")
        else:
            vsdx_path = Path(vsdx_path)
        if Svg.visio is None:
            Svg.visio = win32com.client.Dispatch("Visio.Application")
            Svg.visio.Visible = False
        try:
            document = Svg.visio.Documents.Open(self.svg_path.resolve())
            if clipboard :
                act_win = Svg.visio.ActiveWindow
                # act_win.Page = document.Pages.Item(1)
                act_win.SelectAll()
                act_win.Selection.Copy()
            document.SaveAs(vsdx_path.resolve())
        except Exception as e:
            print(f"An error occurred: {e}")
        document.Close()
        return self

    @classmethod
    def exit(cls):
        if cls.visio:
            try:
                cls.visio.Quit()  # 退出Visio应用
            except Exception as e:
                print(f"Error while closing Visio: {e}")
            finally:
                cls.visio = None  # 清理Visio实例

import copy
import matplotlib_inline
from matplotlib.figure import Figure
class Fig:
    def __init__(self,fig):
        self.fig:Figure = copy.deepcopy(fig)
    def savefig(self,*args,**kwargs) -> Svg:
        kwargs['format'] = 'svg'
        fig = self.fig
        ax = fig.get_axes()[0]
        svg_buffer = io.BytesIO()
        fig.savefig(svg_buffer, **kwargs)
        svg_buffer.seek(0)
        svg_content = svg_buffer.read()
        cleaned_svg_window,flag_out = _svg_windows(svg_content)
        
        if flag_out is False:
            combined_svg_content = cleaned_svg_window
        else:
            bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            ax.set_axis_off()
            if ax.get_legend():
                ax.get_legend().remove()
            kwargs['bbox_inches'] = bbox
            svg_buffer = io.BytesIO()
            fig.savefig(svg_buffer, **kwargs)
            svg_buffer.seek(0)
            svg_content = svg_buffer.read()
            svg_content = _svg_content(svg_content)
            combined_svg_content = _combined_svg(cleaned_svg_window,svg_content)
        combined_svg_content = _svg_clean(combined_svg_content)
        plt.close(fig)
        fname = Path(args[0]).with_suffix(".svg")
        with open(fname, 'w', encoding='utf-8') as file:
            file.write(combined_svg_content)
        return Svg(fname)

# 删除svg不必要数据
def _svg_clean(svg_content):
    soup = BeautifulSoup(svg_content, 'xml')
    for metadata_tag in soup.find_all('metadata'):
        metadata_tag.decompose()
    for style_tag in soup.find_all('style'):
        style_tag.decompose()
    for tag in soup.find_all(True):  # True 表示匹配所有标签
        if 'clip-path' in tag.attrs:  # 检查标签是否包含 clip-path 属性
            del tag['clip-path']  # 删除该属性
    for g_tag in soup.find_all('g'):
        if g_tag.get('id') == 'ax':
            continue
        has_relevant_id = any(k in g_tag.get('id', '') for k in ['legend', 'figure', 'axes'])
        has_single_child = len(g_tag.find_all()) <= 1
        if has_relevant_id or has_single_child:
            g_tag.unwrap()  # 展开该标签
    cleaned_svg_content = soup.prettify()
    return cleaned_svg_content

def _svg_windows(svg_content):
    soup = BeautifulSoup(svg_content, 'xml')
    flag_out = False
    for g_tag in soup.find_all('g', id='out'):
        g_tag.decompose()
        flag_out = True
    cleaned_svg_content = soup.prettify()
    return cleaned_svg_content,flag_out

def _svg_content(svg_content):
    soup = BeautifulSoup(svg_content, 'xml')
    svg_root = soup.find('svg')
    out_elements = soup.find_all('g', id='out')
    svg_root.clear()
    if len(out_elements) == 0:
        return str(soup)
    for out_element in out_elements:
        for path_tag in out_element.find_all('path'):
            style = path_tag.get('style', '')
            if 'stroke-linecap' in style:
                style = style.replace('stroke-linecap: square', 'stroke-linecap: butt')
                path_tag['style'] = style
    ax_group = soup.new_tag('g', id='ax')
    for out_element in out_elements:
        ax_group.append(out_element.extract())
    svg_root.append(ax_group)
    return str(soup)

def _combined_svg(window,content):
    window_soup = BeautifulSoup(window, 'xml')
    content_soup = BeautifulSoup(content, 'xml')
    rect_tag = window_soup.find('clipPath').find('rect')
    ax_tag = content_soup.find('g',id='ax')
    if ax_tag:
        ax_tag.attrs['transform'] = f"translate({rect_tag.attrs['x']}, {rect_tag.attrs['y']})"
        window_soup.find('g', {'id': 'axes_1'}).insert(2, ax_tag)
    # for g_tag in window_soup.find_all('g'):
    #     if g_tag.get('id') != 'ax':
    #         g_tag.unwrap()
    return window_soup.prettify()

def savefig(*args,**kwargs) -> Svg:
    fig = gcf()
    return Fig(fig).savefig(*args,**kwargs)

if __name__ == "__main__":
    import matplotlib_utils
    plt.plot([1,2,3],[3,2,4])
    plt.plot([1,2,3],[5,15,3],gid='out')
    plt.ylim([0,10])
    savefig("test1.svg").to_vsd(clipboard=True).exit()

    fig,ax = plt.subplots()
    ax.plot([1,2,3],[3,2,4],label='inax')
    ax.plot([1,2,3],[5,15,3],label='outax',gid='out')
    ax.set_ylim([0,10])
    ax.legend()
    Fig(fig).savefig("test2.svg").to_vsd(clipboard=True).exit()
