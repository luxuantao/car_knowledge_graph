import sys
sys.path.append("..")
from toolkit.pre_load import thuFactory, neo4jconn, domain_ner_dict
from toolkit.nlp_ner import get_ner, tempword, get_detail_ner_info, get_ner_info


# 中文分词+词性标注+命名实体识别
def ner_post(key):
    ctx = {}
    thu1 = thuFactory
    # 中文分词:提前移除空格
    key = key.strip()
    TagList = thu1.cut(key, text=False)
    text = ""
    # 命名实体识别
    ner_list = get_ner(key)
    # 遍历输出
    for pair in ner_list:
        if pair[1] == 0:
            text += pair[0]
            continue
        if tempword(pair[1]):
            text += "<a href='#'  data-original-title='" + get_ner_info(pair[
                                                                            1]) + "(暂无资料)'  data-placement='top' data-trigger='hover' data-content='" + get_detail_ner_info(
                pair[1]) + "' class='popovers'>" + pair[0] + "</a>"
            continue

        text += "<a href='detail.html?title=" + pair[0] + "'  data-original-title='" + get_ner_info(
            pair[1]) + "'  data-placement='top' data-trigger='hover' data-content='" + get_detail_ner_info(
            pair[1]) + "' class='popovers'>" + pair[0] + "</a>"

    ctx['rlt'] = text

    seg_word = ""
    length = len(TagList)
    # 设置显示格式
    for t in TagList:
        seg_word += t[0] + " <strong><small>[" + t[1] + "]</small></strong> "
    seg_word += ""
    ctx['seg_word'] = seg_word

    return ctx
