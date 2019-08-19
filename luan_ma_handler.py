# coding:utf-8 
__author__ = 'xxj'

import sys
import re
import lxml.etree
reload(sys)
sys.setdefaultencoding('utf-8')


def toutiao_handler():
    '''
    关于今日头条的新闻内容乱码处理
    如：'&quot;\u003Cdiv\u003E\u003Cp\u003E《Dota2》Ti9正在如火如荼地进行
    就是在获取到的今日头条的新闻内容中的标签转换为Unicode编码，而中文未编码。（所以需要对编码的部分进行解码，而其他内容不变）
    :return:
    '''
    con = '''
    '&quot;\u003Cdiv\u003E\u003Cp\u003E《Dota2》Ti9正在如火如荼地进行中，目前小组赛A组比赛已全部结束，B组出线形势也已明朗，A组晋级主赛事胜者组战队为：PSG.LGD、Secret、Newbee、TNC，B组晋级主赛事胜者组战队为：OG、VG、EG、VP。\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002Fc756e78b616849cb83c5c49c81477fe2\&quot; img_width&#x3D;\&quot;1438\&quot; img_height&#x3D;\&quot;899\&quot; alt&#x3D;\&quot;《Dota2》Ti9主赛事对阵表出炉：LGD、VG晋级胜者组\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp\u003E总积分情况如下：\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002Fc6a6f5cfe91d46b4b962875da1627811\&quot; img_width&#x3D;\&quot;513\&quot; img_height&#x3D;\&quot;738\&quot; alt&#x3D;\&quot;《Dota2》Ti9主赛事对阵表出炉：LGD、VG晋级胜者组\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp class&#x3D;\&quot;ql-align-center\&quot;\u003E\u003Cbr\u003E\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002F08cb5097e8c14acaa3edf269639ac73a\&quot; img_width&#x3D;\&quot;500\&quot; img_height&#x3D;\&quot;721\&quot; alt&#x3D;\&quot;《Dota2》Ti9主赛事对阵表出炉：LGD、VG晋级胜者组\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp\u003E第五至第八名四支战队晋级主赛事败者组，最后一名Chaos和NiP则遭到淘汰。\u003C\u002Fp\u003E\u003Cp\u003EV社工作人员Wykrhm也发布了Ti9主赛事对阵表。\u003C\u002Fp\u003E\u003Cdiv class&#x3D;\&quot;pgc-img\&quot;\u003E\u003Cimg src&#x3D;\&quot;http:\u002F\u002Fp1.pstatp.com\u002Flarge\u002Fpgc-image\u002Fb659c7479acd41ab973445875b062610\&quot; img_width&#x3D;\&quot;690\&quot; img_height&#x3D;\&quot;690\&quot; alt&#x3D;\&quot;《Dota2》Ti9主赛事对阵表出炉：LGD、VG晋级胜者组\&quot; inline&#x3D;\&quot;0\&quot;\u003E\u003Cp class&#x3D;\&quot;pgc-img-caption\&quot;\u003E\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E\u003Cp\u003E目前中国战队VG和LGD晋级胜者组，KG和RNG则进入败者组，希望西恩军团加油，期待他们的精彩表现！\u003C\u002Fp\u003E\u003C\u002Fdiv\u003E&quot;'.slice(6, -6),

    '''
    news_content = con.replace('.slice(6, -6),', '').replace('&quot;', '').strip().strip("'")
    news_content = re.sub(r'(\\u[\s\S]{4})', lambda x: x.group(1).decode("unicode-escape"),
                          news_content)     # 对内容中的编码的部分进行解码，未编码的部分保持不变（重点）
    news_content = ''.join(lxml.etree.HTML(news_content).xpath('//text()'))
    print news_content


def main():
    toutiao_handler()


if __name__ == '__main__':
    main()