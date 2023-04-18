from Mission.CasRel_process import sentence_Casrel
from Mission.NER_process import sentence_NER, bert_replace
from Mission.NER_model import Model
from Mission.model import CasRel


text1 = '周杰伦1979年1月18日出生于台湾省新北市，祖籍福建省泉州市永春县，中国台湾流行乐男歌手、音乐人、演员、导演、编剧，毕业于淡江中学。\
2000年,周杰伦发行首张个人专辑《Jay》。2001年,周杰伦发行的专辑《范特西》奠定其融合中西方音乐的风格。2002年,周杰伦举行“The One”世界巡回演唱会 [1]  。2003年,周杰伦成为美国《时代周刊》封面人物 [2]  。2004周杰伦年获得世界音乐大奖中国区最畅销艺人奖 [265]  。2005年周杰伦凭借动作片《头文字D》获得金马奖、金像奖最佳新人奖 [3]  。2006年起周杰伦连续三年获得世界音乐大奖中国区最畅销艺人奖 [4]  。2007年周杰伦自编自导的文艺片《不能说的秘密》获得金马奖年度台湾杰出电影奖 [5]  。\
2008年,周杰伦凭借歌曲《青花瓷》获得第19届金曲奖最佳作曲人奖。2009年,周杰伦入选美国CNN评出的“25位亚洲最具影响力人物” [6]  ，同年凭借专辑《魔杰座》获得第20届金曲奖最佳国语男歌手奖 [7]  。2010年周杰伦入选美国《Fast Company》评出的“全球百大创意人物”。2011年周杰伦凭借专辑《跨时代》再度获得金曲奖最佳国语男歌手奖，并且第四次获得金曲奖最佳国语专辑奖, 同年主演好莱坞电影《青蜂侠》。2012年周杰伦登福布斯中国名人榜榜首 [8]  。2014年周杰伦发行华语乐坛首张数字音乐专辑《哎呦，不错哦》。2021年周杰伦在央视春晚演唱歌曲《Mojito》 [92]  。\
演艺事业外，他还涉足商业、设计等领域。周杰伦2007年成立杰威尔有限公司 [10]  。周杰伦2011年担任华硕笔电设计师，并入股香港文化传信集团 [11]  。\
他热心公益慈善，多次向中国内地灾区捐款捐物。周杰伦2008年捐款援建希望小学 [12]  。周杰伦2014年担任中国禁毒宣传形象大使。'
text2 = '《偶像练习生》（英语：Idol Producer）是由爱奇艺出品，北京鱼子酱文化传播有限责任公司联合制作的偶像竞演养成类真人秀，张艺兴担任”全民制作人代表“，李荣浩担任音乐导师，王嘉尔和欧阳靖担任Rap导师，程潇和周洁琼担任舞蹈导师。 [1] \
节目从中国国内外87家经纪公司、练习生公司的1908位练习生中推荐选拔100位练习生，在4个月中进行封闭式训练及录制，最终由全民票选出优胜9人，组成偶像男团出道。\
节目于2018年1月19日起每周五晚20:00在爱奇艺首播 [2]  ，于2018年4月6日收官，最终蔡徐坤、陈立农、范丞丞、黄明昊、林彦俊、朱正廷、王子异、小鬼（王琳凯）、尤长靖组成九人男团NINE PERCENT正式出道。 [3]'
text3 = '《邪少兵王》的作者是冰火未央'


def process(text):
    obj_dict = []
    rel_dict = []
    entity_name = []
    entity_type = []
    relation_sub = []
    relation_obj = []
    relation_type = []
    sentences = [(sentence.strip()).replace('\n', '') for sentence in text.split('。')]
    for sentence in sentences:
        if sentence != '':
            print(sentence)
            sentence_NER(sentence, obj_dict)
            sentence_process = bert_replace(sentence, obj_dict)
            sentence_Casrel(sentence_process, obj_dict, rel_dict)
    for i, item in enumerate(obj_dict):
        print(i, item.name, item.type)
    for i, item in enumerate(rel_dict):
        print(i, item.sub, item.type, item.obj)
    for entity in obj_dict:
        entity_name.append(entity.name)
        entity_type.append(entity.type)
    for rel in rel_dict:
        relation_sub.append(rel.sub)
        relation_obj.append(rel.obj)
        relation_type.append(rel.type)
    return entity_name, entity_type, relation_sub, relation_type, relation_obj


if __name__ == '__main__':
    # 先将文段按句号分成句子
    process('《最伟大的作品》是周杰伦发行的音乐专辑')
