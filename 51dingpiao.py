#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import cookielib
import urllib
import urllib2
import time
import sys
import re
from bs4 import BeautifulSoup
import ConfigParser
import codecs
import random
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

station_dict = {}

#------------------------------------------------------------------------------
# Print delimiter
def printDelimiter():
  print '-'*100

#------------------------------------------------------------------------------
# Station init
# 全部站点(总共2167个站), 数据来自: https://dynamic.12306.cn/otsweb/js/common/station_name.js?version=5.94
# 每个站的格式如下:
# @bjb|北京北|VAP|beijingbei|bjb|0   ---> @拼音缩写三位|站点名称|编码|拼音|拼音缩写|序号
def stationInit():
  station_names = u'@bjb|北京北|VAP|beijingbei|bjb|0@bjd|北京东|BOP|beijingdong|bjd|1@bji|北京|BJP|beijing|bj|2@bjn|北京南|VNP|beijingnan|bjn|3@bjx|北京西|BXP|beijingxi|bjx|4@cqb|重庆北|CUW|chongqingbei|cqb|5@cqi|重庆|CQW|chongqing|cq|6@cqn|重庆南|CRW|chongqingnan|cqn|7@sha|上海|SHH|shanghai|sh|8@shn|上海南|SNH|shanghainan|shn|9@shq|上海虹桥|AOH|shanghaihongqiao|shhq|10@shx|上海西|SXH|shanghaixi|shx|11@tjb|天津北|TBP|tianjinbei|tjb|12@tji|天津|TJP|tianjin|tj|13@tjn|天津南|TIP|tianjinnan|tjn|14@tjx|天津西|TXP|tianjinxi|tjx|15@cch|长春|CCT|changchun|cc|16@ccn|长春南|CET|changchunnan|ccn|17@ccx|长春西|CRT|changchunxi|ccx|18@cdd|成都东|ICW|chengdudong|cdd|19@cdn|成都南|CNW|chengdunan|cdn|20@cdu|成都|CDW|chengdu|cd|21@csh|长沙|CSQ|changsha|cs|22@csn|长沙南|CWQ|changshanan|csn|23@fzh|福州|FZS|fuzhou|fz|24@fzn|福州南|FYS|fuzhounan|fzn|25@gya|贵阳|GIW|guiyang|gy|26@gzb|广州北|GBQ|guangzhoubei|gzb|27@gzd|广州东|GGQ|guangzhoudong|gzd|28@gzh|广州|GZQ|guangzhou|gz|29@gzn|广州南|IZQ|guangzhounan|gzn|30@heb|哈尔滨|HBB|haerbin|heb|31@hed|哈尔滨东|VBB|harbindong|hebd|32@hex|哈尔滨西|VAB|haerbinxi|hebx|33@hfe|合肥|HFH|hefei|hf|34@hhd|呼和浩特东|NDC|huhehaotedong|hhhtd|35@hht|呼和浩特|HHC|hohhot|hhht|36@hkd|海口东|HMQ|haikoudong|hkd|37@hko|海口|VUQ|haikou|hk|38@hzd|杭州东|HGH|hangzhoudong|hzd|39@hzh|杭州|HZH|hangzhou|hz|40@hzn|杭州南|XHH|hangzhounan|hzn|41@jna|济南|JNK|jinan|jn|42@jnd|济南东|JAK|jinandong|jnd|43@jnx|济南西|JGK|jinanxi|jnx|44@kmi|昆明|KMM|kunming|km|45@kmx|昆明西|KXM|kunmingxi|kmx|46@lsa|拉萨|LSO|lasa|ls|47@lzd|兰州东|LVJ|lanzhoudong|lzd|48@lzh|兰州|LZJ|lanzhou|lz|49@lzx|兰州西|LAJ|lanzhouxi|lzx|50@nch|南昌|NCG|nanchang|nc|51@nji|南京|NJH|nanjing|nj|52@njn|南京南|NKH|nanjingnan|njn|53@nni|南宁|NNZ|nanning|nn|54@sjb|石家庄北|VVP|shijiazhuangbei|sjzb|55@sjz|石家庄|SJP|shijiazhuang|sjz|56@sya|沈阳|SYT|shenyang|sy|57@syb|沈阳北|SBT|shenyangbei|syb|58@syd|沈阳东|SDT|shenyangdong|syd|59@tyb|太原北|TBV|taiyuanbei|tyb|60@tyd|太原东|TDV|taiyuandong|tyd|61@tyu|太原|TYV|taiyuan|ty|62@wha|武汉|WHN|wuhan|wh|63@wjx|王家营西|KNM|wangjiayingxi|wjyx|64@wlq|乌鲁木齐|WMR|wulumuqi|wlmq|65@xab|西安北|EAY|xianbei|xab|66@xan|西安|XAY|xian|xa|67@xan|西安南|CAY|xiannan|xan|68@xnx|西宁西|XXO|xiningxi|xnx|69@ych|银川|YIJ|yinchuan|yc|70@zzh|郑州|ZZF|zhengzhou|zz|71@aes|阿尔山|ART|aershan|aes|72@aka|安康|AKY|ankang|ak|73@aks|阿克苏|ASR|akesu|aks|74@alh|阿里河|AHX|alihe|alh|75@alk|阿拉山口|AKR|alashankou|alsk|76@api|安平|APT|anping|ap|77@aqi|安庆|AQH|anqing|aq|78@ash|安顺|ASW|anshun|as|79@ash|鞍山|AST|anshan|as|80@aya|安阳|AYF|anyang|ay|81@ban|北安|BAB|beian|ba|82@bbu|蚌埠|BBH|bengbu|bb|83@bch|白城|BCT|baicheng|bc|84@bha|北海|BHZ|beihai|bh|85@bhe|白河|BEL|baihe|bh|86@bji|白涧|BAP|baijian|bj|87@bji|宝鸡|BJY|baoji|bj|88@bji|滨江|BJB|binjiang|bj|89@bkt|博克图|BKX|bugt|bkt|90@bse|百色|BIZ|baise|bs|91@bss|白山市|HJL|baishanshi|bss|92@bta|北台|BTT|beitai|bt|93@btd|包头东|BDC|baotoudong|btd|94@bto|包头|BTC|baotou|bt|95@bts|北屯市|BXR|beitunshi|bts|96@bxi|本溪|BXT|benxi|bx|97@byb|白云鄂博|BEC|bayanobo|byeb|98@byx|白银西|BXJ|baiyinxi|byx|99@bzh|亳州|BZH|bozhou|bz|100@cbi|赤壁|CBN|chibi|cb|101@cde|常德|VGQ|changde|cd|102@cde|承德|CDP|chengde|cd|103@cdi|长甸|CDT|changdian|cd|104@cfe|赤峰|CFD|chifeng|cf|105@cli|茶陵|CDG|chaling|cl|106@cna|苍南|CEH|cangnan|cn|107@cpi|昌平|CPP|changping|cp|108@cre|崇仁|CRG|chongren|cr|109@ctu|昌图|CTT|changtu|ct|110@ctz|长汀镇|CDB|changtingzhen|ctz|111@cxi|崇信|CIJ|chongxin|cx|112@cxi|曹县|CXK|caoxian|cx|113@cxi|楚雄|COM|chuxiong|cx|114@cxt|陈相屯|CXT|chenxiangtun|cxt|115@czb|长治北|CBF|changzhibei|czb|116@czh|长征|CZJ|changzheng|cz|117@czh|池州|IYH|chizhou|cz|118@czh|常州|CZH|changzhou|cz|119@czh|郴州|CZQ|chenzhou|cz|120@czh|长治|CZF|changzhi|cz|121@czh|沧州|COP|cangzhou|cz|122@czu|崇左|CZZ|chongzuo|cz|123@dab|大安北|RNT|daanbei|dab|124@dch|大成|DCT|dacheng|dc|125@ddo|丹东|DUT|dandong|dd|126@dfh|东方红|DFB|dongfanghong|dfh|127@dgd|东莞东|DMQ|dongguandong|dgd|128@dhs|大虎山|DHD|dahushan|dhs|129@dhu|敦煌|DHJ|dunhuang|dh|130@dhu|敦化|DHL|dunhua|dh|131@dhu|德惠|DHT|dehui|dh|132@djc|东京城|DJB|dongjingcheng|djc|133@dji|大涧|DFP|dajian|dj|134@djy|都江堰|DDW|dujiangyan|djy|135@dlb|大连北|DFT|dalianbei|dlb|136@dli|大理|DKM|dali|dl|137@dli|大连|DLT|dalian|dl|138@dna|定南|DNG|dingnan|dn|139@dqi|大庆|DZX|daqing|dq|140@dsh|东胜|DOC|dongsheng|ds|141@dsq|大石桥|DQT|dashiqiao|dsq|142@dto|大同|DTV|datong|dt|143@dyi|东营|DPK|dongying|dy|144@dys|大杨树|DUX|dayangshu|dys|145@dyu|都匀|RYW|duyun|dy|146@dzh|邓州|DOF|dengzhou|dz|147@dzh|达州|RXW|dazhou|dz|148@dzh|德州|DZP|dezhou|dz|149@ejn|额济纳|EJC|ejina|ejn|150@eli|二连|RLC|erlian|el|151@esh|恩施|ESN|enshi|es|152@fcg|防城港|FEZ|fangchenggang|fcg|153@fdi|福鼎|FES|fuding|fd|154@fld|风陵渡|FLV|fenglingdu|fld|155@fli|涪陵|FLW|fuling|fl|156@flj|富拉尔基|FRX|fulaerji|flej|157@fsb|抚顺北|FET|fushunbei|fsb|158@fsh|佛山|FSQ|foshan|fs|159@fxi|阜新|FXD|fuxin|fx|160@fya|阜阳|FYH|fuyang|fy|161@gem|格尔木|GRO|geermu|gem|162@gha|广汉|GHW|guanghan|gh|163@gji|古交|GJV|gujiao|gj|164@glb|桂林北|GBZ|guilinbei|glb|165@gli|古莲|GRX|gulian|gl|166@gli|桂林|GLZ|guilin|gl|167@gsh|固始|GXN|gushi|gs|168@gsh|广水|GSN|guangshui|gs|169@gta|干塘|GNJ|gantang|gt|170@gyu|广元|GYW|guangyuan|gy|171@gzh|赣州|GZG|ganzhou|gz|172@gzl|公主岭|GLT|gongzhuling|gzl|173@gzn|公主岭南|GBT|gongzhulingnan|gzln|174@han|淮安|AUH|huaian|ha|175@hbe|鹤北|HMB|hebei|hb|176@hbe|淮北|HRH|huaibei|hb|177@hbi|淮滨|HVN|huaibin|hb|178@hbi|河边|HBV|hebian|hb|179@hch|潢川|KCN|huangchuan|hc|180@hch|韩城|HCY|hancheng|hc|181@hda|邯郸|HDP|handan|hd|182@hdz|横道河子|HDB|hengdaohezi|hdhz|183@hga|鹤岗|HGB|hegang|hg|184@hgt|皇姑屯|HTT|huanggutun|hgt|185@hgu|红果|HEM|hongguo|hg|186@hhe|黑河|HJB|heihe|hh|187@hhu|怀化|HHQ|huaihua|hh|188@hko|汉口|HKN|hankou|hk|189@hld|葫芦岛|HLD|huludao|hld|190@hle|海拉尔|HRX|hailaer|hle|191@hll|霍林郭勒|HWD|huolinguole|hlgl|192@hlu|海伦|HLB|hailun|hl|193@hma|侯马|HMV|houma|hm|194@hmi|哈密|HMR|hami|hm|195@hna|淮南|HAH|huainan|hn|196@hna|桦南|HNB|huanan|hn|197@hnx|海宁西|EUH|hainingxi|hnx|198@hqi|鹤庆|HQM|heqing|hq|199@hrb|怀柔北|HBP|huairoubei|hrb|200@hro|怀柔|HRP|huairou|hr|201@hsd|黄石东|OSN|huangshidong|hsd|202@hsh|华山|HSY|huashan|hs|203@hsh|黄石|HSN|huangshi|hs|204@hsh|黄山|HKH|huangshan|hs|205@hsh|衡水|HSP|hengshui|hs|206@hya|衡阳|HYQ|hengyang|hy|207@hze|菏泽|HIK|heze|hz|208@hzh|贺州|HXZ|hezhou|hz|209@hzh|汉中|HOY|hanzhong|hz|210@hzh|惠州|HCQ|huizhou|hz|211@jan|吉安|VAG|jian|ja|212@jan|集安|JAL|jian|ja|213@jbc|江边村|JBG|jiangbiancun|jbc|214@jch|晋城|JCF|jincheng|jc|215@jcj|金城江|JJZ|jinchengjiang|jcj|216@jdz|景德镇|JCG|jingdezhen|jdz|217@jfe|嘉峰|JFF|jiafeng|jf|218@jgq|加格达奇|JGX|jagdaqi|jgdq|219@jgs|井冈山|JGG|jinggangshan|jgs|220@jhe|蛟河|JHL|jiaohe|jh|221@jhn|金华南|RNH|jinhuanan|jhn|222@jhx|金华西|JBH|jinhuaxi|jhx|223@jji|九江|JJG|jiujiang|jj|224@jli|吉林|JLL|jilin|jl|225@jme|荆门|JMN|jingmen|jm|226@jms|佳木斯|JMB|jiamusi|jms|227@jni|济宁|JIK|jining|jn|228@jnn|集宁南|JAC|jiningnan|jnn|229@jqu|酒泉|JQJ|jiuquan|jq|230@jsh|江山|JUH|jiangshan|js|231@jsh|吉首|JIQ|jishou|js|232@jta|九台|JTL|jiutai|jt|233@jts|镜铁山|JVJ|jingtieshan|jts|234@jxi|鸡西|JXB|jixi|jx|235@jxi|蓟县|JKP|jixian|jx|236@jxx|绩溪县|JRH|jixixian|jxx|237@jyg|嘉峪关|JGJ|jiayuguan|jyg|238@jyo|江油|JFW|jiangyou|jy|239@jzh|锦州|JZD|jinzhou|jz|240@jzh|金州|JZT|jinzhou|jz|241@kel|库尔勒|KLR|kuerle|kel|242@kfe|开封|KFF|kaifeng|kf|243@kla|岢岚|KLV|kelan|kl|244@kli|凯里|KLW|kaili|kl|245@ksh|喀什|KSR|kashi|ks|246@ksn|昆山南|KNH|kunshannan|ksn|247@ktu|奎屯|KTR|kuitun|kt|248@kyu|开原|KYT|kaiyuan|ky|249@lan|六安|UAH|luan|la|250@lba|灵宝|LBF|lingbao|lb|251@lcg|芦潮港|UCH|luchaogang|lcg|252@lch|隆昌|LCW|longchang|lc|253@lch|陆川|LKZ|luchuan|lc|254@lch|利川|LCN|lichuan|lc|255@lch|临川|LCG|linchuan|lc|256@lch|潞城|UTP|lucheng|lc|257@lda|鹿道|LDL|ludao|ld|258@ldi|娄底|LDQ|loudi|ld|259@lfe|临汾|LFV|linfen|lf|260@lgz|良各庄|LGP|lianggezhuang|lgz|261@lhe|临河|LHC|linhe|lh|262@lhe|漯河|LON|luohe|lh|263@lhu|绿化|LWJ|lvhua|lh|264@lhu|隆化|UHP|longhua|lh|265@lji|丽江|LHM|lijiang|lj|266@lji|临江|LQL|linjiang|lj|267@lji|龙井|LJL|longjing|lj|268@lli|吕梁|LHV|lvliang|ll|269@lli|醴陵|LLG|liling|ll|270@lln|柳林南|LKV|liulinnan|lln|271@lpi|滦平|UPP|luanping|lp|272@lps|六盘水|UMW|liupanshui|lps|273@lqi|灵丘|LVV|lingqiu|lq|274@lsh|旅顺|LST|lvshun|ls|275@lxi|陇西|LXJ|longxi|lx|276@lxi|澧县|LEQ|lixian|lx|277@lxi|兰溪|LWH|lanxi|lx|278@lxi|临西|UEP|linxi|lx|279@lya|耒阳|LYQ|leiyang|ly|280@lya|洛阳|LYF|luoyang|ly|281@lya|龙岩|LYS|longyan|ly|282@lyd|洛阳东|LDF|luoyangdong|lyd|283@lyd|连云港东|UKH|lianyungangdong|lygd|284@lyi|临沂|LVK|linyi|ly|285@lym|洛阳龙门|LLF|luoyanglongmen|lylm|286@lyu|柳园|DHR|liuyuan|ly|287@lyu|凌源|LYD|lingyuan|ly|288@lyu|辽源|LYL|liaoyuan|ly|289@lzh|立志|LZX|lizhi|lz|290@lzh|柳州|LZZ|liuzhou|lz|291@lzh|辽中|LZD|liaozhong|lz|292@mch|麻城|MCN|macheng|mc|293@mdh|免渡河|MDX|mianduhe|mdh|294@mdj|牡丹江|MDB|mudanjiang|mdj|295@meg|莫尔道嘎|MRX|mordaga|medg|296@mgu|满归|MHX|mangui|mg|297@mgu|明光|MGH|mingguang|mg|298@mhe|漠河|MVX|mohe|mh|299@mji|梅江|MKQ|meijiang|mj|300@mmd|茂名东|MDQ|maomingdong|mmd|301@mmi|茂名|MMZ|maoming|mm|302@msh|密山|MSB|mishan|ms|303@msj|马三家|MJT|masanjia|msj|304@mwe|麻尾|VAW|mawei|mw|305@mya|绵阳|MYW|mianyang|my|306@mzh|梅州|MOQ|meizhou|mz|307@mzl|满洲里|MLX|manzhouli|mzl|308@nbd|宁波东|NVH|ningbodong|nbd|309@nch|南岔|NCB|nancha|nc|310@nch|南充|NCW|nanchong|nc|311@nda|南丹|NDZ|nandan|nd|312@ndm|南大庙|NMP|nandamiao|ndm|313@nfe|南芬|NFT|nanfen|nf|314@nhe|讷河|NHX|nehe|nh|315@nji|嫩江|NGX|nenjiang|nj|316@nji|内江|NJW|neijiang|nj|317@npi|南平|NPS|nanping|np|318@nto|南通|NUH|nantong|nt|319@nya|南阳|NFF|nanyang|ny|320@nzs|碾子山|NZX|nianzishan|nzs|321@pds|平顶山|PEN|pingdingshan|pds|322@pji|盘锦|PVD|panjin|pj|323@pli|平凉|PIJ|pingliang|pl|324@pln|平凉南|POJ|pingliangnan|pln|325@pqu|平泉|PQP|pingquan|pq|326@psh|坪石|PSQ|pingshi|ps|327@pxi|萍乡|PXG|pingxiang|px|328@pxi|凭祥|PXZ|pingxiang|px|329@pxx|郫县西|PCW|pixianxi|pxx|330@pzh|攀枝花|PRW|panzhihua|pzh|331@qch|蕲春|QRN|qichun|qc|332@qcs|青城山|QSW|qingchengshan|qcs|333@qda|青岛|QDK|qingdao|qd|334@qhc|清河城|QYP|qinghecheng|qhc|335@qji|黔江|QNW|qianjiang|qj|336@qji|曲靖|QJM|qujing|qj|337@qjz|前进镇|QEB|qianjinzhen|qjz|338@qqe|齐齐哈尔|QHX|qiqihaer|qqhe|339@qth|七台河|QTB|qitaihe|qth|340@qxi|沁县|QVV|qinxian|qx|341@qzd|泉州东|QRS|quanzhoudong|qzd|342@qzh|泉州|QYS|quanzhou|qz|343@qzh|衢州|QEH|quzhou|qz|344@ran|融安|RAZ|rongan|ra|345@rjg|汝箕沟|RQJ|rujigou|rqg|346@rji|瑞金|RJG|ruijin|rj|347@rzh|日照|RZK|rizhao|rz|348@scp|双城堡|SCB|shuangchengpu|scb|349@sfh|绥芬河|SFB|suifenhe|sfh|350@sgd|韶关东|SGQ|shaoguandong|sgd|351@shg|山海关|SHD|shanhaiguan|shg|352@shu|绥化|SHB|suihua|sh|353@sjf|三间房|SFX|sanjianfang|sjf|354@sjt|苏家屯|SXT|sujiatun|sjt|355@sla|舒兰|SLL|shulan|sl|356@smi|三明|SMS|sanming|sm|357@smu|神木|OMY|shenmu|sm|358@smx|三门峡|SMF|sanmenxia|smx|359@sna|商南|ONY|shangnan|sn|360@sni|遂宁|NIW|suining|sn|361@spi|四平|SPT|siping|sp|362@sqi|商丘|SQF|shangqiu|sq|363@sra|上饶|SRG|shangrao|sr|364@ssh|韶山|SSQ|shaoshan|ss|365@sso|宿松|OAH|susong|ss|366@sto|汕头|OTQ|shantou|st|367@swu|邵武|SWS|shaowu|sw|368@sxi|涉县|OEP|shexian|sx|369@sya|三亚|SEQ|sanya|sy|370@sya|邵阳|SYQ|shaoyang|sy|371@sya|十堰|SNN|shiyan|sy|372@sys|双鸭山|SSB|shuangyashan|sys|373@syu|松原|VYT|songyuan|sy|374@szh|深圳|SZQ|shenzhen|sz|375@szh|苏州|SZH|suzhou|sz|376@szh|随州|SZN|suizhou|sz|377@szh|宿州|OXH|suzhou|sz|378@szh|朔州|SUV|shuozhou|sz|379@szx|深圳西|OSQ|shenzhenxi|szx|380@tba|塘豹|TBQ|tangbao|tb|381@teq|塔尔气|TVX|tarqi|teq|382@tgu|潼关|TGY|tongguan|tg|383@tgu|塘沽|TGP|tanggu|tg|384@the|塔河|TXX|tahe|th|385@thu|通化|THL|tonghua|th|386@tla|泰来|TLX|tailai|tl|387@tlf|吐鲁番|TFR|tulufan|tlf|388@tli|通辽|TLD|tongliao|tl|389@tli|铁岭|TLT|tieling|tl|390@tlz|陶赖昭|TPT|taolaizhao|tlz|391@tme|图们|TML|tumen|tm|392@tre|铜仁|RDQ|tongren|tr|393@tsb|唐山北|FUP|tangshanbei|tsb|394@tsf|田师府|TFT|tianshifu|tsf|395@tsh|泰山|TAK|taishan|ts|396@tsh|天水|TSJ|tianshui|ts|397@tsh|唐山|TSP|tangshan|ts|398@typ|通远堡|TYT|tongyuanpu|tyb|399@tys|太阳升|TQT|taiyangsheng|tys|400@tzh|泰州|UTH|taizhou|tz|401@tzi|桐梓|TZW|tongzi|tz|402@tzx|通州西|TAP|tongzhouxi|tzx|403@wch|五常|WCB|wuchang|wc|404@wch|武昌|WCN|wuchang|wc|405@wfd|瓦房店|WDT|wafangdian|wfd|406@whi|威海|WKK|weihai|wh|407@whu|芜湖|WHH|wuhu|wh|408@whx|乌海西|WXC|wuhaixi|whx|409@wjt|吴家屯|WJT|wujiatun|wjt|410@wlo|武隆|WLW|wulong|wl|411@wlt|乌兰浩特|WWT|ulanhot|wlht|412@wna|渭南|WNY|weinan|wn|413@wsh|威舍|WSM|weishe|ws|414@wts|歪头山|WIT|waitoushan|wts|415@wwe|武威|WUJ|wuwei|ww|416@wwn|武威南|WWJ|wuweinan|wwn|417@wxi|无锡|WXH|wuxi|wx|418@wxi|乌西|WXR|wuxi|wx|419@wyl|乌伊岭|WPB|wuyiling|wyl|420@wys|武夷山|WAS|wuyishan|wys|421@wyu|万源|WYY|wanyuan|wy|422@wzh|万州|WYW|wanzhou|wz|423@wzh|梧州|WZZ|wuzhou|wz|424@wzh|温州|RZH|wenzhou|wz|425@wzn|温州南|VRH|wenzhounan|wzn|426@xch|西昌|ECW|xichang|xc|427@xch|许昌|XCF|xuchang|xc|428@xcn|西昌南|ENW|xichangnan|xcn|429@xfa|香坊|XFB|xiangfang|xf|430@xga|轩岗|XGV|xuangang|xg|431@xgu|兴国|EUG|xingguo|xg|432@xha|宣汉|XHY|xuanhan|xh|433@xhu|新会|EFQ|xinhui|xh|434@xhu|新晃|XLQ|xinhuang|xh|435@xlt|锡林浩特|XTC|xilinhaote|xlht|436@xlx|兴隆县|EXP|xinglongxian|xlx|437@xmb|厦门北|XKS|xiamenbei|xmb|438@xme|厦门|XMS|xiamen|xm|439@xmq|厦门高崎|XBS|xiamengaoqi|xmgq|440@xsh|秀山|ETW|xiushan|xs|441@xsh|小市|XST|xiaoshi|xs|442@xta|向塘|XTG|xiangtang|xt|443@xwe|宣威|XWM|xuanwei|xw|444@xxi|新乡|XXF|xinxiang|xx|445@xya|信阳|XUN|xinyang|xy|446@xya|咸阳|XYY|xianyang|xy|447@xya|襄阳|XFN|xiangyang|xy|448@xyc|熊岳城|XYT|xiongyuecheng|xyc|449@xyi|兴义|XRZ|xingyi|xy|450@xyi|新沂|VIH|xinyi|xy|451@xyu|新余|XUG|xinyu|xy|452@xzh|徐州|XCH|xuzhou|xz|453@yan|延安|YWY|yanan|ya|454@ybi|宜宾|YBW|yibin|yb|455@ybn|亚布力南|YWB|yabulinan|ybln|456@ybs|叶柏寿|YBD|yebaishou|ybs|457@ycd|宜昌东|HAN|yichangdong|ycd|458@ych|永川|YCW|yongchuan|yc|459@ych|宜春|YCG|yichun|yc|460@ych|宜昌|YCN|yichang|yc|461@ych|盐城|AFH|yancheng|yc|462@ych|运城|YNV|yuncheng|yc|463@ych|伊春|YCB|yichun|yc|464@yci|榆次|YCV|yuci|yc|465@ycu|杨村|YBP|yangcun|yc|466@yes|伊尔施|YET|yirshi|yes|467@yga|燕岗|YGW|yangang|yg|468@yji|永济|YIV|yongji|yj|469@yji|延吉|YJL|yanji|yj|470@yko|营口|YKT|yingkou|yk|471@yks|牙克石|YKX|yakeshi|yks|472@yli|阎良|YNY|yanliang|yl|473@yli|玉林|YLZ|yulin|yl|474@yli|榆林|ALY|yulin|yl|475@ymp|一面坡|YPB|yimianpo|ymp|476@yni|伊宁|YMR|yining|yn|477@ypg|阳平关|YAY|yangpingguan|ypg|478@ypi|玉屏|YZW|yuping|yp|479@ypi|原平|YPV|yuanping|yp|480@yqi|延庆|YNP|yanqing|yq|481@yqq|阳泉曲|YYV|yangquanqu|yqq|482@yqu|玉泉|YQB|yuquan|yq|483@yqu|阳泉|AQP|yangquan|yq|484@ysh|玉山|YNG|yushan|ys|485@ysh|营山|NUW|yingshan|ys|486@ysh|燕山|AOP|yanshan|ys|487@ysh|榆树|YRT|yushu|ys|488@yta|鹰潭|YTG|yingtan|yt|489@yta|烟台|YAK|yantai|yt|490@yth|伊图里河|YEX|yitulihe|ytlh|491@ytx|玉田县|ATP|yutianxian|ytx|492@ywu|义乌|YWH|yiwu|yw|493@yxi|阳新|YON|yangxin|yx|494@yxi|义县|YXD|yixian|yx|495@yya|益阳|AEQ|yiyang|yy|496@yya|岳阳|YYQ|yueyang|yy|497@yzh|永州|AOQ|yongzhou|yz|498@yzh|扬州|YLH|yangzhou|yz|499@zbo|淄博|ZBK|zibo|zb|500@zcd|镇城底|ZDV|zhenchengdi|zcd|501@zgo|自贡|ZGW|zigong|zg|502@zha|珠海|ZHQ|zhuhai|zh|503@zhb|珠海北|ZIQ|zhuhaibei|zhb|504@zji|湛江|ZJZ|zhanjiang|zj|505@zji|镇江|ZJH|zhenjiang|zj|506@zjj|张家界|DIQ|zhangjiajie|zjj|507@zjk|张家口|ZKP|zhangjiakou|zjk|508@zjn|张家口南|ZMP|zhangjiakounan|zjkn|509@zko|周口|ZKN|zhoukou|zk|510@zlm|哲里木|ZLC|zhelimu|zlm|511@zlt|扎兰屯|ZTX|zhalantun|zlt|512@zmd|驻马店|ZDN|zhumadian|zmd|513@zqi|肇庆|ZVQ|zhaoqing|zq|514@zsz|周水子|ZIT|zhoushuizi|zsz|515@zto|昭通|ZDW|zhaotong|zt|516@zwe|中卫|ZWJ|zhongwei|zw|517@zya|资阳|ZYW|ziyang|zy|518@zyi|遵义|ZIW|zunyi|zy|519@zzh|枣庄|ZEK|zaozhuang|zz|520@zzh|资中|ZZW|zizhong|zz|521@zzh|株洲|ZZQ|zhuzhou|zz|522@zzx|枣庄西|ZFK|zaozhuangxi|zzx|523@aax|昂昂溪|AAX|angangxi|aax|524@ach|阿城|ACB|acheng|ac|525@ada|安达|ADX|anda|ad|526@adi|安定|ADP|anding|ad|527@agu|安广|AGT|anguang|ag|528@ahe|艾河|AHP|aihe|ah|529@ahu|安化|PKQ|anhua|ah|530@ajc|艾家村|AJJ|aijiacun|ajc|531@aji|鳌江|ARH|aojiang|aj|532@aji|安家|AJB|anjia|aj|533@aji|阿金|AJD|ajin|aj|534@akt|阿克陶|AER|aketao|akt|535@aky|安口窑|AYY|ankouyao|aky|536@alg|敖力布告|ALD|aolibugao|albg|537@alo|安龙|AUZ|anlong|al|538@als|阿龙山|ASX|alongshan|als|539@alu|安陆|ALN|anlu|al|540@ame|阿木尔|JTX|amuer|ame|541@anz|阿南庄|AZM|ananzhuang|anz|542@aqx|安庆西|APH|anqingxi|aqx|543@asx|鞍山西|AXT|anshanxi|asx|544@ata|安塘|ATV|antang|at|545@atb|安亭北|ASH|antingbei|atb|546@ats|阿图什|ATR|atushi|ats|547@atu|安图|ATL|antu|at|548@axi|安溪|AXS|anxi|ax|549@bao|博鳌|BWQ|boao|ba|550@bbg|白壁关|BGV|baibiguan|bbg|551@bbn|蚌埠南|BMH|bengbunan|bbn|552@bch|巴楚|BCR|bachu|bc|553@bch|板城|BUP|bancheng|bc|554@bdh|北戴河|BEP|beidaihe|bdh|555@bdi|保定|BDP|baoding|bd|556@bdi|宝坻|BPP|baodi|bd|557@bdl|八达岭|ILP|badaling|bdl|558@bdo|巴东|BNN|badong|bd|559@bgu|柏果|BGM|baiguo|bg|560@bha|布海|BUT|buhai|bh|561@bhd|白河东|BIY|baihedong|bhd|562@bho|贲红|BVC|benhong|bh|563@bhs|宝华山|BWH|baohuashan|bhs|564@bhx|白河县|BEY|baihexian|bhx|565@bjg|白芨沟|BJJ|baijigou|bjg|566@bjg|碧鸡关|BJM|bijiguan|bjg|567@bji|北滘|IBQ|beijiao|b|568@bji|碧江|BLQ|bijiang|bj|569@bjp|白鸡坡|BBM|baijipo|bjp|570@bjs|笔架山|BSB|bijiashan|bjs|571@bjt|八角台|BTD|bajiaotai|bjt|572@bka|保康|BKD|baokang|bk|573@bkp|白奎堡|BKB|baikuipu|bkb|574@bla|白狼|BAT|bailang|bl|575@bla|百浪|BRZ|bailang|bl|576@ble|博乐|BOR|bole|bl|577@blg|宝拉格|BQC|baolage|blg|578@bli|巴林|BLX|balin|bl|579@bli|宝林|BNB|baolin|bl|580@bli|北流|BOZ|beiliu|bl|581@bli|勃利|BLB|boli|bl|582@blk|布列开|BLR|buliekai|blk|583@bls|宝龙山|BND|baolongshan|bls|584@bmc|八面城|BMD|bamiancheng|bmc|585@bmq|班猫箐|BNM|banmaoqing|bmj|586@bmt|八面通|BMB|bamiantong|bmt|587@bmz|北马圈子|BRP|beimajuanzi|bmqz|588@bpn|北票南|RPD|beipiaonan|bpn|589@bqi|白旗|BQP|baiqi|bq|590@bql|宝泉岭|BQB|baoquanling|bql|591@bqu|白泉|BQL|baiquan|bq|592@bsh|白沙|BSW|baisha|bs|593@bsh|巴山|BAY|bashan|bs|594@bsj|白水江|BSY|baishuijiang|bsj|595@bsp|白沙坡|BPM|baishapo|bsp|596@bss|白石山|BAL|baishishan|bss|597@bsz|白水镇|BUM|baishuizhen|bsz|598@bti|坂田|BTQ|bantian|bt|599@bto|泊头|BZP|botou|bt|600@btu|北屯|BYP|beitun|bt|601@bxh|本溪湖|BHT|benxihu|bxh|602@bxi|博兴|BXK|boxing|bx|603@bxt|八仙筒|VXD|baxiantong|bxt|604@byg|白音察干|BYC|bayanqagan|bycg|605@byh|背荫河|BYB|beiyinhe|byh|606@byi|北营|BIV|beiying|by|607@byl|巴彦高勒|BAC|bayangol|bygl|608@byl|白音他拉|BID|baiyintala|bytl|609@byq|鲅鱼圈|BYT|bayuquan|byq|610@bys|白银市|BNJ|baiyinshi|bys|611@bys|白音胡硕|BCD|baiyinhushuo|byhs|612@bzh|巴中|IEW|bazhong|bz|613@bzh|霸州|RMP|bazhou|bz|614@bzh|北宅|BVP|beizhai|bz|615@cbb|赤壁北|CIN|chibibei|cbb|616@cbg|查布嘎|CBC|chabuga|cbg|617@cch|长城|CEJ|changcheng|cc|618@cch|长冲|CCM|changchong|cc|619@cdd|承德东|CCP|chengdedong|cdd|620@cfx|赤峰西|CID|chifengxi|cfx|621@cga|嵯岗|CAX|cuogang|cg|622@cga|柴岗|CGT|chaigang|cg|623@cge|长葛|CEF|changge|cg|624@cgp|柴沟堡|CGV|chaigoupu|cgb|625@cgu|城固|CGY|chenggu|cg|626@cgy|陈官营|CAJ|chenguanying|cgy|627@cgz|成高子|CZB|chenggaozi|cgz|628@cha|草海|WBW|caohai|ch|629@che|柴河|CHB|chaihe|ch|630@che|册亨|CHZ|ceheng|ch|631@chk|草河口|CKT|caohekou|chk|632@chk|崔黄口|CHP|cuihuangkou|chk|633@chu|巢湖|CIH|chaohu|ch|634@cjg|蔡家沟|CJT|caijiagou|cjg|635@cjh|成吉思汗|CJX|qinggishan|cjsh|636@cji|岔江|CAM|chajiang|cj|637@cjp|蔡家坡|CJY|caijiapo|cjp|638@cko|沧口|CKK|cangkou|ck|639@cle|昌乐|CLK|changle|cl|640@clg|超梁沟|CYP|chaolianggou|clg|641@cli|慈利|CUQ|cili|cl|642@cli|昌黎|CLP|changli|cl|643@clz|长岭子|CLT|changlingzi|clz|644@cmi|晨明|CMB|chenming|cm|645@cno|长农|CNJ|changnong|cn|646@cpb|昌平北|VBP|changpingbei|cpb|647@cpi|常平|DAQ|changping|cp|648@cpl|长坡岭|CPM|changpoling|cpl|649@cqi|辰清|CQB|chenqing|cq|650@csh|楚山|CSB|chushan|cs|651@csh|长寿|EFW|changshou|cs|652@csh|磁山|CSP|cishan|cs|653@csh|苍石|CST|cangshi|cs|654@csh|草市|CSL|caoshi|cs|655@csq|察素齐|CSC|chasuqi|csq|656@cst|长山屯|CVT|changshantun|cst|657@cti|长汀|CES|changting|ct|658@ctx|昌图西|CPT|changtuxi|ctx|659@cwa|春湾|CQQ|chunwan|cw|660@cxi|磁县|CIP|cixian|cx|661@cxi|岑溪|CNZ|cenxi|cx|662@cxi|辰溪|CXQ|chenxi|cx|663@cxi|磁西|CRP|cixi|cx|664@cxn|长兴南|CFH|changxingnan|cxn|665@cya|磁窑|CYK|ciyao|cy|666@cya|朝阳|CYD|chaoyang|cy|667@cya|春阳|CAL|chunyang|cy|668@cya|城阳|CEK|chengyang|cy|669@cyc|创业村|CEX|chuangyecun|cyc|670@cyc|朝阳川|CYL|chaoyangchuan|cyc|671@cyd|朝阳地|CDD|chaoyangdi|cyd|672@cyu|长垣|CYF|changyuan|cy|673@cyz|朝阳镇|CZL|chaoyangzhen|cyz|674@czb|滁州北|CUH|chuzhoubei|czb|675@czb|常州北|ESH|changzhoubei|czb|676@czh|滁州|CXH|chuzhou|cz|677@czh|潮州|CKQ|chaozhou|cz|678@czh|常庄|CVK|changzhuang|cz|679@czl|曹子里|CFP|caozili|czl|680@czw|车转湾|CWM|chezhuanwan|czw|681@czx|郴州西|ICQ|chenzhouxi|czx|682@czx|沧州西|CBP|cangzhouxi|czx|683@dan|德安|DAG|dean|da|684@dan|大安|RAT|daan|da|685@dan|东安|DAZ|dongan|da|686@dba|大坝|DBJ|daba|db|687@dba|大板|DBC|daban|db|688@dba|大巴|DBD|daba|db|689@dba|到保|RBT|daobao|db|690@dbi|定边|DYJ|dingbian|db|691@dbj|东边井|DBB|dongbianjing|dbj|692@dbs|德伯斯|RDT|debosi|dbs|693@dcg|打柴沟|DGJ|dachaigou|dcg|694@dch|德昌|DVW|dechang|dc|695@dda|滴道|DDB|didao|dd|696@dde|大德|DEM|dade|dd|697@ddg|大磴沟|DKJ|dadenggou|ddg|698@ded|刀尔登|DRD|daoerdeng|ded|699@dee|得耳布尔|DRX|derbur|debe|700@dfa|东方|UFQ|dongfang|df|701@dfe|丹凤|DGY|danfeng|df|702@dfe|东丰|DIL|dongfeng|df|703@dge|都格|DMM|duge|dg|704@dgt|大官屯|DTT|daguantun|dgt|705@dgu|大关|RGW|daguan|dg|706@dgu|东光|DGP|dongguang|dg|707@dha|东海|DHB|donghai|dh|708@dhc|大灰厂|DHP|dahuichang|dhc|709@dhq|大红旗|DQD|dahongqi|dhq|710@dhx|东海县|DQH|donghaixian|dhx|711@dhx|德惠西|DXT|dehuixi|dhx|712@djg|达家沟|DJT|dajiagou|djg|713@dji|东津|DKB|dongjin|dj|714@dji|杜家|DJL|dujia|dj|715@djz|大旧庄|DJM|dajiuzhuang|djz|716@dkt|大口屯|DKP|dakoutun|dkt|717@dla|东来|RVD|donglai|dl|718@dlh|德令哈|DHO|delingha|dlh|719@dlh|大陆号|DLC|daluhao|dlh|720@dli|带岭|DLB|dailing|dl|721@dli|大林|DLD|dalin|dl|722@dlq|达拉特旗|DIC|dalateqi|dltq|723@dlt|独立屯|DTX|dulitun|dlt|724@dlu|豆罗|DLV|douluo|dl|725@dlx|达拉特西|DNC|dalatexi|dltx|726@dmc|东明村|DMD|dongmingcun|dmc|727@dmh|洞庙河|DEP|dongmiaohe|dmh|728@dmx|东明县|DNF|dongmingxian|dmx|729@dni|大拟|DNZ|dani|dn|730@dpf|大平房|DPD|dapingfang|dpf|731@dps|大盘石|RPP|dapanshi|dps|732@dpu|大埔|DPI|dapu|dp|733@dpu|大堡|DVT|dapu|db|734@dqh|大其拉哈|DQX|daqilaha|dqlh|735@dqi|道清|DML|daoqing|dq|736@dqs|对青山|DQB|duiqingshan|dqs|737@dqx|德清西|MOH|deqingxi|dqx|738@dsh|东升|DRQ|dongsheng|ds|739@dsh|独山|RWW|dushan|ds|740@dsh|砀山|DKH|dangshan|ds|741@dsh|登沙河|DWT|dengshahe|dsh|742@dsp|读书铺|DPM|dushupu|dsp|743@dst|大石头|DSL|dashitou|dst|744@dsz|大石寨|RZT|dashizhai|dsz|745@dta|东台|DBH|dongtai|dt|746@dta|定陶|DQK|dingtao|dt|747@dta|灯塔|DGT|dengta|dt|748@dtb|大田边|DBM|datianbian|dtb|749@dth|东通化|DTL|dongtonghua|dth|750@dtu|丹徒|RUH|dantu|dt|751@dtu|大屯|DNT|datun|dt|752@dwa|东湾|DRJ|dongwan|dw|753@dwk|大武口|DFJ|dawukou|dwk|754@dwp|低窝铺|DWJ|diwopu|dwp|755@dwt|大王滩|DZZ|dawangtan|dwt|756@dwz|大湾子|DFM|dawanzi|dwz|757@dxg|大兴沟|DXL|daxinggou|dxg|758@dxi|大兴|DXX|daxing|dx|759@dxi|定西|DSJ|dingxi|dx|760@dxi|甸心|DXM|dianxin|dx|761@dxi|东乡|DXG|dongxiang|dx|762@dxi|代县|DKV|daixian|dx|763@dxi|定襄|DXV|dingxiang|dx|764@dxu|东戌|RXP|dongxu|dx|765@dxz|东辛庄|DXD|dongxinzhuang|dxz|766@dya|丹阳|DYH|danyang|dy|767@dya|大雁|DYX|dayan|dy|768@dya|德阳|DYW|deyang|dy|769@dya|当阳|DYN|dangyang|dy|770@dyb|丹阳北|EXH|danyangbei|dyb|771@dyd|大英东|IAW|dayingdong|dyd|772@dyd|东淤地|DBV|dongyudi|dyd|773@dyi|大营|DYV|daying|dy|774@dyu|定远|EWH|dingyuan|dy|775@dyu|岱岳|RYV|daiyue|dy|776@dyu|大元|DYZ|dayuan|dy|777@dyz|大营镇|DJP|dayingzhen|dyz|778@dyz|大营子|DZD|dayingzi|dyz|779@dzc|大战场|DTJ|dazhanchang|dzc|780@dzd|德州东|DIP|dezhoudong|dzd|781@dzh|低庄|DVQ|dizhuang|dz|782@dzh|东镇|DNV|dongzhen|dz|783@dzh|道州|DFZ|daozhou|dz|784@dzh|东至|DCH|dongzhi|dz|785@dzh|东庄|DZV|dongzhuang|dz|786@dzh|兑镇|DWV|duizhen|dz|787@dzh|豆庄|ROP|douzhuang|dz|788@dzh|定州|DXP|dingzhou|dz|789@dzy|大竹园|DZY|dazhuyuan|dzy|790@dzz|大杖子|DAP|dazhangzi|dzz|791@dzz|豆张庄|RZP|douzhangzhuang|dzz|792@ebi|峨边|EBW|ebian|eb|793@edm|二道沟门|RDP|erdaogoumen|edgm|794@edw|二道湾|RDX|erdaowan|edw|795@elo|二龙|RLD|erlong|el|796@elt|二龙山屯|ELA|erlongshantun|elst|797@eme|峨眉|EMW|emei|em|798@emh|二密河|RML|ermihe|emh|799@eyi|二营|RYJ|erying|ey|800@ezh|鄂州|ECN|ezhou|ez|801@fan|福安|FAS|fuan|fa|802@fch|防城|FAZ|fangcheng|fc|803@fch|丰城|FCG|fengcheng|fc|804@fcn|丰城南|FNG|fengchengnan|fcn|805@fdo|肥东|FIH|feidong|fd|806@fer|发耳|FEM|faer|fe|807@fha|富海|FHX|fuhai|fh|808@fha|福海|FHR|fuhai|fh|809@fhc|凤凰城|FHT|fenghuangcheng|fhc|810@fhu|奉化|FHH|fenghua|fh|811@fji|富锦|FIB|fujin|fj|812@fjt|范家屯|FTT|fanjiatun|fjt|813@flt|福利屯|FTB|fulitun|flt|814@flz|丰乐镇|FZB|fenglezhen|flz|815@fna|阜南|FNH|funan|fn|816@fni|阜宁|AKH|funing|fn|817@fni|抚宁|FNP|funing|fn|818@fqi|福清|FQS|fuqing|fq|819@fqu|福泉|VMW|fuquan|fq|820@fsc|丰水村|FSJ|fengshuicun|fsc|821@fsh|丰顺|FUQ|fengshun|fs|822@fsh|繁峙|FSV|fanshi|fs|823@fsh|抚顺|FST|fushun|fs|824@fsk|福山口|FKP|fushankou|fsk|825@fsu|扶绥|FSZ|fusui|fs|826@ftu|冯屯|FTX|fengtun|ft|827@fty|浮图峪|FYP|futuyu|fty|828@fxd|富县东|FDY|fuxiandong|fxd|829@fxi|凤县|FXY|fengxian|fx|830@fxi|富县|FEY|fuxian|fx|831@fxi|费县|FXK|feixian|fx|832@fya|凤阳|FUH|fengyang|fy|833@fya|汾阳|FAV|fenyang|fy|834@fyb|扶余北|FBT|fuyubei|fyb|835@fyi|分宜|FYG|fenyi|fy|836@fyu|富源|FYM|fuyuan|fy|837@fyu|扶余|FYT|fuyu|fy|838@fyu|富裕|FYX|fuyu|fy|839@fzb|抚州北|FBG|fuzhoubei|fzb|840@fzh|凤州|FZY|fengzhou|fz|841@fzh|丰镇|FZC|fengzhen|fz|842@fzh|范镇|VZK|fanzhen|fz|843@gan|固安|GFP|guan|ga|844@gan|广安|VJW|guangan|ga|845@gbd|高碑店|GBP|gaobeidian|gbd|846@gbz|沟帮子|GBD|goubangzi|gbz|847@gcd|甘草店|GDJ|gancaodian|gcd|848@gch|谷城|GCN|gucheng|gc|849@gch|藁城|GEP|gaocheng|gc|850@gcu|高村|GCV|gaocun|gc|851@gcz|古城镇|GZB|guchengzhen|gcz|852@gde|广德|GRH|guangde|gd|853@gdi|贵定|GTW|guiding|gd|854@gdn|贵定南|IDW|guidingnan|gdn|855@gdo|古东|GDV|gudong|gd|856@gga|贵港|GGZ|guigang|gg|857@gga|官高|GVP|guangao|gg|858@ggm|葛根庙|GGT|gegenmiao|ggm|859@ggo|干沟|GGL|gangou|gg|860@ggu|甘谷|GGJ|gangu|gg|861@ggz|高各庄|GGP|gaogezhuang|ggz|862@ghe|甘河|GAX|ganhe|gh|863@ghe|根河|GEX|genhe|gh|864@gjd|郭家店|GDT|guojiadian|gjd|865@gjz|孤家子|GKT|gujiazi|gjz|866@gla|高老|GOB|gaolao|gl|867@gla|古浪|GLJ|gulang|gl|868@gla|皋兰|GEJ|gaolan|gl|869@glf|高楼房|GFM|gaoloufang|glf|870@glh|归流河|GHT|guiliuhe|glh|871@gli|关林|GLF|guanlin|gl|872@glu|甘洛|VOW|ganluo|gl|873@glz|郭磊庄|GLP|guoleizhuang|glz|874@gmi|高密|GMK|gaomi|gm|875@gmz|公庙子|GMC|gongmiaozi|gmz|876@gnh|工农湖|GRT|gongnonghu|gnh|877@gns|广宁寺|GNT|guangningsi|gns|878@gnw|广南卫|GNM|guangnanwei|gnw|879@gpi|高平|GPF|gaoping|gp|880@gqb|甘泉北|GEY|ganquanbei|gqb|881@gqc|共青城|GAG|gongqingcheng|gqc|882@gqk|甘旗卡|GQD|ganqika|gqk|883@gqu|甘泉|GQY|ganquan|gq|884@gqz|高桥镇|GZD|gaoqiaozhen|gqz|885@gsh|赶水|GSW|ganshui|gs|886@gsh|灌水|GST|guanshui|gs|887@gsk|孤山口|GSP|gushankou|gsk|888@gso|果松|GSL|guosong|gs|889@gsz|高山子|GSD|gaoshanzi|gsz|890@gsz|嘎什甸子|GXD|gashidianzi|gsdz|891@gta|高台|GTJ|gaotai|gt|892@gta|高滩|GAY|gaotan|gt|893@gti|古田|GTS|gutian|gt|894@gti|官厅|GTP|guanting|gt|895@gto|广通|GOM|guangtong|gt|896@gtx|官厅西|KEP|guantingxi|gtx|897@gxi|贵溪|GXG|guixi|gx|898@gya|涡阳|GYH|guoyang|gy|899@gyi|巩义|GXF|gongyi|gy|900@gyi|高邑|GIP|gaoyi|gy|901@gyn|巩义南|GYF|gongyinan|gyn|902@gyu|固原|GUJ|guyuan|gy|903@gyu|菇园|GYL|guyuan|gy|904@gyz|公营子|GYD|gongyingzi|gyz|905@gze|光泽|GZS|guangze|gz|906@gzh|古镇|GNQ|guzhen|gz|907@gzh|瓜州|GZJ|guazhou|gz|908@gzh|高州|GSQ|gaozhou|gz|909@gzh|固镇|GEH|guzhen|gz|910@gzh|盖州|GXT|gaizhou|gz|911@gzj|官字井|GOT|guanzijing|gzj|912@gzp|革镇堡|GZT|gezhenpu|gzb|913@gzs|冠豸山|GSS|guanzhishan|gzs|914@gzx|盖州西|GAT|gaizhouxi|gzx|915@han|红安|HWN|hongan|ha|916@han|淮安南|AMH|huaiannan|han|917@hax|红安西|VXN|honganxi|hax|918@hax|海安县|HIH|haianxian|hax|919@hba|黄柏|HBL|huangbai|hb|920@hbe|海北|HEB|haibei|hb|921@hbi|鹤壁|HAF|hebi|hb|922@hch|华城|VCQ|huacheng|hc|923@hch|合川|WKW|hechuan|hc|924@hch|河唇|HCZ|hechun|hc|925@hch|汉川|HCN|hanchuan|hc|926@hch|海城|HCT|haicheng|hc|927@hct|黑冲滩|HCJ|heichongtan|hct|928@hcu|黄村|HCP|huangcun|hc|929@hcx|海城西|HXT|haichengxi|hcx|930@hde|化德|HGC|huade|hd|931@hdo|洪洞|HDV|hongdong|hd|932@hfe|横峰|HFG|hengfeng|hf|933@hfw|韩府湾|HXJ|hanfuwan|hfw|934@hgu|汉沽|HGP|hangu|hg|935@hgy|黄瓜园|HYM|huangguayuan|hgy|936@hgz|红光镇|IGW|hongguangzhen|hgz|937@hhe|浑河|HHT|hunhe|hh|938@hhg|红花沟|VHD|honghuagou|hhg|939@hht|黄花筒|HUD|huanghuatong|hht|940@hjd|贺家店|HJJ|hejiadian|hjd|941@hji|和静|HJR|hejing|hj|942@hji|红江|HFM|hongjiang|hj|943@hji|黑井|HIM|heijing|hj|944@hji|获嘉|HJF|huojia|hj|945@hji|河津|HJV|hejin|hj|946@hji|涵江|HJS|hanjiang|hj|947@hji|华家|HJT|huajia|hj|948@hjx|河间西|HXP|hejianxi|hjx|949@hjz|花家庄|HJM|huajiazhuang|hjz|950@hkn|河口南|HKJ|hekounan|hkn|951@hko|黄口|KOH|huangkou|hk|952@hko|湖口|HKG|hukou|hk|953@hla|呼兰|HUB|hulan|hl|954@hlb|葫芦岛北|HPD|huludaobei|hldb|955@hlh|浩良河|HHB|haolianghe|hlh|956@hlh|哈拉海|HIT|halahai|hlh|957@hli|鹤立|HOB|heli|hl|958@hli|桦林|HIB|hualin|hl|959@hli|黄陵|ULY|huangling|hl|960@hli|海林|HRB|hailin|hl|961@hli|虎林|VLB|hulin|hl|962@hli|寒岭|HAT|hanling|hl|963@hlo|和龙|HLL|helong|hl|964@hlo|海龙|HIL|hailong|hl|965@hls|哈拉苏|HAX|harus|hls|966@hlt|呼鲁斯太|VTJ|hulstai|hlst|967@hlz|火连寨|HLT|huolianzhai|hlz|968@hme|黄梅|VEH|huangmei|hm|969@hmt|蛤蟆塘|HMT|hamatang|gmt|970@hmy|韩麻营|HYP|hanmaying|hmy|971@hnh|黄泥河|HHL|huangnihe|hnh|972@hni|海宁|HNH|haining|hn|973@hno|惠农|HMJ|huinong|hn|974@hpi|和平|VAQ|heping|hp|975@hpz|花棚子|HZM|huapengzi|hpz|976@hqi|花桥|VQH|huaqiao|hq|977@hqi|宏庆|HEY|hongqing|hq|978@hre|怀仁|HRV|huairen|hr|979@hro|华容|HRN|huarong|hr|980@hsb|华山北|HDY|huashanbei|hsb|981@hsd|黄松甸|HDL|huangsongdian|hsd|982@hsg|和什托洛盖|VSR|heshituoluogai|hstlg|983@hsh|红山|VSB|hongshan|hs|984@hsh|汉寿|VSQ|hanshou|hs|985@hsh|衡山|HSQ|hengshan|hs|986@hsh|黑水|HOT|heishui|hs|987@hsh|惠山|VCH|huishan|hs|988@hsh|虎什哈|HHP|hushiha|hsh|989@hsp|红寺堡|HSJ|hongsipu|hsb|990@hst|虎石台|HUT|hushitai|hst|991@hsw|海石湾|HSO|haishiwan|hsw|992@hsx|衡山西|HEQ|hengshanxi|hsx|993@hsx|红砂岘|VSJ|hongshaxian|hsj|994@hta|黑台|HQB|heitai|ht|995@hta|桓台|VTK|huantai|ht|996@hti|和田|VTR|hetian|ht|997@hto|会同|VTQ|huitong|ht|998@htz|海坨子|HZT|haituozi|htz|999@hwa|黑旺|HWK|heiwang|hw|1000@hwa|海湾|RWH|haiwan|hw|1001@hxi|红星|VXB|hongxing|hx|1002@hxi|徽县|HYY|huixian|hx|1003@hxl|红兴隆|VHB|hongxinglong|hxl|1004@hxt|换新天|VTB|huanxintian|hxt|1005@hxt|红岘台|HTJ|hongxiantai|hxt|1006@hya|红彦|VIX|hongyan|hy|1007@hya|合阳|HAY|heyang|hy|1008@hya|海阳|HYK|haiyang|hy|1009@hyd|衡阳东|HVQ|hengyangdong|hyd|1010@hyi|华蓥|HUW|huaying|hy|1011@hyi|汉阴|HQY|hanyin|hy|1012@hyt|黄羊滩|HGJ|huangyangtan|hyt|1013@hyu|汉源|WHW|hanyuan|hy|1014@hyu|湟源|HNO|huangyuan|hy|1015@hyu|河源|VIQ|heyuan|hy|1016@hyu|花园|HUN|huayuan|hy|1017@hyz|黄羊镇|HYJ|huangyangzhen|hyz|1018@hzh|湖州|VZH|huzhou|hz|1019@hzh|化州|HZZ|huazhou|hz|1020@hzh|黄州|VON|huangzhou|hz|1021@hzh|霍州|HZV|huozhou|hz|1022@hzx|惠州西|VXQ|huizhouxi|hzx|1023@jba|巨宝|JRT|jubao|jb|1024@jbi|靖边|JIY|jingbian|jb|1025@jbt|金宝屯|JBD|jinbaotun|jbt|1026@jcb|晋城北|JEF|jinchengbei|jcb|1027@jch|金昌|JCJ|jinchang|jc|1028@jch|鄄城|JCK|juancheng|jc|1029@jch|交城|JNV|jiaocheng|jc|1030@jch|建昌|JFD|jianchang|jc|1031@jde|峻德|JDB|junde|jd|1032@jdi|井店|JFP|jingdian|jd|1033@jdo|鸡东|JOB|jidong|jd|1034@jdu|江都|UDH|jiangdu|jd|1035@jgs|鸡冠山|JST|jiguanshan|jgs|1036@jgt|金沟屯|VGP|jingoutun|jgt|1037@jha|静海|JHP|jinghai|jh|1038@jhe|金河|JHX|jinhe|jh|1039@jhe|锦河|JHB|jinhe|jh|1040@jhe|锦和|JHQ|jinhe|jh|1041@jhe|精河|JHR|jinghe|jh|1042@jhn|精河南|JIR|jinghenan|jhn|1043@jhu|江华|JHZ|jianghua|jh|1044@jhu|建湖|AJH|jianhu|jh|1045@jjg|纪家沟|VJD|jijiagou|jjg|1046@jji|晋江|JJS|jinjiang|jj|1047@jji|江津|JJW|jiangjin|jj|1048@jji|姜家|JJB|jiangjia|jj|1049@jke|金坑|JKT|jinkeng|jk|1050@jli|芨岭|JLJ|jiling|jl|1051@jmc|金马村|JMM|jinmacun|jmc|1052@jme|角美|JES|jiaomei|jm|1053@jme|江门|JWQ|jiangmen|jm|1054@jna|莒南|JOK|junan|jn|1055@jna|井南|JNP|jingnan|jn|1056@jou|建瓯|JVS|jianou|jo|1057@jpe|经棚|JPC|jingpeng|jp|1058@jqi|江桥|JQX|jiangqiao|jq|1059@jsa|九三|SSX|jiusan|js|1060@jsb|金山北|EGH|jinshanbei|jsb|1061@jsh|京山|JCN|jingshan|js|1062@jsh|建始|JRN|jianshi|js|1063@jsh|嘉善|JSH|jiashan|js|1064@jsh|稷山|JVV|jishan|js|1065@jsh|吉舒|JSL|jishu|js|1066@jsh|建设|JET|jianshe|js|1067@jsh|甲山|JOP|jiashan|js|1068@jsj|建三江|JIB|jiansanjiang|jsj|1069@jsn|嘉善南|EAH|jiashannan|jsn|1070@jst|金山屯|JTB|jinshantun|jst|1071@jst|江所田|JOM|jiangsuotian|jst|1072@jta|景泰|JTJ|jingtai|jt|1073@jwe|吉文|JWX|jiwen|jw|1074@jxi|进贤|JUG|jinxian|jx|1075@jxi|莒县|JKK|juxian|jx|1076@jxi|嘉祥|JUK|jiaxiang|jx|1077@jxi|介休|JXV|jiexiu|jx|1078@jxi|井陉|JJP|jingxing|jx|1079@jxi|嘉兴|JXH|jiaxing|jx|1080@jxn|嘉兴南|EPH|jiaxingnan|jxn|1081@jxz|夹心子|JXT|jiaxinzi|jxz|1082@jya|简阳|JYW|jianyang|jy|1083@jya|揭阳|JRQ|jieyang|jy|1084@jya|建阳|JYS|jianyang|jy|1085@jya|姜堰|UEH|jiangyan|jy|1086@jye|巨野|JYK|juye|jy|1087@jyo|江永|JYZ|jiangyong|jy|1088@jyu|靖远|JYJ|jingyuan|jy|1089@jyu|缙云|JYH|jinyun|jy|1090@jyu|江源|SZL|jiangyuan|jy|1091@jyu|济源|JYF|jiyuan|jy|1092@jyx|靖远西|JXJ|jingyuanxi|jyx|1093@jzb|胶州北|JZK|jiaozhoubei|jzb|1094@jzd|焦作东|WEF|jiaozuodong|jzd|1095@jzh|靖州|JEQ|jingzhou|jz|1096@jzh|荆州|JBN|jingzhou|jz|1097@jzh|金寨|JZH|jinzhai|jz|1098@jzh|晋州|JXP|jinzhou|jz|1099@jzh|胶州|JXK|jiaozhou|jz|1100@jzn|锦州南|JOD|jinzhounan|jzn|1101@jzu|焦作|JOF|jiaozuo|jz|1102@jzw|旧庄窝|JVP|jiuzhuangwo|jzw|1103@jzz|金杖子|JYD|jinzhangzi|jzz|1104@kan|开安|KAT|kaian|ka|1105@kch|库车|KCR|kuche|kc|1106@kch|康城|KCP|kangcheng|kc|1107@kde|库都尔|KDX|huder|kde|1108@kdi|宽甸|KDT|kuandian|kd|1109@kdo|克东|KOB|kedong|kd|1110@kji|开江|KAW|kaijiang|kj|1111@kjj|康金井|KJB|kangjinjing|kjj|1112@klq|喀喇其|KQX|kalaqi|klq|1113@klu|开鲁|KLC|kailu|kl|1114@kly|克拉玛依|KHR|kelamayi|klmy|1115@kqi|口前|KQL|kouqian|kq|1116@ksh|奎山|KAB|kuishan|ks|1117@ksh|昆山|KSH|kunshan|ks|1118@ksh|克山|KSB|keshan|ks|1119@kto|开通|KTT|kaitong|kt|1120@kxl|康熙岭|KXZ|kangxiling|kxl|1121@kyh|克一河|KHX|keyihe|kyh|1122@kyx|开原西|KXT|kaiyuanxi|kyx|1123@kzh|康庄|KZP|kangzhuang|kz|1124@lbi|来宾|UBZ|laibin|lb|1125@lbi|老边|LLT|laobian|lb|1126@lbx|灵宝西|LPF|lingbaoxi|lbx|1127@lch|龙川|LUQ|longchuan|lc|1128@lch|乐昌|LCQ|lechang|lc|1129@lch|黎城|UCP|licheng|lc|1130@lch|聊城|UCK|liaocheng|lc|1131@lcu|蓝村|LCK|lancun|lc|1132@ldo|林东|LRC|lindong|ld|1133@ldu|乐都|LDO|ledu|ld|1134@ldx|梁底下|LDP|liangdixia|ldx|1135@ldz|六道河子|LVP|liudaohezi|ldhz|1136@lfa|鲁番|LVM|lufan|lf|1137@lfa|廊坊|LJP|langfang|lf|1138@lfa|落垡|LOP|luofa|lf|1139@lfb|廊坊北|LFP|langfangbei|lfb|1140@lfe|禄丰|LFM|lufeng|lf|1141@lfu|老府|UFD|laofu|lf|1142@lga|兰岗|LNB|langang|lg|1143@lgd|龙骨甸|LGM|longgudian|lgd|1144@lgo|芦沟|LOM|lugou|lg|1145@lgo|龙沟|LGJ|longgou|lg|1146@lgu|拉古|LGB|lagu|lg|1147@lha|临海|UFH|linhai|lh|1148@lha|林海|LXX|linhai|lh|1149@lha|拉哈|LHX|laha|lh|1150@lha|凌海|JID|linghai|lh|1151@lhe|柳河|LNL|liuhe|lh|1152@lhe|六合|KLH|luhe|lh|1153@lhu|龙华|LHP|longhua|lh|1154@lhy|滦河沿|UNP|luanheyan|lhy|1155@lhz|六合镇|LEX|liuhezhen|lhz|1156@ljd|亮甲店|LRT|liangjiadian|ljd|1157@ljd|刘家店|UDT|liujiadian|ljd|1158@ljh|刘家河|LVT|liujiahe|ljh|1159@lji|连江|LKS|lianjiang|lj|1160@lji|李家|LJB|lijia|lj|1161@lji|罗江|LJW|luojiang|lj|1162@lji|廉江|LJZ|lianjiang|lj|1163@lji|庐江|UJH|lujiang|lj|1164@lji|两家|UJT|liangjia|lj|1165@lji|龙江|LJX|longjiang|lj|1166@lji|龙嘉|UJL|longjia|lj|1167@ljk|莲江口|LHB|lianjiangkou|ljk|1168@ljl|蔺家楼|ULK|linjialou|ljl|1169@ljp|李家坪|LIJ|lijiaping|ljp|1170@lka|兰考|LKF|lankao|lk|1171@lko|林口|LKB|linkou|lk|1172@lkp|路口铺|LKQ|lukoupu|lkp|1173@lla|老莱|LAX|laolai|ll|1174@lli|拉林|LAB|lalin|ll|1175@lli|陆良|LRM|luliang|ll|1176@lli|龙里|LLW|longli|ll|1177@lli|零陵|UWZ|lingling|ll|1178@lli|临澧|LWQ|linli|ll|1179@lli|兰棱|LLB|lanling|ll|1180@llo|卢龙|UAP|lulong|ll|1181@lmd|喇嘛甸|LMX|lamadian|lmd|1182@lmd|里木店|LMB|limudian|lmd|1183@lme|洛门|LMJ|luomen|lm|1184@lna|龙南|UNG|longnan|ln|1185@lpi|梁平|UQW|liangping|lp|1186@lpi|罗平|LPM|luoping|lp|1187@lpl|落坡岭|LPP|luopoling|lpl|1188@lps|六盘山|UPJ|liupanshan|lps|1189@lps|乐平市|LPG|lepingshi|lps|1190@lqi|临清|UQK|linqing|lq|1191@lqs|龙泉寺|UQJ|longquansi|lqs|1192@lsc|乐善村|LUM|leshancun|lsc|1193@lsd|冷水江东|UDQ|lengshuijiangdong|lsjd|1194@lsg|连山关|LGT|lianshanguan|lsg|1195@lsg|流水沟|USP|liushuigou|lsg|1196@lsh|陵水|LIQ|lingshui|ls|1197@lsh|乐山|UTW|leshan|ls|1198@lsh|罗山|LRN|luoshan|ls|1199@lsh|鲁山|LAF|lushan|ls|1200@lsh|丽水|USH|lishui|ls|1201@lsh|梁山|LMK|liangshan|ls|1202@lsh|灵石|LSV|lingshi|ls|1203@lsh|露水河|LUL|lushuihe|lsh|1204@lsh|庐山|LSG|lushan|ls|1205@lsp|林盛堡|LBT|linshengpu|lsp|1206@lst|柳树屯|LSD|liushutun|lst|1207@lsz|梨树镇|LSB|lishuzhen|lsz|1208@lsz|龙山镇|LAS|longshanzhen|lsz|1209@lsz|李石寨|LET|lishizhai|lsz|1210@lta|黎塘|LTZ|litang|lt|1211@lta|轮台|LAR|luntai|lt|1212@lta|芦台|LTP|lutai|lt|1213@ltb|龙塘坝|LBM|longtangba|ltb|1214@ltu|濑湍|LVZ|laituan|lt|1215@ltx|骆驼巷|LTJ|luotuoxiang|ltx|1216@lwa|李旺|VLJ|liwang|lw|1217@lwd|莱芜东|LWK|laiwudong|lwd|1218@lws|狼尾山|LRJ|langweishan|lws|1219@lwu|灵武|LNJ|lingwu|lw|1220@lwx|莱芜西|UXK|laiwuxi|lwx|1221@lxi|朗乡|LXB|langxiang|lx|1222@lxi|陇县|LXY|longxian|lx|1223@lxi|临湘|LXQ|linxiang|lx|1224@lxi|莱西|LXK|laixi|lx|1225@lxi|林西|LXC|linxi|lx|1226@lxi|滦县|UXP|luanxian|lx|1227@lya|略阳|LYY|lueyang|ly|1228@lya|莱阳|LYK|laiyang|ly|1229@lya|辽阳|LYT|liaoyang|ly|1230@lyb|临沂北|UYK|linyibei|lyb|1231@lyd|凌源东|LDD|lingyuandong|lyd|1232@lyg|连云港|UIH|lianyungang|lyg|1233@lyh|老羊壕|LYC|laoyanghao|lyh|1234@lyi|临颍|LNF|linying|ly|1235@lyi|老营|LXL|laoying|ly|1236@lyo|龙游|LMH|longyou|ly|1237@lyu|罗源|LVS|luoyuan|ly|1238@lyu|林源|LYX|linyuan|ly|1239@lyu|涟源|LAQ|lianyuan|ly|1240@lyu|涞源|LYP|laiyuan|ly|1241@lyx|耒阳西|LPQ|leiyangxi|lyx|1242@lze|临泽|LEJ|linze|lz|1243@lzg|龙爪沟|LZT|longzhaogou|lzg|1244@lzh|雷州|UAQ|leizhou|lz|1245@lzh|六枝|LIW|liuzhi|lz|1246@lzh|鹿寨|LIZ|luzhai|lz|1247@lzh|来舟|LZS|laizhou|lz|1248@lzh|龙镇|LZA|longzhen|lz|1249@lzh|拉鲊|LEM|lazha|lz|1250@man|明安|MAC|mingan|ma|1251@mas|马鞍山|MAH|maanshan|mas|1252@mba|毛坝|MBY|maoba|mb|1253@mbg|毛坝关|MGY|maobaguan|mbg|1254@mcb|麻城北|MBN|machengbei|mcb|1255@mch|渑池|MCF|mianchi|mc|1256@mch|明城|MCL|mingcheng|mc|1257@mch|庙城|MAP|miaocheng|mc|1258@mcn|渑池南|MNF|mianchinan|mcn|1259@mcp|茅草坪|KPM|maocaoping|mcp|1260@mdh|猛洞河|MUQ|mengdonghe|mdh|1261@mds|磨刀石|MOB|modaoshi|mds|1262@mdu|弥渡|MDF|midu|md|1263@mes|帽儿山|MRB|maoershan|mes|1264@mga|明港|MGN|minggang|mg|1265@mhk|梅河口|MHL|meihekou|mhk|1266@mhu|马皇|MHZ|mahuang|mh|1267@mjg|孟家岗|MGB|mengjiagang|mjg|1268@mla|美兰|MHQ|meilan|ml|1269@mld|汨罗东|MQQ|miluodong|mld|1270@mlh|马莲河|MHB|malianhe|mlh|1271@mli|茅岭|MLZ|maoling|ml|1272@mli|庙岭|MLL|miaoling|ml|1273@mli|茂林|MLD|maolin|ml|1274@mli|穆棱|MLB|muling|ml|1275@mli|马林|MID|malin|ml|1276@mlo|马龙|MGM|malong|ml|1277@mlo|汨罗|MLQ|miluo|ml|1278@mlt|木里图|MUD|mulitu|mlt|1279@mml|密马龙|MMM|mimalong|mml|1280@mnh|玛纳斯湖|MNR|manasihu|mnsh|1281@mni|冕宁|UGW|mianning|mn|1282@mpa|沐滂|MPQ|mupang|mp|1283@mqh|马桥河|MQB|maqiaohe|mqh|1284@mqi|闽清|MQS|minqing|mq|1285@mqu|民权|MQF|minquan|mq|1286@msh|明水河|MUT|mingshuihe|msh|1287@msh|麻山|MAB|mashan|ms|1288@msh|眉山|MSW|meishan|ms|1289@msw|漫水湾|MKW|manshuiwan|msw|1290@msz|茂舍祖|MOM|maoshezu|msz|1291@msz|米沙子|MST|mishazi|msz|1292@mtz|庙台子|MZB|miaotaizi|mtz|1293@mxi|美溪|MEB|meixi|mx|1294@mxi|勉县|MVY|mianxian|mx|1295@mya|麻阳|MVQ|mayang|my|1296@myc|牧羊村|MCM|muyangcun|myc|1297@myi|米易|MMW|miyi|my|1298@myu|麦园|MYS|maiyuan|my|1299@myu|墨玉|MUR|moyu|my|1300@myu|密云|MUP|miyun|my|1301@mzh|庙庄|MZJ|miaozhuang|mz|1302@mzh|米脂|MEY|mizhi|mz|1303@mzh|明珠|MFQ|mingzhu|mz|1304@nan|宁安|NAB|ningan|na|1305@nan|农安|NAT|nongan|na|1306@nbs|南博山|NBK|nanboshan|nbs|1307@nch|南仇|NCK|nanchou|nc|1308@ncs|南城司|NSP|nanchengsi|ncs|1309@ncu|宁村|NCZ|ningcun|nc|1310@nde|宁德|NES|ningde|nd|1311@ngc|南观村|NGP|nanguancun|ngc|1312@ngd|南宫东|NFP|nangongdong|ngd|1313@ngl|南关岭|NLT|nanguanling|ngl|1314@ngu|宁国|NNH|ningguo|ng|1315@nha|宁海|NHH|ninghai|nh|1316@nhc|南河川|NHJ|nanhechuan|nhc|1317@nhu|南华|NHS|nanhua|nh|1318@nhz|泥河子|NHD|nihezi|nhz|1319@nji|宁家|NVT|ningjia|nj|1320@nji|牛家|NJB|niujia|nj|1321@nji|南靖|NJS|nanjing|nj|1322@nji|能家|NJD|nengjia|nj|1323@nko|南口|NKP|nankou|nk|1324@nkq|南口前|NKT|nankouqian|nkq|1325@nla|南朗|NNQ|nanlang|nl|1326@nli|乃林|NLD|nailin|nl|1327@nlk|尼勒克|NIR|nileke|nlk|1328@nlu|那罗|ULZ|naluo|nl|1329@nlx|宁陵县|NLF|ninglingxian|nlx|1330@nma|奈曼|NMD|naiman|nm|1331@nmi|宁明|NMZ|ningming|nm|1332@nmu|南木|NMX|nanmu|nm|1333@npn|南平南|NNS|nanpingnan|npn|1334@npu|那铺|NPZ|napu|np|1335@nqi|南桥|NQD|nanqiao|nq|1336@nqu|那曲|NQO|naqu|nq|1337@nqu|暖泉|NQJ|nuanquan|nq|1338@nta|南台|NTT|nantai|nt|1339@nto|南头|NOQ|nantou|nt|1340@nwu|宁武|NWV|ningwu|nw|1341@nwz|南湾子|NWP|nanwanzi|nwz|1342@nxb|南翔北|NEH|nanxiangbei|nxb|1343@nxi|宁乡|NXQ|ningxiang|nx|1344@nxi|内乡|NXF|neixiang|nx|1345@nxt|牛心台|NXT|niuxintai|nxt|1346@nyu|南峪|NUP|nanyu|ny|1347@nzg|娘子关|NIP|niangziguan|nzg|1348@nzh|南召|NAF|nanzhao|nz|1349@nzm|南杂木|NZT|nanzamu|nzm|1350@pan|平安|PAL|pingan|pa|1351@pan|蓬安|PAW|pengan|pa|1352@pay|平安驿|PNO|pinganyi|pay|1353@paz|磐安镇|PAJ|pananzhen|paz|1354@paz|平安镇|PZT|pinganzhen|paz|1355@pcd|蒲城东|PEY|puchengdong|pcd|1356@pch|蒲城|PCY|pucheng|pc|1357@pde|裴德|PDB|peide|pd|1358@pdi|偏店|PRP|piandian|pd|1359@pdx|平顶山西|BFF|pingdingshanxi|pdsx|1360@pdx|坡底下|PXJ|podixia|pdx|1361@pet|瓢儿屯|PRT|piaoertun|pet|1362@pfa|平房|PFB|pingfang|pf|1363@pga|平岗|PGL|pinggang|pg|1364@pgu|平关|PGM|pingguan|pg|1365@pgu|盘关|PAM|panguan|pg|1366@pgu|平果|PGZ|pingguo|pg|1367@phb|徘徊北|PHP|paihuibei|phb|1368@phk|平河口|PHM|pinghekou|phk|1369@pjb|盘锦北|PBD|panjinbei|pjb|1370@pjd|潘家店|PDP|panjiadian|pjd|1371@pko|皮口|PKT|pikou|pk|1372@pld|普兰店|PLT|pulandian|pld|1373@pli|偏岭|PNT|pianling|pl|1374@plu|平罗|SZJ|pingluo|plu|1375@psh|平山|PSB|pingshan|ps|1376@psh|彭山|PSW|pengshan|ps|1377@psh|皮山|PSR|pishan|ps|1378@psh|彭水|PHW|pengshui|ps|1379@psh|磐石|PSL|panshi|ps|1380@psh|平社|PSV|pingshe|ps|1381@pta|平台|PVT|pingtai|pt|1382@pti|平田|PTM|pingtian|pt|1383@pti|莆田|PTS|putian|pt|1384@ptq|葡萄菁|PTW|putaoqing|ptj|1385@pwa|普湾|PWT|puwan|pw|1386@pwa|平旺|PWV|pingwang|pw|1387@pxg|平型关|PGV|pingxingguan|pxg|1388@pxi|普雄|POW|puxiong|px|1389@pya|平洋|PYX|pingyang|py|1390@pya|彭阳|PYJ|pengyang|py|1391@pya|平遥|PYV|pingyao|py|1392@pyi|平邑|PIK|pingyi|py|1393@pyp|平原堡|PPJ|pingyuanpu|pyp|1394@pyu|平原|PYK|pingyuan|py|1395@pyu|平峪|PYP|pingyu|py|1396@pze|彭泽|PZG|pengze|pz|1397@pzh|邳州|PJH|pizhou|pz|1398@pzh|平庄|PZD|pingzhuang|pz|1399@pzi|泡子|POD|paozi|pz|1400@pzn|平庄南|PND|pingzhuangnan|pzn|1401@qan|乾安|QOT|qianan|qa|1402@qan|庆安|QAB|qingan|qa|1403@qan|迁安|QQP|qianan|qa|1404@qdb|祁东北|QRQ|qidongbei|qd|1405@qdi|七甸|QDM|qidian|qd|1406@qfd|曲阜东|QAK|qufudong|qfd|1407@qfe|庆丰|QFT|qingfeng|qf|1408@qft|奇峰塔|QVP|qifengta|qft|1409@qfu|曲阜|QFK|qufu|qf|1410@qfy|勤丰营|QFM|qinfengying|qfy|1411@qha|琼海|QYQ|qionghai|qh|1412@qhd|秦皇岛|QTP|qinhuangdao|qhd|1413@qhe|千河|QUY|qianhe|qh|1414@qhe|清河|QIP|qinghe|qh|1415@qhm|清河门|QHD|qinghemen|qhm|1416@qhy|清华园|QHP|qinghuayuan|qhy|1417@qji|渠旧|QJZ|qujiu|qj|1418@qji|綦江|QJW|qijiang|qj|1419@qji|潜江|QJN|qianjiang|qj|1420@qji|全椒|INH|quanjiao|qj|1421@qji|秦家|QJB|qinjia|qj|1422@qjp|祁家堡|QBT|qijiapu|qjb|1423@qjx|清涧县|QNY|qingjianxian|qjx|1424@qjz|秦家庄|QZV|qinjiazhuang|qjz|1425@qlh|七里河|QLD|qilihe|qlh|1426@qli|渠黎|QLZ|quli|ql|1427@qli|秦岭|QLY|qinling|ql|1428@qls|青龙山|QGH|qinglongshan|qls|1429@qls|青龙寺|QSM|qinglongsi|qls|1430@qme|祁门|QIH|qimen|qm|1431@qmt|前磨头|QMP|qianmotou|qmt|1432@qsh|青山|QSB|qingshan|qs|1433@qsh|全胜|QVB|quansheng|qs|1434@qsh|确山|QSN|queshan|qs|1435@qsh|清水|QUJ|qingshui|qs|1436@qsh|前山|QXQ|qianshan|qs|1437@qsy|戚墅堰|QYH|qishuyan|qsy|1438@qti|青田|QVH|qingtian|qt|1439@qto|桥头|QAT|qiaotou|qt|1440@qtx|青铜峡|QTJ|qingtongxia|qtx|1441@qwe|前卫|QWD|qianwei|qw|1442@qwt|前苇塘|QWP|qianweitang|qwt|1443@qxi|渠县|QRW|quxian|qx|1444@qxi|祁县|QXV|qixian|qx|1445@qxi|青县|QXP|qingxian|qx|1446@qxi|桥西|QXJ|qiaoxi|qx|1447@qxu|清徐|QUV|qingxu|qx|1448@qxy|旗下营|QXC|qixiaying|qxy|1449@qya|千阳|QOY|qianyang|qy|1450@qya|沁阳|QYF|qinyang|qy|1451@qya|泉阳|QYL|quanyang|qy|1452@qyb|祁阳北|QVQ|qiyangbei|qy|1453@qyi|七营|QYJ|qiying|qy|1454@qys|庆阳山|QSJ|qingyangshan|qys|1455@qyu|清远|QBQ|qingyuan|qy|1456@qyu|清原|QYT|qingyuan|qy|1457@qzd|钦州东|QDZ|qinzhoudong|qzd|1458@qzh|全州|QZZ|quanzhou|qz|1459@qzh|钦州|QRZ|qinzhou|qz|1460@qzs|青州市|QZK|qingzhoushi|qzs|1461@ran|瑞安|RAH|ruian|ra|1462@rch|荣昌|RCW|rongchang|rc|1463@rch|瑞昌|RCG|ruichang|rc|1464@rga|如皋|RBH|rugao|rg|1465@rgu|容桂|RUQ|ronggui|rg|1466@rqi|任丘|RQP|renqiu|rq|1467@rsh|乳山|ROK|rushan|rs|1468@rsh|融水|RSZ|rongshui|rs|1469@rsh|热水|RSD|reshui|rs|1470@rxi|容县|RXZ|rongxian|rx|1471@rya|饶阳|RVP|raoyang|ry|1472@rya|汝阳|RYF|ruyang|ry|1473@ryh|绕阳河|RHD|raoyanghe|ryh|1474@rzh|汝州|ROF|ruzhou|rz|1475@sba|石坝|OBJ|shiba|sb|1476@sbc|上板城|SBP|shangbancheng|sbc|1477@sbi|施秉|AQW|shibing|sb|1478@sbn|上板城南|OBP|shangbanchengnan|sbcn|1479@sby|世博园|ZWT|shiboyuan|sby|1480@scb|双城北|SBB|shuangchengbei|scb|1481@sch|商城|SWN|shangcheng|sc|1482@sch|莎车|SCR|shache|sc|1483@sch|顺昌|SCS|shunchang|sc|1484@sch|舒城|OCH|shucheng|sc|1485@sch|神池|SMV|shenchi|sc|1486@sch|沙城|SCP|shacheng|sc|1487@sch|石城|SCT|shicheng|sc|1488@scz|山城镇|SCL|shanchengzhen|scz|1489@sda|山丹|SDJ|shandan|sd|1490@sde|顺德|ORQ|shunde|sd|1491@sde|绥德|ODY|suide|sd|1492@sdo|邵东|SOQ|shaodong|sd|1493@sdo|水洞|SIL|shuidong|sd|1494@sdu|商都|SXC|shangdu|sd|1495@sdu|十渡|SEP|shidu|sd|1496@sdw|四道湾|OUD|sidaowan|sdw|1497@sdy|顺德学院|OJQ|shundexueyuan|sdxy|1498@sfa|绅坊|OLH|shenfang|sf|1499@sfe|双丰|OFB|shuangfeng|sf|1500@sft|四方台|STB|sifangtai|sft|1501@sfu|水富|OTW|shuifu|sf|1502@sgk|三关口|OKJ|sanguankou|sgk|1503@sgl|桑根达来|OGC|sanggendalai|sgdl|1504@sgu|韶关|SNQ|shaoguan|sg|1505@sgz|上高镇|SVK|shanggaozhen|sgz|1506@sha|上杭|JBS|shanghang|sh|1507@sha|沙海|SED|shahai|sh|1508@she|松河|SBM|songhe|sh|1509@she|沙河|SHP|shahe|sh|1510@shk|沙河口|SKT|shahekou|shk|1511@shl|赛汗塔拉|SHC|saihantai|shtl|1512@shs|沙河市|VOP|shaheshi|shs|1513@shs|沙后所|SSD|shahousuo|shs|1514@sht|山河屯|SHL|shanhetun|sht|1515@shx|三河县|OXP|sanhexian|shx|1516@shy|四合永|OHD|siheyong|shy|1517@shz|三汇镇|OZW|sanhuizhen|shz|1518@shz|双河镇|SEL|shuanghezhen|shz|1519@shz|石河子|SZR|shihezi|shz|1520@shz|三合庄|SVP|sanhezhuang|shz|1521@sjd|三家店|ODP|sanjiadian|sjd|1522@sjh|水家湖|SQH|shuijiahu|sjh|1523@sjh|沈家河|OJJ|shenjiahe|sjh|1524@sjh|松江河|SJL|songjianghe|sjh|1525@sji|尚家|SJB|shangjia|sj|1526@sji|孙家|SUB|sunjia|sj|1527@sji|沈家|OJB|shenjia|sj|1528@sji|松江|SAH|songjiang|sj|1529@sjk|三江口|SKD|sanjiangkou|sjk|1530@sjl|司家岭|OLK|sijialing|sjl|1531@sjn|松江南|IMH|songjiangnan|sjn|1532@sjn|石景山南|SRP|shijingshannan|sjsn|1533@sjt|邵家堂|SJJ|shaojiatang|sjt|1534@sjx|三江县|SOZ|sanjiangxian|sjx|1535@sjz|三家寨|SMM|sanjiazhai|sjz|1536@sjz|十家子|SJD|shijiazi|sjz|1537@sjz|松江镇|OZL|songjiangzhen|sjz|1538@sjz|施家嘴|SHM|shijiazui|sjz|1539@sjz|深井子|SWT|shenjingzi|sjz|1540@sld|什里店|OMP|shilidian|sld|1541@sle|疏勒|SUR|shule|sl|1542@slh|疏勒河|SHJ|shulehe|slh|1543@slh|舍力虎|VLD|shelihu|slh|1544@sli|石磷|SPB|shilin|sl|1545@sli|绥棱|SIB|suiling|sl|1546@sli|石岭|SOL|shiling|sl|1547@sli|石林|SLM|shilin|sl|1548@sln|石林南|LNM|shilinnan|sln|1549@slo|石龙|SLQ|shilong|sl|1550@slq|萨拉齐|SLC|salaqi|slq|1551@slu|索伦|SNT|suolun|sl|1552@slu|商洛|OLY|shangluo|sl|1553@slz|沙岭子|SLP|shalingzi|slz|1554@smb|石门县北|VFQ|shimenxianbei|smxb|1555@smn|三门峡南|SCF|sanmenxianan|smxn|1556@smx|三门县|OQH|sanmenxian|smx|1557@smx|石门县|OMQ|shimenxian|smx|1558@smx|三门峡西|SXF|sanmenxiaxi|smxx|1559@sni|肃宁|SYP|suning|sn|1560@son|宋|SOB|song|s|1561@spa|双牌|SBZ|shuangpai|sp|1562@spd|四平东|PPT|sipingdong|spd|1563@spi|遂平|SON|suiping|sp|1564@spt|沙坡头|SFJ|shapotou|spt|1565@sqn|商丘南|SPF|shangqiunan|sqn|1566@squ|水泉|SID|shuiquan|sq|1567@sqx|石泉县|SXY|shiquanxian|sqx|1568@sqz|石桥子|SQT|shiqiaozi|sqz|1569@src|石人城|SRB|shirencheng|src|1570@sre|石人|SRL|shiren|sr|1571@ssh|山市|SQB|shanshi|ss|1572@ssh|神树|SWB|shenshu|ss|1573@ssh|鄯善|SSR|shanshan|ss|1574@ssh|三水|SJQ|sanshui|ss|1575@ssh|泗水|OSK|sishui|ss|1576@ssh|石山|SAD|shishan|ss|1577@ssh|松树|SFT|songshu|ss|1578@ssh|首山|SAT|shoushan|ss|1579@ssj|三十家|SRD|sanshijia|ssj|1580@ssp|三十里堡|SST|sanshilipu|sslb|1581@ssz|松树镇|SSL|songshuzhen|ssz|1582@sta|松桃|MZQ|songtao|st|1583@sth|索图罕|SHX|suotuhan|sth|1584@stj|三堂集|SDH|santangji|stj|1585@sto|石头|OTB|shitou|st|1586@sto|神头|SEV|shentou|st|1587@stu|沙沱|SFM|shatuo|st|1588@swa|上万|SWP|shangwan|sw|1589@swu|孙吴|SKB|sunwu|sw|1590@swx|沙湾县|SXR|shawanxian|swx|1591@sxi|遂溪|SXZ|suixi|sx|1592@sxi|沙县|SAS|shaxian|sx|1593@sxi|绍兴|SOH|shaoxing|sx|1594@sxi|歙县|OVH|shexian|sx|1595@sxi|石岘|SXL|shixian|sj|1596@sxp|上西铺|SXM|shangxipu|sxp|1597@sxz|石峡子|SXJ|shixiazi|sxz|1598@sya|绥阳|SYB|suiyang|sy|1599@sya|沭阳|FMH|shuyang|sy|1600@sya|寿阳|SYV|shouyang|sy|1601@sya|水洋|OYP|shuiyang|sy|1602@syc|三阳川|SYJ|sanyangchuan|syc|1603@syd|上腰墩|SPJ|shangyaodun|syd|1604@syi|三营|OEJ|sanying|sy|1605@syi|顺义|SOP|shunyi|sy|1606@syj|三义井|OYD|sanyijing|syj|1607@syp|三源浦|SYL|sanyuanpu|syp|1608@syu|三原|SAY|sanyuan|sy|1609@syu|上虞|BDH|shangyu|sy|1610@syu|上园|SUD|shangyuan|sy|1611@syu|水源|OYJ|shuiyuan|sy|1612@syz|桑园子|SAJ|sangyuanzi|syz|1613@szb|绥中北|SND|suizhongbei|szb|1614@szb|苏州北|OHH|suzhoubei|szb|1615@szd|宿州东|SRH|suzhoudong|szd|1616@szd|深圳东|BJQ|shenzhendong|szd|1617@szh|深州|OZP|shenzhou|sz|1618@szh|孙镇|OZY|sunzhen|sz|1619@szh|绥中|SZD|suizhong|sz|1620@szh|尚志|SZB|shangzhi|sz|1621@szh|师庄|SNM|shizhuang|sz|1622@szi|松滋|SIN|songzi|sz|1623@szo|师宗|SEM|shizong|sz|1624@szq|苏州园区|KAH|suzhouyuanqu|szyq|1625@szq|苏州新区|ITH|suzhouxinqu|szxq|1626@tan|泰安|TMK|taian|ta|1627@tan|台安|TID|taian|ta|1628@tay|通安驿|TAJ|tonganyi|tay|1629@tba|桐柏|TBF|tongbai|tb|1630@tbe|通北|TBB|tongbei|tb|1631@tch|汤池|TCX|tangchi|tc|1632@tch|桐城|TTH|tongcheng|tc|1633@tch|郯城|TZK|tancheng|tc|1634@tch|铁厂|TCL|tiechang|tc|1635@tcu|桃村|TCK|taocun|tc|1636@tda|通道|TRQ|tongdao|td|1637@tdo|田东|TDZ|tiandong|td|1638@tga|天岗|TGL|tiangang|tg|1639@tgl|土贵乌拉|TGC|togrogul|tgwl|1640@tgo|通沟|TOL|tonggou|tg|1641@tgu|太谷|TGV|taigu|tg|1642@tha|塔哈|THX|taha|th|1643@tha|棠海|THM|tanghai|th|1644@the|唐河|THF|tanghe|th|1645@the|泰和|THG|taihe|th|1646@thu|太湖|TKH|taihu|th|1647@tji|团结|TIX|tuanjie|tj|1648@tjj|谭家井|TNJ|tanjiajing|tjj|1649@tjt|陶家屯|TOT|taojiatun|tjt|1650@tjw|唐家湾|PDQ|tangjiawan|tjw|1651@tjz|统军庄|TZP|tongjunzhuang|tjz|1652@tka|泰康|TKX|taikang|tk|1653@tld|吐列毛杜|TMD|tuliemaodu|tlmd|1654@tlh|图里河|TEX|tulihe|tlh|1655@tli|亭亮|TIZ|tingliang|tl|1656@tli|田林|TFZ|tianlin|tl|1657@tli|铜陵|TJH|tongling|tl|1658@tli|铁力|TLB|tieli|tl|1659@tlx|铁岭西|PXT|tielingxi|tlx|1660@tme|天门|TMN|tianmen|tm|1661@tmn|天门南|TNN|tianmennan|tmn|1662@tms|太姥山|TLS|taimushan|tls|1663@tmt|土牧尔台|TRC|tomortei|tmet|1664@tmz|土门子|TCJ|tumenzi|tmz|1665@tna|潼南|TVW|tongnan|tn|1666@tna|洮南|TVT|taonan|tn|1667@tpc|太平川|TIT|taipingchuan|tpc|1668@tpz|太平镇|TEB|taipingzhen|tpz|1669@tqi|图强|TQX|tuqiang|tq|1670@tqi|台前|TTK|taiqian|tq|1671@tql|天桥岭|TQL|tianqiaoling|tql|1672@tqz|土桥子|TQJ|tuqiaozi|tqz|1673@tsc|汤山城|TCT|tangshancheng|tsc|1674@tsh|桃山|TAB|taoshan|ts|1675@tsz|塔石嘴|TIM|tashizui|tsz|1676@ttu|通途|TUT|tongtu|tt|1677@twh|汤旺河|THB|tangwanghe|twh|1678@txi|同心|TXJ|tongxin|tx|1679@txi|土溪|TSW|tuxi|tx|1680@txi|桐乡|TCH|tongxiang|tx|1681@tya|田阳|TRZ|tianyang|ty|1682@tyi|桃映|TKQ|taoying|ty|1683@tyi|天义|TND|tianyi|ty|1684@tyi|汤阴|TYF|tangyin|ty|1685@tyl|驼腰岭|TIL|tuoyaoling|tyl|1686@tys|太阳山|TYJ|taiyangshan|tys|1687@tyu|汤原|TYB|tangyuan|ty|1688@tyy|塔崖驿|TYP|tayanyi|tyy|1689@tzd|滕州东|TEK|tengzhoudong|tzd|1690@tzh|台州|TZH|taizhou|tz|1691@tzh|天祝|TZJ|tianzhu|tz|1692@tzh|滕州|TXK|tengzhou|tz|1693@tzh|天镇|TZV|tianzhen|tz|1694@tzl|桐子林|TEW|tongzilin|tzl|1695@tzs|天柱山|QWH|tianzhushan|tzs|1696@wan|文安|WBP|wenan|wa|1697@wan|武安|WAP|wuan|wa|1698@waz|王安镇|WVP|wanganzhen|waz|1699@wca|旺苍|WEW|wangcang|wc|1700@wcg|五叉沟|WCT|wuchagou|wcg|1701@wch|文昌|WEQ|wenchang|wc|1702@wch|温春|WDB|wenchun|wc|1703@wdc|五大连池|WRB|wudalianchi|wdlc|1704@wde|文登|WBK|wendeng|wd|1705@wdg|五道沟|WDL|wudaogou|wdg|1706@wdh|五道河|WHP|wudaohe|wdh|1707@wdi|文地|WNZ|wendi|wd|1708@wdo|卫东|WVT|weidong|wd|1709@wds|武当山|WRN|wudangshan|wds|1710@wdu|望都|WDP|wangdu|wd|1711@weh|乌尔旗汗|WHX|orqohan|weqh|1712@wfa|潍坊|WFK|weifang|wf|1713@wft|万发屯|WFB|wanfatun|wft|1714@wfu|王府|WUT|wangfu|wf|1715@wfx|瓦房店西|WXT|wafangdianxi|wfdx|1716@wga|王岗|WGB|wanggang|wg|1717@wgo|武功|WGY|wugong|wg|1718@wgo|湾沟|WGL|wangou|wg|1719@wgt|吴官田|WGM|wuguantian|wgt|1720@wha|乌海|WVC|wuhai|wh|1721@whe|苇河|WHB|weihe|wh|1722@whu|卫辉|WHF|weihui|wh|1723@wjc|吴家川|WCJ|wujiachuan|wjc|1724@wji|五家|WUB|wujia|wj|1725@wji|威箐|WAM|weiqing|wq|1726@wji|午汲|WJP|wuji|wj|1727@wji|渭津|WJL|weijin|wj|1728@wjw|王家湾|WJJ|wangjiawan|wjw|1729@wke|倭肯|WQB|woken|wk|1730@wks|五棵树|WKT|wukeshu|wks|1731@wlb|五龙背|WBT|wulongbei|wlb|1732@wld|乌兰哈达|WLC|ulanhad|wlhd|1733@wle|万乐|WEB|wanle|wl|1734@wlg|瓦拉干|WVX|walagan|wlg|1735@wli|温岭|VHH|wenling|wl|1736@wli|五莲|WLK|wulian|wl|1737@wlq|乌拉特前旗|WQC|uradqranqi|wltqq|1738@wls|乌拉山|WSC|wulashan|wls|1739@wlt|卧里屯|WLX|wolitun|wlt|1740@wnb|渭南北|WBY|weinanbei|wnb|1741@wne|乌奴耳|WRX|onor|wne|1742@wni|万宁|WNQ|wanning|wn|1743@wni|万年|WWG|wannian|wn|1744@wnn|渭南南|WVY|weinannan|wnn|1745@wnz|渭南镇|WNJ|weinanzhen|wnz|1746@wpi|沃皮|WPT|wopi|wp|1747@wpu|吴堡|WUY|wupu|wb|1748@wqi|吴桥|WUP|wuqiao|wq|1749@wqi|汪清|WQL|wangqing|wq|1750@wqi|武清|WWP|wuqing|wq|1751@wqu|温泉|WQM|wenquan|wq|1752@wsh|武山|WSJ|wushan|ws|1753@wsh|文水|WEV|wenshui|ws|1754@wsz|魏善庄|WSP|weishanzhuang|wsz|1755@wto|王瞳|WTP|wangtong|wt|1756@wts|五台山|WSV|wutaishan|wts|1757@wtz|王团庄|WZJ|wangtuanzhuang|wtz|1758@wwu|五五|WVR|wuwu|ww|1759@wxd|无锡东|WGH|wuxidong|wxd|1760@wxi|卫星|WVB|weixing|wx|1761@wxi|闻喜|WXV|wenxi|wx|1762@wxi|武乡|WVV|wuxiang|wx|1763@wxq|无锡新区|IFH|wuxixinqu|wxxq|1764@wxu|武穴|WXN|wuxue|wx|1765@wxu|吴圩|WYZ|wuxu|wy|1766@wya|王杨|WYB|wangyang|wy|1767@wyi|五营|WWB|wuying|wy|1768@wyi|武义|RYH|wuyi|wy|1769@wyt|瓦窑田|WIM|wayaotian|wjt|1770@wyu|五原|WYC|wuyuan|wy|1771@wzg|苇子沟|WZL|weizigou|wzg|1772@wzh|韦庄|WZY|weizhuang|wz|1773@wzh|五寨|WZV|wuzhai|wz|1774@wzt|王兆屯|WZB|wangzhaotun|wzt|1775@wzz|微子镇|WQP|weizizhen|wzz|1776@wzz|魏杖子|WKD|weizhangzi|wzz|1777@xan|新安|EAM|xinan|xa|1778@xan|兴安|XAZ|xingan|xa|1779@xax|新安县|XAF|xinanxian|xax|1780@xba|新保安|XAP|xinbaoan|xba|1781@xbc|下板城|EBP|xiabancheng|xbc|1782@xbl|西八里|XLP|xibali|xbl|1783@xch|宣城|ECH|xuancheng|xc|1784@xch|兴城|XCD|xingcheng|xc|1785@xcu|小村|XEM|xiaocun|xc|1786@xcy|新绰源|XRX|xinchuoyuan|xcy|1787@xcz|下城子|XCB|xiachengzi|xcz|1788@xcz|新城子|XCT|xinchengzi|xcz|1789@xde|喜德|EDW|xide|xd|1790@xdj|小得江|EJM|xiaodejiang|xdj|1791@xdm|西大庙|XMP|xidamiao|xdm|1792@xdo|小董|XEZ|xiaodong|xd|1793@xdo|小东|XOD|xiaodong|xd|1794@xdp|西斗铺|XPC|xidoupu|xdp|1795@xfe|息烽|XFW|xifeng|xf|1796@xfe|信丰|EFG|xinfeng|xf|1797@xfe|襄汾|XFV|xiangfen|xf|1798@xga|新干|EGG|xingan|xg|1799@xga|孝感|XGN|xiaogan|xg|1800@xgc|西固城|XUJ|xigucheng|xgc|1801@xgy|夏官营|XGJ|xiaguanying|xgy|1802@xgz|西岗子|NBB|xigangzi|xgz|1803@xhe|襄河|XXB|xianghe|xh|1804@xhe|新和|XIR|xinhe|xh|1805@xhe|宣和|XWJ|xuanhe|xh|1806@xhj|斜河涧|EEP|xiehejian|xhj|1807@xht|新华屯|XAX|xinhuatun|xht|1808@xhu|新华|XHB|xinhua|xh|1809@xhu|新化|EHQ|xinhua|xh|1810@xhu|宣化|XHP|xuanhua|xh|1811@xhx|兴和西|XEC|xinghexi|xhx|1812@xhy|小河沿|XYD|xiaoheyan|xhy|1813@xhy|下花园|XYP|xiahuayuan|xhy|1814@xhz|小河镇|EKY|xiaohezhen|xhz|1815@xji|徐家|XJB|xujia|xj|1816@xji|峡江|EJG|xiajiang|xj|1817@xji|新绛|XJV|xinjiang|xj|1818@xji|辛集|ENP|xinji|xj|1819@xji|新江|XJM|xinjiang|xj|1820@xjk|西街口|EKM|xijiekou|xjk|1821@xjt|许家屯|XJT|xujiatun|xjt|1822@xjt|许家台|XTJ|xujiatai|xjt|1823@xjz|谢家镇|XMT|xiejiazhen|xjz|1824@xka|兴凯|EKB|xingkai|xk|1825@xla|小榄|EAQ|xiaolan|xl|1826@xla|香兰|XNB|xianglan|xl|1827@xld|兴隆店|XDD|xinglongdian|xld|1828@xle|新乐|ELP|xinle|xl|1829@xli|新林|XPX|xinlin|xl|1830@xli|小岭|XLB|xiaoling|xl|1831@xli|新李|XLJ|xinli|xl|1832@xli|西林|XYB|xilin|xl|1833@xli|西柳|GCT|xiliu|xl|1834@xli|仙林|XPH|xianlin|xl|1835@xlt|新立屯|XLD|xinlitun|xlt|1836@xlx|小路溪|XLM|xiaoluxi|xlx|1837@xlz|兴隆镇|XZB|xinglongzhen|xlz|1838@xlz|新立镇|XGT|xinlizhen|xlz|1839@xmi|新民|XMD|xinmin|xm|1840@xms|西麻山|XMB|ximashan|xms|1841@xmt|下马塘|XAT|xiamatang|xmt|1842@xna|孝南|XNV|xiaonan|xn|1843@xnb|咸宁北|XRN|xianningbei|xnb|1844@xni|兴宁|ENQ|xingning|xn|1845@xni|咸宁|XNN|xianning|xn|1846@xpi|西平|XPN|xiping|xp|1847@xpi|兴平|XPY|xingping|xp|1848@xpt|新坪田|XPM|xinpingtian|xpt|1849@xpu|霞浦|XOS|xiapu|xp|1850@xpu|溆浦|EPQ|xupu|xp|1851@xpu|犀浦|XIW|xipu|xp|1852@xqi|新青|XQB|xinqing|xq|1853@xqi|新邱|XQD|xinqiu|xq|1854@xqp|兴泉堡|XQJ|xingquanpu|xqp|1855@xrq|仙人桥|XRL|xianrenqiao|xrq|1856@xsg|小寺沟|ESP|xiaosigou|xsg|1857@xsh|杏树|XSB|xingshu|xs|1858@xsh|夏石|XIZ|xiashi|xs|1859@xsh|浠水|XZN|xishui|xs|1860@xsh|下社|XSV|xiashe|xs|1861@xsh|徐水|XSP|xushui|xs|1862@xsh|小哨|XAM|xiaoshao|xs|1863@xsp|新松浦|XOB|xinsongpu|xsp|1864@xst|杏树屯|XDT|xingshutun|xst|1865@xsw|许三湾|XSJ|xusanwan|xsw|1866@xta|湘潭|XTQ|xiangtan|xt|1867@xta|邢台|XTP|xingtai|xt|1868@xtx|仙桃西|XAN|xiantaoxi|xtx|1869@xtz|下台子|EIP|xiataizi|xtz|1870@xwe|徐闻|XJQ|xuwen|xw|1871@xwp|新窝铺|EPD|xinwopu|xwp|1872@xwu|修武|XWF|xiuwu|xw|1873@xxi|新县|XSN|xinxian|xx|1874@xxi|息县|ENN|xixian|xx|1875@xxi|西乡|XQY|xixiang|xx|1876@xxi|湘乡|XXQ|xiangxiang|xx|1877@xxi|西峡|XIF|xixia|xx|1878@xxi|孝西|XOV|xiaoxi|xx|1879@xxj|小新街|XXM|xiaoxinjie|xxj|1880@xxx|新兴县|XGQ|xinxingxian|xxx|1881@xxz|西小召|XZC|xixiaozhao|xxz|1882@xxz|小西庄|XXP|xiaoxizhuang|xxz|1883@xya|向阳|XDB|xiangyang|xy|1884@xya|旬阳|XUY|xunyang|xy|1885@xyb|旬阳北|XBY|xunyangbei|xyb|1886@xyd|襄阳东|XWN|xiangyangdong|xyd|1887@xye|兴业|SNZ|xingye|xy|1888@xyg|小雨谷|XHM|xiaoyugu|xyg|1889@xyi|信宜|EEQ|xinyi|xy|1890@xyj|小月旧|XFM|xiaoyuejiu|xyj|1891@xyq|小扬气|XYX|xiaoyangqi|xyq|1892@xyu|祥云|EXM|xiangyun|xy|1893@xyu|襄垣|EIF|xiangyuan|xy|1894@xyx|夏邑县|EJH|xiayixian|xyx|1895@xyy|新友谊|EYB|xinyouyi|xyy|1896@xyz|新阳镇|XZJ|xinyangzhen|xyz|1897@xzd|徐州东|UUH|xuzhoudong|xzd|1898@xzf|新帐房|XZX|xinzhangfang|xzf|1899@xzh|悬钟|XRP|xuanzhong|xz|1900@xzh|新肇|XZT|xinzhao|xz|1901@xzh|忻州|XXV|xinzhou|xz|1902@xzi|汐子|XZD|xizi|xz|1903@xzm|西哲里木|XRD|xizhelimu|xzlm|1904@xzz|新杖子|ERP|xinzhangzi|xzz|1905@yan|姚安|YAC|yaoan|ya|1906@yan|依安|YAX|yian|ya|1907@yan|永安|YAS|yongan|ya|1908@yax|永安乡|YNB|yonganxiang|yax|1909@ybc|渔坝村|YBM|yubacun|ybc|1910@ybl|亚布力|YBB|yabuli|ybl|1911@ybs|元宝山|YUD|yuanbaoshan|ybs|1912@yca|羊草|YAB|yangcao|yc|1913@ycd|秧草地|YKM|yangcaodi|ycd|1914@ych|阳澄湖|AIH|yangchenghu|ych|1915@ych|迎春|YYB|yingchun|yc|1916@ych|叶城|YER|yecheng|yc|1917@ych|盐池|YKJ|yanchi|yc|1918@ych|砚川|YYY|yanchuan|yc|1919@ych|阳春|YQQ|yangchun|yc|1920@ych|宜城|YIN|yicheng|yc|1921@ych|应城|YHN|yingcheng|yc|1922@ych|禹城|YCK|yucheng|yc|1923@ych|晏城|YEK|yancheng|yc|1924@ych|羊场|YED|yangchang|yc|1925@ych|阳城|YNF|yangcheng|yc|1926@ych|阳岔|YAL|yangcha|yc|1927@ych|郓城|YPK|yuncheng|yc|1928@ych|雁翅|YAP|yanchi|yc|1929@ycl|云彩岭|ACP|yuncailing|ycl|1930@ycx|虞城县|IXH|yuchengxian|ycx|1931@ycz|营城子|YCT|yingchengzi|ycz|1932@yde|永登|YDJ|yongdeng|yd|1933@yde|英德|YDQ|yingde|yd|1934@ydi|尹地|YDM|yindi|yd|1935@ydi|永定|YGS|yongding|yd|1936@yds|雁荡山|YGH|yandangshan|yds|1937@ydu|于都|YDG|yudu|yd|1938@ydu|园墩|YAJ|yuandun|yd|1939@ydx|英德西|IIQ|yingdexi|ydx|1940@yfu|永福|YFZ|yongfu|yf|1941@yfy|永丰营|YYM|yongfengying|yfy|1942@yga|杨岗|YRB|yanggang|yg|1943@yga|阳高|YOV|yanggao|yg|1944@ygu|阳谷|YIK|yanggu|yg|1945@yha|友好|YOB|youhao|yh|1946@yha|余杭|EVH|yuhang|yh|1947@yhc|沿河城|YHP|yanhecheng|yhc|1948@yhu|岩会|AEP|yanhui|yh|1949@yjh|羊臼河|YHM|yangjiuhe|yjh|1950@yji|永嘉|URH|yongjia|yj|1951@yji|营街|YAM|yingjie|yj|1952@yji|盐津|AEW|yanjin|yj|1953@yji|余江|YHG|yujiang|yj|1954@yji|叶集|YCH|yeji|yj|1955@yji|燕郊|AJP|yanjiao|yj|1956@yji|姚家|YAT|yaojia|yj|1957@yjj|岳家井|YGJ|yuejiajing|yjj|1958@yjp|一间堡|YJT|yijianpu|yjb|1959@yjs|英吉沙|YIR|yingjisha|yjs|1960@yjs|云居寺|AFP|yunjusi|yjs|1961@yjz|燕家庄|AZK|yanjiazhuang|yjz|1962@yka|永康|RFH|yongkang|yk|1963@ykd|营口东|YGT|yingkoudong|ykd|1964@yla|银浪|YJX|yinlang|yl|1965@yla|永郎|YLW|yonglang|yl|1966@ylb|宜良北|YSM|yiliangbei|ylb|1967@yld|永乐店|YDY|yongledian|yld|1968@ylh|伊拉哈|YLX|yilaha|ylh|1969@yli|伊林|YLB|yilin|yl|1970@yli|彝良|ALW|yiliang|yl|1971@yli|杨林|YLM|yanglin|yl|1972@ylp|余粮堡|YLD|yuliangpu|ylb|1973@ylq|杨柳青|YQP|yangliuqing|ylq|1974@ylt|月亮田|YUM|yueliangtian|ylt|1975@ylw|亚龙湾|TWQ|yalongwan|ylw|1976@ylz|杨陵镇|YSY|yanglingzhen|ylz|1977@yma|义马|YMF|yima|ym|1978@yme|云梦|YMN|yunmeng|ym|1979@ymo|元谋|YMM|yuanmou|ym|1980@ymp|阳明堡|YVV|yangmingpu|ymp|1981@yms|一面山|YST|yimianshan|yms|1982@ymz|玉门镇|YXJ|yumenzhen|ymz|1983@yna|沂南|YNK|yinan|yn|1984@yna|宜耐|YVM|yinai|yn|1985@ynd|伊宁东|YNR|yiningdong|ynd|1986@ypl|一平浪|YIM|yipinglang|ypl|1987@yps|营盘水|YZJ|yingpanshui|yps|1988@ypu|羊堡|ABM|yangpu|yp|1989@ypw|营盘湾|YPC|yingpanwan|ypw|1990@yqb|阳泉北|YPP|yangquanbei|yqb|1991@yqi|乐清|UPH|yueqing|yq|1992@yqi|焉耆|YSR|yanqi|yq|1993@yqi|源迁|AQK|yuanqian|yq|1994@yqt|姚千户屯|YQT|yaoqianhutun|yqht|1995@yqu|阳曲|YQV|yangqu|yq|1996@ysg|榆树沟|YGP|yushugou|ysg|1997@ysh|月山|YBF|yueshan|ys|1998@ysh|玉石|YSJ|yushi|ys|1999@ysh|偃师|YSF|yanshi|ys|2000@ysh|沂水|YUK|yishui|ys|2001@ysh|榆社|YSV|yushe|ys|2002@ysh|窑上|ASP|yaoshang|ys|2003@ysh|元氏|YSP|yuanshi|ys|2004@ysl|杨树岭|YAD|yangshuling|ysl|2005@ysp|野三坡|AIP|yesanpo|ysp|2006@yst|榆树屯|YSX|yushutun|yst|2007@yst|榆树台|YUT|yushutai|yst|2008@ysz|鹰手营子|YIP|yingshouyingzi|ysyz|2009@yta|源潭|YTQ|yuantan|yt|2010@ytp|牙屯堡|YTZ|yatunpu|ytb|2011@yts|烟筒山|YSL|yantongshan|yts|2012@ytt|烟筒屯|YUX|yantongtun|ytt|2013@yws|羊尾哨|YWM|yangweishao|yws|2014@yxi|越西|YHW|yuexi|yx|2015@yxi|攸县|YOG|youxian|yx|2016@yxi|玉溪|YXM|yuxi|yx|2017@yxi|永修|ACG|yongxiu|yx|2018@yya|酉阳|AFW|youyang|yy|2019@yya|余姚|YYH|yuyao|yy|2020@yyd|弋阳东|YIG|yiyangdong|yyd|2021@yyd|岳阳东|YIQ|yueyangdong|yyd|2022@yyi|阳邑|ARP|yangyi|yy|2023@yyu|鸭园|YYL|yayuan|yy|2024@yyz|鸳鸯镇|YYJ|yuanyangzhen|yyz|2025@yzb|燕子砭|YZY|yanzibian|yzb|2026@yzh|宜州|YSZ|yizhou|yz|2027@yzh|仪征|UZH|yizheng|yz|2028@yzh|兖州|YZK|yanzhou|yz|2029@yzi|迤资|YQM|yizi|yz|2030@yzw|羊者窝|AEM|yangzhewo|wzw|2031@yzz|杨杖子|YZD|yangzhangzi|yzz|2032@zan|镇安|ZEY|zhenan|za|2033@zan|治安|ZAD|zhian|za|2034@zba|招柏|ZBP|zhaobai|zb|2035@zbw|张百湾|ZUP|zhangbaiwan|zbw|2036@zch|枝城|ZCN|zhicheng|zc|2037@zch|子长|ZHY|zichang|zc|2038@zch|诸城|ZQK|zhucheng|zc|2039@zch|邹城|ZIK|zoucheng|zc|2040@zch|赵城|ZCV|zhaocheng|zc|2041@zda|章党|ZHT|zhangdang|zd|2042@zdo|肇东|ZDB|zhaodong|zd|2043@zfp|照福铺|ZFM|zhaofupu|zfp|2044@zgt|章古台|ZGD|zhanggutai|zgt|2045@zgu|赵光|ZGB|zhaoguang|zg|2046@zhe|中和|ZHX|zhonghe|zh|2047@zhm|中华门|VNH|zhonghuamen|zhm|2048@zjb|枝江北|ZIN|zhijiangbei|zjb|2049@zjc|钟家村|ZJY|zhongjiacun|zjc|2050@zjg|朱家沟|ZUB|zhujiagou|zjg|2051@zjg|紫荆关|ZYP|zijingguan|zjg|2052@zji|周家|ZOB|zhoujia|zj|2053@zji|诸暨|ZDH|zhuji|zj|2054@zjn|镇江南|ZEH|zhenjiangnan|zjn|2055@zjt|周家屯|ZOD|zhoujiatun|zjt|2056@zjt|郑家屯|ZJD|zhengjiatun|zjt|2057@zjw|褚家湾|CWJ|zhujiawan|cjw|2058@zjx|湛江西|ZWQ|zhanjiangxi|zjx|2059@zjy|朱家窑|ZUJ|zhujiayao|zjy|2060@zjz|曾家坪子|ZBW|caojiapingzi|zjpz|2061@zla|张兰|ZLV|zhanglan|zla|2062@zla|镇赉|ZLT|zhenlai|zl|2063@zli|枣林|ZIV|zaolin|zl|2064@zlt|扎鲁特|ZLD|zhalute|zlt|2065@zlx|扎赉诺尔西|ZXX|jalainurxi|zlnex|2066@zmt|樟木头|ZOQ|zhangmutou|zmt|2067@zmu|中牟|ZGF|zhongmu|zm|2068@znd|中宁东|ZDJ|zhongningdong|znd|2069@zni|中宁|VNJ|zhongning|zn|2070@znn|中宁南|ZNJ|zhongningnan|znn|2071@zpi|镇平|ZPF|zhenping|zp|2072@zpi|漳平|ZPS|zhangping|zp|2073@zpu|泽普|ZPR|zepu|zp|2074@zqi|枣强|ZVP|zaoqiang|zq|2075@zqi|张桥|ZQY|zhangqiao|zq|2076@zqi|章丘|ZTK|zhangqiu|zq|2077@zrh|朱日和|ZRC|zhurihe|zrh|2078@zrl|泽润里|ZLM|zerunli|zrl|2079@zsb|中山北|ZGQ|zhongshanbei|zsb|2080@zsd|樟树东|ZOG|zhangshudong|zsd|2081@zsh|中山|ZSQ|zhongshan|zs|2082@zsh|柞水|ZSY|zhashui|zs|2083@zsh|钟山|ZSZ|zhongshan|zs|2084@zsh|樟树|ZSG|zhangshu|zs|2085@zwo|珠窝|ZOP|zhuwo|zw|2086@zwt|张维屯|ZWB|zhangweitun|zwt|2087@zwu|彰武|ZWD|zhangwu|zw|2088@zxi|棕溪|ZOY|zongxi|zx|2089@zxi|钟祥|ZTN|zhongxiang|zx|2090@zxi|资溪|ZXS|zixi|zx|2091@zxi|镇西|ZVT|zhenxi|zx|2092@zxi|张辛|ZIP|zhangxin|zx|2093@zxq|正镶白旗|ZXC|zhengxiangbaiqi|zxbq|2094@zya|紫阳|ZVY|ziyang|zy|2095@zya|枣阳|ZYN|zaoyang|zy|2096@zyb|竹园坝|ZAW|zhuyuanba|zyb|2097@zye|张掖|ZYJ|zhangye|zy|2098@zyu|镇远|ZUW|zhenyuan|zy|2099@zyx|朱杨溪|ZXW|zhuyangxi|zyx|2100@zzd|漳州东|GOS|zhangzhoudong|zzd|2101@zzh|漳州|ZUS|zhangzhou|zz|2102@zzh|壮志|ZUX|zhuangzhi|zz|2103@zzh|子洲|ZZY|zizhou|zz|2104@zzh|中寨|ZZM|zhongzhai|zz|2105@zzh|涿州|ZXP|zhuozhou|zz|2106@zzi|咋子|ZAL|zhazi|zz|2107@zzs|卓资山|ZZC|zhuozishan|zzs|2108@zzx|株洲西|ZAQ|zhuzhouxi|zzx|2109@ayd|安阳东|ADF|anyangdong|ayd|2110@bdd|保定东|BMP|baodingdong|bdd|2111@cxi|长兴|CBH|changxing|cx|2112@cya|长阳|CYN|changyang|cy|2113@deh|东二道河|DRB|dongerdaohe|dedh|2114@dju|大苴|DIM|daju|dj|2115@dqg|大青沟|DSD|daqinggou|dqg|2116@dqi|德清|DRH|deqing|dq|2117@dzd|定州东|DOP|dingzhoudong|dzd|2118@fch|富川|FDZ|fuchuan|fc|2119@fyu|抚远|FYB|fuyuan|fy|2120@gbd|高碑店东|GMP|gaobeidiandong|gbdd|2121@gju|革居|GEM|geju|gj|2122@gmc|光明城|IMQ|guangmingcheng|gmc|2123@gyx|高邑西|GNP|gaoyixi|gyx|2124@hbd|鹤壁东|HFF|hebidong|hbd|2125@hcg|寒葱沟|HKB|hanconggou|hcg|2126@hdd|邯郸东|HPP|handandong|hdd|2127@hfc|合肥北城|COH|hefeibeicheng|hfbc|2128@hhe|洪河|HPB|honghe|hh|2129@hme|虎门|IUQ|humen|hm|2130@hmn|哈密南|HLR|haminan|hmn|2131@hnd|淮南东|HOH|huainandong|hnd|2132@jni|江宁|JJH|jiangning|jn|2133@jrx|句容西|JWH|jurongxi|jrx|2134@jsh|建水|JSM|jianshui|js|2135@klu|库伦|KLD|kulun|kl|2136@ldy|离堆公园|INW|liduigongyuan|ldgy|2137@lhx|漯河西|LBN|luohexi|lhx|2138@lsh|溧水|LDH|lishui|ls|2139@lya|溧阳|LEH|liyang|ly|2140@mgd|明港东|MDN|minggangdong|mgd|2141@mzb|蒙自北|MBM|mengzibei|mzb|2142@qfe|前锋|QFB|qianfeng|qf|2143@qsh|庆盛|QSQ|qingsheng|qs|2144@sxb|绍兴北|SLH|shaoxingbei|sxb|2145@syb|上虞北|SSH|shangyubei|syb|2146@szb|深圳北|IOQ|shenzhenbei|szb|2147@tha|通海|TAM|tonghai|th|2148@wws|瓦屋山|WAH|wawushan|wws|2149@xcd|许昌东|XVF|xuchangdong|xcd|2150@xgb|孝感北|XJN|xiaoganbei|xgb|2151@xtd|邢台东|EDP|xingtaidong|xtd|2152@xxd|新乡东|EGF|xinxiangdong|xxd|2153@xyc|西阳村|XQF|xiyangcun|xyc|2154@xyd|信阳东|OYN|xinyangdong|xyd|2155@ybl|迎宾路|YFW|yingbinlu|ybl|2156@yge|雨格|VTM|yuge|yg|2157@yxi|宜兴|YUH|yixing|yx|2158@yyb|余姚北|CTH|yuyaobei|yyb|2159@zdc|正定机场|ZHP|zhengdingjichang|zdjc|2160@zji|织金|IZW|zhijin|zj|2161@zmx|驻马店西|ZLN|zhumadianxi|zmdx|2162@zqi|庄桥|ZQH|zhuangqiao|zq|2163@zzd|涿州东|ZAP|zhuozhoudong|zzd|2164@zzd|卓资东|ZDC|zhuozidong|zzd|2165@zzd|郑州东|ZAF|zhengzhoudong|zzd|2166'
  station_list = station_names.split('@')
  station_list = station_list[1:] # The first one is empty, skip it

  for station in station_list:
    items = station.split('|') # bjb|北京北|VAP|beijingbei|bjb|0
    station_dict[items[1]] = items[2]
  
  return station_dict

#------------------------------------------------------------------------------
# Convert train station name to telecode
def stationName2Telecode(name):
  if station_dict.has_key(name):
    return station_dict[name]
  else:
    return ''

#------------------------------------------------------------------------------
# Get current time and convert to string
def getTime():
  return time.strftime("%Y-%m-%d %X",time.localtime())

#------------------------------------------------------------------------------
# Card type
# 证件类型: 
# 1->二代身份证
# 2->一代身份证
# C->港澳通行证
# G->台湾通行证
# B->护照
def getCardType(cardtype):
  d = {
    '1':u"二代身份证",
    '2':u"一代身份证",
    'C':u"港澳通行证",
    'G':u"台湾通行证",
    'B':u"护照"
  }

  if d.has_key(cardtype):
    return d[cardtype]
  else:
    return u"未知证件类型"

#------------------------------------------------------------------------------
# Seat type
# 席别: 
# 1->硬座/无座
# 3->硬卧
# 4->软卧
# 7->一等软座
# 8->二等软座
# 9->商务座
# M->一等座
# O->二等座
# P->特等座
def getSeatType(seattype):
  d = {
    '1':u"硬座",#硬座/无座
    '3':u"硬卧",
    '4':u"软卧",
    '7':u"一等软座",
    '8':u"二等软座",
    '9':u"商务座",
    'M':u"一等座",
    'O':u"二等座",
    'P':u"特等座"
  }

  if d.has_key(seattype):
    return d[seattype]
  else:
    return u"未知席别"

#------------------------------------------------------------------------------
# Ticket type
# 票种类型
# 1->成人票
# 2->儿童票
# 3->学生票
# 4->残军票
def getTicketType(tickettype):
  d = {
    '1':u"成人票",
    '2':u"儿童票",
    '3':u"学生票",
    '4':u"残军票"
  }

  if d.has_key(tickettype):
    return d[tickettype]
  else:
    return u"未知票种"

#------------------------------------------------------------------------------
# Check date format
def checkDate(date):
  m = re.match(r'^\d{4}-\d{2}-\d{2}$',date) # 2013-01-10

  if m:
    return 1
  else:
    return 0

#------------------------------------------------------------------------------
# Input date
def inputDate():
  train_date = ''

  while 1:
    train_date = raw_input("")
    if checkDate(train_date):
      break
    else:
      print u"格式错误,请重新输入有效的乘车日期,如2013-02-01:"

  return train_date

#------------------------------------------------------------------------------
# Input station
def inputStation():
  station = ''

  while 1:
    station = raw_input("").decode("gb2312","ignore")
    telecode = stationName2Telecode(station)
    if telecode:
      break
    else:
      print u"站点错误,没有站点'%s',请重新输入:"%(station)

  return {"name":station,"telecode":telecode}

#------------------------------------------------------------------------------
# Check order result
def checkOrderResult(respInfo):
  key = u'席位已成功锁定'
  if respInfo.find(key) != -1:
    return 1

  key = u'待支付'
  if respInfo.find(key) != -1:
    return 1

  return 0

#------------------------------------------------------------------------------
# Send post request
def sendPostRequest(url,data,referer="https://dynamic.12306.cn/otsweb/order/confirmPassengerAction.do?method=init"):
  #print("Start post %s at %s"%(url,getTime()))
  post_timeout = 300
  req = urllib2.Request(url, data)
  req.add_header('Content-Type', "application/x-www-form-urlencoded")
  req.add_header('Referer',referer)

  resp = None
  tries = 0
  max_tries = 3
  while tries < max_tries:
    tries += 1
    try:
      resp = urllib2.urlopen(req,timeout=post_timeout*tries)
    except urllib2.HTTPError,e:
      print("Post %d times %s exception HTTPError code:"%(tries,url),e.code)
    except urllib2.URLError,e:
      print("Post %d times %s exception URLError reason:"%(tries,url),e.reason)
    except:
      print("Post %d times %s exception other"%(tries,url))
    if resp:
      break
  #print("Stop post %s at %s"%(url,getTime()))
  return resp

#------------------------------------------------------------------------------
# Send get request
def sendGetRequest(url,referer="https://dynamic.12306.cn/otsweb/order/confirmPassengerAction.do?method=init"):
  #print("Start get %s at %s"%(url,getTime()))
  get_timeout = 150
  req = urllib2.Request(url)
  req.add_header('Referer',referer)

  resp = None
  tries = 0
  max_tries = 3
  while tries < max_tries:
    tries += 1
    try:
      resp = urllib2.urlopen(req,timeout=get_timeout*tries)
    except urllib2.HTTPError,e:
      print("Get %d times %s exception HTTPError code:"%(tries,url),e.code)
    except urllib2.URLError,e:
      print("Get %d times %s exception URLError reason:"%(tries,url),e.reason)
    except:
      print("Get %d times %s exception other"%(tries,url))
    if resp:
      break
  #print("Stop get %s at %s"%(url,getTime()))
  return resp

#------------------------------------------------------------------------------
# Save picture code
# 请求验证图片, 并保存到本地
def getCaptcha(url):
  captcha = ''
  while 1:
    f = open("pic-code.jpeg","wb")
    f.write(urllib2.urlopen(url).read())
    f.close()
    print u"请输入4位图片验证码登陆(直接回车刷新):"
    captcha = raw_input("")
    if len(captcha) == 4:
      return captcha

#------------------------------------------------------------------------------
# Check login result
def checkLoginResult(respInfo):
  key = 'isLogin= true'
  if respInfo.find(key) != -1:
    return 1
  else:
    return 0

#------------------------------------------------------------------------------
# Login process
def login(username,password):
  #访问主页, 自动保存Cookie信息
  url = "https://dynamic.12306.cn/otsweb/"
  referer = "https://dynamic.12306.cn/otsweb/"
  resp = sendGetRequest(url,referer)

  url = "https://dynamic.12306.cn/otsweb/loginAction.do?method=init"
  referer = "https://dynamic.12306.cn/otsweb/"
  resp = sendGetRequest(url,referer)
  '''
  try:
    respInfo = resp.read()
    v0 = respInfo.find('jsversion=')
    v1 = respInfo.find('&method=loginJs')
    ver = respInfo[v0+len('jsversion='):v1]
    url = "https://dynamic.12306.cn/otsweb/dynamicJsAction.do?jsversion=" + ver + "&method=loginJs" # "https://dynamic.12306.cn/otsweb/dynamicJsAction.do?jsversion=3490&method=loginJs"
    referer = "https://dynamic.12306.cn/otsweb/loginAction.do?method=init"
    resp = sendPostRequest(url,{},referer)
  except:
    print(u"login()->sendPostRequest(%s)->resp.read() exception"%(url))
    return 0
  '''

  # 图片验证码
  captcha = getCaptcha("https://dynamic.12306.cn/otsweb/passCodeNewAction.do?module=login&rand=sjrand")

  # 获取loginRand, 该值是随后的模拟登陆post的一个必要参数, 由服务器返回, 每次都不相同
  url = "https://dynamic.12306.cn/otsweb/loginAction.do?method=loginAysnSuggest"
  referer = "https://dynamic.12306.cn/otsweb/loginAction.do?method=init#"
  resp = sendPostRequest(url,{},referer)
  try:
    respInfo = resp.read() # {"loginRand":"752","randError":"Y"}
  except:
    print(u"login()->sendPostRequest(%s)->resp.read() exception"%(url))
    return 0
  try:
    respDict = eval(respInfo)
  except:
    print(u"login()->eval(respInfo) exception")
    return 0
  loginRand = ''
  if respDict.has_key("loginRand"):
    loginRand = respDict['loginRand']
  else:
    print u"请求 loginRand 失败"
    return 0

  # 模拟登陆
  url = "https://dynamic.12306.cn/otsweb/loginAction.do?method=login"
  referer = "https://dynamic.12306.cn/otsweb/loginAction.do?method=init"
  # 参数顺序可能导致登陆失败
  params = [
    {'loginRand'       :loginRand},
    {'refundLogin'       :"N"},
    {'refundFlag'      :"Y"},
    {'isClick'      :""},
    {'from_tk'      :"null"},
    {'loginUser.user_name'   :username},
    {'nameErrorFocus'     :""},
    {'user.password'     :password},
    {'passwordErrorFocus'   :""},
    {'randCode'        :captcha},
    {'randErrorFocus'     :""},
    {'NDE1MzYzNQ=='    :"NzkxOGIzOWI3NmVjYWFmOA=="},
    {'myversion'     :"undefined"},
  ]
  postData = ""
  for param in params:
    postData += "&" + urllib.urlencode(param)
  postData = postData[1:]

  resp = sendPostRequest(url,postData,referer)
  try:
    respInfo = resp.read()
  except:
    print(u"login()->sendPostRequest(%s)->resp.read() exception"%(url))
    return 0

  # 判断登陆是否成功
  return checkLoginResult(respInfo)

#------------------------------------------------------------------------------
# Pares trains detail information and left tickets information
'''内容如下
0,<span id='id_65000K905207' class='base_txtdiv' onmouseover=javascript:onStopHover('65000K905207#BJQ#EHQ') onmouseout='onStopOut()'>K9052</span>,<img src='/otsweb/images/tips/first.gif'>&nbsp;&nbsp;&nbsp;&nbsp;深圳东&nbsp;&nbsp;&nbsp;&nbsp;<br>&nbsp;&nbsp;&nbsp;&nbsp;14:52,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;新化&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>&nbsp;&nbsp;&nbsp;&nbsp;03:19,12:27,--,--,--,--,--,4,<font color='darkgray'>无</font>,--,<font color='#008800'>有</font>,<font color='#008800'>有</font>,--,<a name='btn130_2' class='btn130_2' style='text-decoration:none;' onclick=javascript:getSelected('K9052#12:27#14:52#65000K905207#BJQ#EHQ#03:19#深圳东#新化#01#11#1*****32544*****00041*****03343*****0000#MDZERjM0NzY4Qjk2ODIzQTkwNkVFRDREMDVGMUM4Rjc2MDQ1MkJBMTdBNzA0MTVGMDA1MTAyMDM6Ojo6MTM4MzMxNTU4ODcwNw==#Q6')>预&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;订</a>\n
1,<span id='id_69000K906007' class='base_txtdiv' onmouseover=javascript:onStopHover('69000K906007#OSQ#EHQ') onmouseout='onStopOut()'>K9060</span>,<img src='/otsweb/images/tips/first.gif'>&nbsp;&nbsp;&nbsp;&nbsp;深圳西&nbsp;&nbsp;&nbsp;&nbsp;<br>&nbsp;&nbsp;&nbsp;&nbsp;19:08,&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;新化&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>&nbsp;&nbsp;&nbsp;&nbsp;08:30,13:22,--,--,--,--,--,--,<font color='#008800'>有</font>,--,<font color='#008800'>有</font>,<font color='#008800'>有</font>,--,<a name='btn130_2' class='btn130_2' style='text-decoration:none;' onclick=javascript:getSelected('K9060#13:22#19:08#69000K906007#OSQ#EHQ#08:30#深圳西#新化#01#13#1*****36801*****10883*****0157#QkJGREVBRjY0NDQ2OTdFQTdGOUMzN0NBMzU3QUE0NTU0MzA1QTQwMTA4NjNDMjcyMDEzQkRDMDY6Ojo6MTM4MzMxNTU4ODcwNw==#Q7')>预&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;订</a>
'''
def getTrainsDetailInfo(h):
  h = h.replace("&nbsp;","") # 删除&nbsp;
  h = h.decode("utf-8","ignore") # 使用decode("gb2312","ignore")会乱码, 因为网页内容是 utf-8 编码的
  all_trains = h.split(",<span")
  all_trains = all_trains[1:]
  trains = []
  cols = [u"车次",u"发站",u"到站",u"历时",u"商务座",u"特等座",u"一等座",u"二等座",u"高级软卧",u"软卧",u"硬卧",u"软座",u"硬座",u"无座",u"其它",u"购票"]
  for train in all_trains:
    c = train.split(",")
    s = c[0].find(">")
    e = c[0].find("<")
    c[0] = c[0][s+1:e] # 车次[id='id_65000K905206' class='base_txtdiv' onmouseover=javascript:onStopHover('65000K905206#BJQ#EHQ') onmouseout='onStopOut()'>K9052</span>]
    key = "<img src='/otsweb/images/tips/first.gif'>"
    s = c[1].find(key)
    s = 0 if s == -1 else  s + len(key)
    e = c[1].find("<br>")
    c[1] = c[1][s:e] + c[1][-5:] # 发站[<img src='/otsweb/images/tips/first.gif'>深圳东<br>14:52 或 #深圳东<br>14:52]
    key = "<img src='/otsweb/images/tips/last.gif'>"
    s = c[2].find(key)
    s = 0 if s == -1 else  s + len(key)
    e = c[2].find("<br>")
    c[2] = c[2][s:e] + c[2][-5:] # 到站[<img src='/otsweb/images/tips/last.gif'>怀化<br>03:19 或 #新化<br>03:19]
    c[3] = c[3] # 历时[12:27]
    for i in xrange(4,15):
      s = c[i].find(">")
      e = c[i].find("</font>")
      if s == -1:
        s = 0
        e = len(c[i])
      else:
        s += 1
      c[i] = c[i][s:e]
    d = dict(zip(cols, c))
    if c[15].find("btn130_2") != -1: # btn130_2 表示预定按钮可以点击, btn130 表示预订按钮灰显
      d[u"预订"] = 1
    else:
      d[u"预订"] = 0
    trains.append(d)
  return trains

#------------------------------------------------------------------------------
# Print trains
def printTrains(trains,cfg):
  printDelimiter()
  print u"%s\t%s--->%s  '有':票源充足  '无':票已售完  '*':未到起售时间  '--':无此席别"%(cfg.train_date,cfg.from_city_name,cfg.to_city_name)
  printDelimiter()
  print u"序号/车次\t发站\t\t到站\t\t一等座\t二等座\t软卧\t硬卧\t软座\t硬座\t无座"
  printDelimiter()
  index = 1
  for t in trains:
    print u"(%d)   %s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"%(index,t[u"车次"],t[u"发站"],t[u"到站"],t[u"一等座"],t[u"二等座"],t[u"软卧"],t[u"硬卧"],t[u"软座"],t[u"硬座"],t[u"无座"])
    index += 1
  printDelimiter()

#------------------------------------------------------------------------------
# Query tickets
def queryTickets(cfg):
  # 查询初始化可以省略
  #url = "https://dynamic.12306.cn/otsweb/order/querySingleAction.do?method=init"
  #referer = "https://dynamic.12306.cn/otsweb/"
  #resp = sendGetRequest(url,referer)

  #https://dynamic.12306.cn/otsweb/order/querySingleAction.do?method=queryLeftTicket&orderRequest.train_date=2013-11-15&orderRequest.from_station_telecode=SZQ&orderRequest.to_station_telecode=EHQ&orderRequest.train_no=&trainPassType=QB&trainClass=QB%23D%23Z%23T%23K%23QT%23&includeStudent=00&seatTypeAndNum=&orderRequest.start_time_str=00%3A00--24%3A00
  url = "https://dynamic.12306.cn/otsweb/order/querySingleAction.do?method=queryLeftTicket"
  referer = "https://dynamic.12306.cn/otsweb/order/querySingleAction.do?method=init"
  # 参数顺序也可能导致查询失败
  params = [
    {'orderRequest.train_date'       :cfg.train_date},
    {'orderRequest.from_station_telecode':cfg.from_station_telecode},
    {'orderRequest.to_station_telecode'  :cfg.to_station_telecode},
    {'orderRequest.train_no'       :""},
    {'trainPassType'           :"QB"},
    {'trainClass'            :"QB#D#Z#T#K#QT#"},
    {'includeStudent'          :"00"},
    {'seatTypeAndNum'          :""},
    {'orderRequest.start_time_str'     :"00:00--24:00"}
  ]
  for param in params:
    url += "&" + urllib.urlencode(param)
  resp = sendGetRequest(url,referer)
  try:
    respInfo = resp.read()
  except:
    print(u"queryTickets()->sendGetRequest(%s)->resp.read() exception"%(url))
    return []

  # 各车次余票详情
  trains = getTrainsDetailInfo(respInfo)
  printTrains(trains,cfg)
  return trains

#------------------------------------------------------------------------------
# Select train
def selectTrain(trains):
  trains_num = len(trains)
  index = 0
  while 1: # 必须选择有效的车次
    index = raw_input("")
    if not index.isdigit():
      print u"只能输入数字序号,请重新选择车次(1~%d)"%(trains_num)
      continue
    index = int(index)
    if index<1 or index>trains_num:
      print u"输入的序号无效,请重新选择车次(1~%d)"%(trains_num)
      continue
    if not trains[index-1][u"预订"]:
      print u"您选择的车次%s没票啦,请重新选择车次"%(trains[index-1][u"车次"])
      continue
    else:
      break

  return index

#------------------------------------------------------------------------------
# Select Actions
# -1->重新查询/0->退出程序/1~len->车次序号
def selectAction(trains,cfg):
  ret = -1
  trains_num = len(trains)
  print u"您可以选择:\n1~%d.选择车次开始订票\nd.更改乘车日期\nf.更改出发站\nt.更改目的站\ns.同时更改出发站和目的站\na.同时更改乘车日期,出发站和目的站\nq.退出\n刷新车票请直接回车"%(trains_num)
  printDelimiter()
  select = raw_input("")
  if select.isdigit():
    index = int(select)
    if index<1 or index>trains_num:
      print u"输入的序号无效,请重新选择车次(1~%d)"%(trains_num)
      index = selectTrain(trains)
    if not trains[index-1][u"预订"]:
      print u"您选择的车次%s没票啦,请重新选择车次"%(trains[index-1][u"车次"])
      index = selectTrain(trains)
    ret = index
  elif select == "d" or select == "D":
    print u"请输入乘车日期:"
    cfg.train_date = inputDate()
  elif select == "f" or select == "F":
    print u"请输入出发站:"
    station = inputStation()
    cfg.from_city_name = station['name']
    cfg.from_station_telecode = station['telecode'] # 车站编码, 例如深圳对应的编码是SZQ
  elif select == "t" or select == "T":
    print u"请输入目的站:"
    station = inputStation()
    cfg.to_city_name = station['name']
    cfg.to_station_telecode = station['telecode']
  elif select == "s" or select == "S":
    print u"请输入出发站:"
    station = inputStation()
    cfg.from_city_name = station['name']
    cfg.from_station_telecode = station['telecode']
    print u"请输入目的站:"
    station = inputStation()
    cfg.to_city_name = station['name']
    cfg.to_station_telecode = station['telecode']
  elif select == "a" or select == "A":
    print u"请输入乘车日期:"
    cfg.train_date = inputDate()
    print u"请输入出发站:"
    station = inputStation()
    cfg.from_city_name = station['name']
    cfg.from_station_telecode = station['telecode']
    print u"请输入目的站:"
    station = inputStation()
    cfg.to_city_name = station['name']
    cfg.to_station_telecode = station['telecode']
  elif select == "q" or select == "Q":
    ret = 0

  return ret

def parseOnClick(train,cfg):
  soup = BeautifulSoup(train[u"购票"])
  tag_a = soup.find("a", class_=["btn130_2", "btn130"])
  onclick = tag_a['onclick']
  itemList = onclick.split('#')
  station_train_code = itemList[0][len("javascript:getSelected('"):] # 车次[K9060]
  lishi = itemList[1] # 历时[13:22]
  train_start_time = itemList[2] # 发出时间[19:08]
  trainno4 = itemList[3] # 车次编码[69000K906007]
  from_station_telecode = itemList[4] # 出发站编码[OSQ]
  to_station_telecode = itemList[5] # 目的站编码[EHQ]
  arrive_time = itemList[6] # 到达时间[08:30]
  from_station_name = itemList[7] # 出发站名称[深圳西]
  to_station_name = itemList[8] # 目的站名称[新化]
  from_station_no = itemList[9] # 出发站是第几站[01]
  to_station_no = itemList[10] # 目的站是第几站[3]
  ypInfoDetail = itemList[11] # 余票详情[1*****36601*****08953*****0000]
  mmStr = itemList[12] # 6D10DCDFCFD7BFC946029BADC0C7DFD166BD121BC8972AC7B931556A
  locationCode = itemList[13][:-len("')")] # Q6
  postDict = {
    'station_train_code'    :station_train_code,
    'train_date'        :cfg.train_date, # 乘车日期 ["2013-01-10",]
    'seattype_num'        :"", # 隐含选项, 使用默认值""即可
    'from_station_telecode'   :from_station_telecode,
    'to_station_telecode'     :to_station_telecode,
    'include_student'       :"00", # 隐含选项, 乘客中包含学生, 使用默认值00即可
    'from_station_telecode_name':cfg.from_city_name, # 对应查询界面'出发地'输入框中的内容[u"深圳"]
    'to_station_telecode_name'  :cfg.to_city_name, # 对应查询界面'目的地'输入框中的内容[u"新化"]
    'round_train_date'      :cfg.train_date, # "2013-01-10",
    'round_start_time_str'    :"00:00--24:00", # 发出时间段, 不用修改
    'single_round_type'     :"1",
    'train_pass_type'       :"QB", # [GL->过路][SF->始发][QB->全部]
    'train_class_arr'       :"QB#D#Z#T#K#QT#", # [QB->全部][D->动车][Z->Z字头][T->T字头][K->K字头][QT其它]
    'start_time_str'      :"00:00--24:00", # 发出时间段,不用修改
    'lishi'           :lishi,
    'train_start_time'      :train_start_time,
    'trainno4'          :trainno4,
    'arrive_time'         :arrive_time,
    'from_station_name'     :from_station_name,
    'to_station_name'       :to_station_name,
    'from_station_no'       :from_station_no,
    'to_station_no'       :to_station_no,
    'ypInfoDetail'        :ypInfoDetail,
    'mmStr'           :mmStr,
    'locationCode'        :locationCode
  }

  return postDict

#------------------------------------------------------------------------------
# Order Init
def orderInit(onClickDict):
  url = "https://dynamic.12306.cn/otsweb/order/querySingleAction.do?method=submutOrderRequest"
  referer = "https://dynamic.12306.cn/otsweb/order/querySingleAction.do?method=init"
  postData = urllib.urlencode(onClickDict)
  resp = sendPostRequest(url,postData,referer) # 服务器会返回302, 重定向到 https://dynamic.12306.cn/otsweb/order/confirmPassengerAction.do?method=init
  respInfo = None
  try:
    respInfo = resp.read()
  except:
    print(u"orderInit()->sendPostRequest(%s)->resp.read() exception"%(url))
  #logging.debug('orderInit submutOrderRequest respInfo:%s'%(respInfo))
  if not respInfo:
    url = "https://dynamic.12306.cn/otsweb/order/confirmPassengerAction.do?method=init"
    resp = sendPostRequest(url,postData,referer)
    try:
      respInfo = resp.read()
    except:
      print(u"orderInit()->sendPostRequest(%s)->resp.read() exception"%(url))
    #logging.debug('orderInit init respInfo:%s'%(respInfo))
  return respInfo

#------------------------------------------------------------------------------
# Get hidden item
def getHiddenItem(respInfo):
  if not respInfo:
    return 0
  soup = BeautifulSoup(respInfo)
  tag = soup.find(attrs={"name": "org.apache.struts.taglib.html.TOKEN", "type":"hidden"})
  if not tag:
    return 0
  token = tag['value']
  tag = soup.find(attrs={"name":"leftTicketStr", "type":"hidden", "id":"left_ticket"})
  if not tag:
    return 0
  leftTicketStr = tag['value']
  tag = soup.find(attrs={"name":"textfield", "type":"text", "id":"passenger_filter_input"})
  if not tag:
    return 0
  textfield = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.train_date", "type":"hidden", "id":"start_date"})
  if not tag:
    return 0
  train_date = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.train_no", "type":"hidden", "id":"train_no"})
  if not tag:
    return 0
  train_no = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.station_train_code", "type":"hidden", "id":"station_train_code"})
  if not tag:
    return 0
  station_train_code = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.from_station_telecode", "type":"hidden", "id":"from_station_telecode"})
  if not tag:
    return 0
  from_station_telecode = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.to_station_telecode", "type":"hidden", "id":"to_station_telecode"})
  if not tag:
    return 0
  to_station_telecode = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.seat_type_code", "type":"hidden", "id":"seat_type_code"})
  if not tag:
    return 0
  seat_type_code = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.ticket_type_order_num", "type":"hidden", "id":"ticket_type_order_num"})
  if not tag:
    return 0
  ticket_type_order_num = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.bed_level_order_num", "type":"hidden", "id":"bed_level_order_num"})
  if not tag:
    return 0
  bed_level_order_num = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.start_time", "type":"hidden", "id":"orderRequest_start_time"})
  if not tag:
    return 0
  start_time = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.end_time", "type":"hidden", "id":"orderRequest_end_time"})
  if not tag:
    return 0
  end_time = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.from_station_name", "type":"hidden", "id":"orderRequest_from_station_name"})
  if not tag:
    return 0
  from_station_name = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.to_station_name", "type":"hidden", "id":"orderRequest_to_station_name"})
  if not tag:
    return 0
  to_station_name = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.cancel_flag", "type":"hidden", "id":"cancel_flag"})
  if not tag:
    return 0
  cancel_flag = tag['value']
  tag = soup.find(attrs={"name":"orderRequest.id_mode", "type":"hidden", "id":"orderRequest_id_mode"})
  if not tag:
    return 0
  id_mode = tag['value']

  # 通用的POST数据, 来自于之前init的响应数据
  hiddenDict = {
    'org.apache.struts.taglib.html.TOKEN'   :token,
    'leftTicketStr'           :leftTicketStr,
    'textfield'             :textfield,
    'checkbox2'             :"2",
    'checkbox3'             :"3",
    'checkbox4'             :"4",
    'checkbox5'             :"5",
    'checkbox6'             :"6",
    'orderRequest.train_date'       :train_date,
    'orderRequest.train_no'       :train_no,
    'orderRequest.station_train_code'   :station_train_code,
    'orderRequest.from_station_telecode':from_station_telecode,
    'orderRequest.to_station_telecode'  :to_station_telecode,
    'orderRequest.seat_type_code'     :seat_type_code,
    'orderRequest.ticket_type_order_num':ticket_type_order_num,
    'orderRequest.bed_level_order_num'  :bed_level_order_num,
    'orderRequest.start_time'       :start_time,
    'orderRequest.end_time'       :end_time,
    'orderRequest.from_station_name'  :from_station_name,
    'orderRequest.to_station_name'    :to_station_name,
    'orderRequest.cancel_flag'      :cancel_flag,
    'orderRequest.id_mode'        :id_mode,
  }
  hiddenList = [
    ('org.apache.struts.taglib.html.TOKEN'   ,token),
    ('leftTicketStr'           ,leftTicketStr),
    ('textfield'             ,textfield),
    ('checkbox2'             ,"2"),
    ('checkbox3'             ,"3"),
    ('checkbox4'             ,"4"),
    ('checkbox5'             ,"5"),
    ('checkbox6'             ,"6"),
    ('orderRequest.train_date'       ,train_date),
    ('orderRequest.train_no'       ,train_no),
    ('orderRequest.station_train_code'   ,station_train_code),
    ('orderRequest.from_station_telecode',from_station_telecode),
    ('orderRequest.to_station_telecode'  ,to_station_telecode),
    ('orderRequest.seat_type_code'     ,seat_type_code),
    ('orderRequest.ticket_type_order_num',ticket_type_order_num),
    ('orderRequest.bed_level_order_num'  ,bed_level_order_num),
    ('orderRequest.start_time'       ,start_time),
    ('orderRequest.end_time'       ,end_time),
    ('orderRequest.from_station_name'  ,from_station_name),
    ('orderRequest.to_station_name'    ,to_station_name),
    ('orderRequest.cancel_flag'      ,cancel_flag),
    ('orderRequest.id_mode'        ,id_mode)
  ]
  return (hiddenDict,hiddenList)

#------------------------------------------------------------------------------
# Generate common data
def genCommonData(hiddenDict,cfg,captcha):
  # 乘客信息
  passenger_seat_detail = "0" # [0->随机][1->下铺][2->中铺][3->上铺]
  all_passengers = [
    {
      'passengerTickets'          :"%s,%s,%s,%s,%s,%s,%s,%s"%(p['seattype'],passenger_seat_detail,p['tickettype'],p['name'],p['cardtype'],p['id'],p['phone'],"Y"),#"席别,随机,票种,姓名,证件类型,证件号码,手机号码,保存到常用联系人"
      'oldPassengers'           :"%s,%s,%s"%(p['name'],p['cardtype'],p['id']), # "姓名,证件类型,身证件号码"
      'passenger_%d_seat'%(p['index'])      :p['seattype'], # [1->硬座][3->硬卧]
      'passenger_%d_ticket'%(p['index'])    :p['tickettype'], # [1->成人票][2->儿童票][3->学生票][4->残军票]
      'passenger_%d_name'%(p['index'])      :p['name'], # 乘客姓名
      'passenger_%d_cardtype'%(p['index'])    :p['cardtype'], # 证件类型: [1->二代身份证][2->一代身份证][C->港澳通行证][G->台湾通行证][B->护照]
      'passenger_%d_cardno'%(p['index'])    :p['id'], # 证件号码
      'passenger_%d_mobileno'%(p['index'])    :p['phone'], # 手机号码
      'checkbox9'             :"Y" # 保存到常用联系人
    }
    for p in cfg.passengers
  ]
  commonPostData = urllib.urlencode(hiddenDict)
  for p in all_passengers:
    commonPostData = commonPostData + '&' + urllib.urlencode(p)

  d = {
    'randCode'              :captcha,
    'orderRequest.reserve_flag'     :"A" # A网上支付, B网上预订, 默认选择A
  }
  commonPostData = commonPostData + '&' + urllib.urlencode(d)

  return commonPostData

#------------------------------------------------------------------------------
# Generate common data
def genCommonDataOneByOne(hiddenDict,cfg,captcha):
  #乘客信息
  passenger_seat_detail = "0" # [0->随机][1->下铺][2->中铺][3->上铺]
  all_passengers = [
    [
      ('passengerTickets'          ,"%s,%s,%s,%s,%s,%s,%s,%s"%(p['seattype'],passenger_seat_detail,p['tickettype'],p['name'],p['cardtype'],p['id'],p['phone'],"Y")),#"席别,随机,票种,姓名,证件类型,证件号码,手机号码,保存到常用联系人"
      ('oldPassengers'           ,"%s,%s,%s"%(p['name'],p['cardtype'],p['id'])), # "姓名,证件类型,身证件号码"
      ('passenger_%d_seat'%(p['index'])      ,p['seattype']), # [1->硬座][3->硬卧]
      ('passenger_%d_ticket'%(p['index'])    ,p['tickettype']), # [1->成人票][2->儿童票][3->学生票][4->残军票]
      ('passenger_%d_name'%(p['index'])      ,p['name']), # 乘客姓名
      ('passenger_%d_cardtype'%(p['index'])    ,p['cardtype']), # 证件类型: [1->二代身份证][2->一代身份证][C->港澳通行证][G->台湾通行证][B->护照]
      ('passenger_%d_cardno'%(p['index'])    ,p['id']), # 证件号码
      ('passenger_%d_mobileno'%(p['index'])    ,p['phone']), # 手机号码
      ('checkbox9'             ,"Y") # 保存到常用联系人
    ]
    for p in cfg.passengers
  ]
  commonPostData = urllib.urlencode(hiddenDict)
  for p in all_passengers:
    commonPostData = commonPostData + '&' + urllib.urlencode(p)

  d = [
    ('randCode'              ,captcha),
    ('orderRequest.reserve_flag'     ,"A") # A网上支付, B网上预订, 默认选择A
  ]
  commonPostData = commonPostData + '&' + urllib.urlencode(d)

  return commonPostData

#------------------------------------------------------------------------------
# Check order info
# 1->OK/0->Fail/-1->errMsg
def checkOrderInfo(commonPostData,captcha):
  url = "https://dynamic.12306.cn/otsweb/order/confirmPassengerAction.do?method=checkOrderInfo&rand=" + captcha
  tFlagDict = {'tFlag':"dc"} # [dc->单程][wc->往程][fc->返程][gc->改签]
  postData = commonPostData + '&' + urllib.urlencode(tFlagDict)
  resp = sendPostRequest(url,postData)
  respInfo = None
  try:
    respInfo = resp.read()
  except:
    print(u"checkOrderInfo()->sendPostRequest(%s)->resp.read() exception"%(url))
    return 0
  #{"checkHuimd":"Y","check608":"Y","msg":"","errMsg":"Y"}
  #参数解释参考https://dynamic.12306.cn/otsweb/js/order/save_passenger_info.js?version=5.37
  #checkHuimd":"N"#"对不起，由于您取消次数过多，今日将不能继续受理您的订票请求！"
  #"check608":"N"#"本车为实名制列车，实行一日一车一证一票制！"
  logging.debug('checkOrderInfo respInfo:%s'%(respInfo))
  respDict = {}
  try:
    respDict = eval(respInfo)
  except:
    print(u"checkOrderInfo(%s)->eval(respInfo) exception"%(url))
    return 0
  if respDict.has_key("errMsg"):
    if respDict['errMsg'] != "Y":
      print u'检查订单信息,服务器返回错误errMsg:%s'%(respDict['errMsg'])
      return -1
  elif respDict.has_key("msg"):
    if respDict['msg'] != "":
      print u'检查订单信息,服务器返回错误msg:%s'%(respDict['msg'])
      return 0
  elif respDict.has_key("checkHuimd"):
    if respDict['checkHuimd'] != "Y":
      print u'检查订单信息,服务器返回错误checkHuimd:%s'%(respDict['checkHuimd'])
      return 0
  elif respDict.has_key("check608"):
    if respDict['check608'] != "Y":
      print u'检查订单信息,服务器返回错误check608:%s'%(respDict['check608'])
      return 0
  return 1

#------------------------------------------------------------------------------
# Get queue count
# 1->OK/0->Fail/-1->errMsg
def getQueueCount(hiddenDict):
  #https://dynamic.12306.cn/otsweb/order/confirmPassengerAction.do?method=getQueueCount&train_date=2013-11-15&train_no=69000K906007&station=K9060&seat=3&from=OSQ&to=EHQ&ticket=100985368010098510883021350157
  url = "https://dynamic.12306.cn/otsweb/order/confirmPassengerAction.do?method=getQueueCount&"
  parameters = [
    ('train_date',hiddenDict['orderRequest.train_date']),
    ('train_no'  ,hiddenDict['orderRequest.train_no']),
    ('station'   ,hiddenDict['orderRequest.station_train_code']),
    ('seat'    ,"1" if not hiddenDict['orderRequest.seat_type_code'] else hiddenDict['orderRequest.seat_type_code']),
    ('from'    ,hiddenDict['orderRequest.from_station_telecode']),
    ('to'    ,hiddenDict['orderRequest.to_station_telecode']),
    ('ticket'  ,hiddenDict['leftTicketStr'])
  ]
  url += urllib.urlencode(parameters)
  resp = sendGetRequest(url)
  try:
    respInfo = resp.read()
  except:
    print(u"getQueueCount()->sendGetRequest(%s)->resp.read() exception"%(url))
    return 0
  #{"countT":0,"count":1,"ticket":"1*****36601*****09683*****0067","op_1":false,"op_2":false}
  #参数解释参考#https://dynamic.12306.cn/otsweb/js/order/save_passenger_info.js?version=5.37
  #"countT":0#目前排队人数
  #"count":1#在你之前的排队人数
  #"ticket":"1*****36601*****09683*****0067"#其中36601代表无座有660张, 09683代码座位票有968张,0067代表卧铺票有67张,纯属推测
  #"op_1":true#"目前排队人数已经超过余票张数，特此提醒。"
  #"op_2":true#"目前排队人数已经超过余票张数，请您选择其他席别或车次，特此提醒。"
  logging.debug('getQueueCount respInfo:%s'%(respInfo))
  return 1

#------------------------------------------------------------------------------
# Confirm single for queue
# 1->OK/0->Fail/-1->errMsg
def confirmSingleForQueue(commonPostData):
  url = "https://dynamic.12306.cn/otsweb/order/confirmPassengerAction.do?method=confirmSingleForQueue"
  resp = sendPostRequest(url,commonPostData)
  try:
    respInfo = resp.read()#{"errMsg":"Y"}
  except:
    print(u"confirmSingleForQueue()->sendPostRequest(%s)->resp.read() exception"%(url))
    return 0
  logging.debug('confirmSingleForQueue respInfo:%s'%(respInfo))
  try:
    respDict = eval(respInfo)
  except:
    print(u"confirmSingleForQueue(%s)->eval(respInfo) exception"%(url))
    return 0
  if respDict.has_key("errMsg"):
    if respDict['errMsg'] != "Y":
      print u'订单入队,服务器返回错误:%s'%(respDict['errMsg'])
      return -1
  return 1

#------------------------------------------------------------------------------
# Query order wait time and return orderId
def queryOrderWaitTime():
  url = "https://dynamic.12306.cn/otsweb/order/myOrderAction.do?method=queryOrderWaitTime&tourFlag=dc"
  resp = sendGetRequest(url)
  orderId = ''
  try:
    respInfo = resp.read()
  except:
    print(u"queryOrderWaitTime()->sendGetRequest(%s)->resp.read() exception"%(url))
  #{"tourFlag":"dc","waitTime":5,"waitCount":1,"requestId":5691791102757848251,"count":0}
  #参数解释参考https://dynamic.12306.cn/otsweb/js/order/save_passenger_info.js?version=5.37
  #"tourFlag":"dc"#单程
  #"waitTime":5#排队等待时间
  #"waitCount":1#排队人数
  #"requestId":5691791102757848251#
  #获取orderId
  try:
    respDict = eval(respInfo)
  except:
    print(u"queryOrderWaitTime(%s)->eval(respInfo) exception"%(url))
    respDict = {}
  if respDict.has_key("orderId"):
    orderId = respDict["orderId"]

  # 如果上一次没有返回 orderId, 则再次重复一遍
  if orderId == '':
    resp = sendGetRequest(url)
    try:
      respInfo = resp.read()
    except:
      print(u"queryOrderWaitTime()->sendGetRequest(%s)->resp.read() exception"%(url))
    # 获取 orderId
    try:
      respDict = eval(respInfo)
    except:
      print(u"queryOrderWaitTime(%s)->eval(respInfo) exception"%(url))
      respDict = {}
    orderId = ''
    if respDict.has_key("orderId"):
      orderId = respDict["orderId"]
  logging.debug('queryOrderWaitTime respInfo:%s'%(respInfo))
  return orderId

class Config:
  username = '' # 账号
  password = '' # 密码
  train_date = '' # 乘车日期[2013-09-09]
  from_city_name = '' # 对应查询界面'出发地'输入框中的内容[u'深圳']
  to_city_name = '' # 对应查询界面'目的地'输入框中的内容[u'新化']
  from_station_telecode = '' # 出发站编码, 例如深圳对应的编码是 SZQ
  to_station_telecode = '' # 目的站编码, 例如新化对应的编码是 EHQ
  passengers = [] # 乘客列表
  def readConfig(self,config_file='config.ini'):
    # 从配置文件读取订票信息
    cp = ConfigParser.ConfigParser()
    try:
      cp.readfp(codecs.open(config_file, 'r','utf-8-sig'))
    except IOError as e:
      print u"打开配置文件'%s'失败啦!"%(config_file)
      return
    Config.username = cp.get("login","username")
    Config.password = cp.get("login","password")
    Config.train_date = cp.get("train","date");
    Config.from_city_name = cp.get("train","from")
    Config.to_city_name = cp.get("train","to")
    Config.from_station_telecode = stationName2Telecode(Config.from_city_name)
    Config.to_station_telecode = stationName2Telecode(Config.to_city_name)
    # 检查出发站, 目的站和乘车日期
    if not Config.from_station_telecode:
      print u"出发站错误,请重新输入:"
      station = inputStation()
      Config.from_city_name = station['name']
      Config.from_station_telecode = station['telecode']
    if not Config.to_station_telecode:
      print u"目的站错误,请重新输入:"
      station = inputStation()
      Config.to_city_name = station['name']
      Config.to_station_telecode = station['telecode']
    if not checkDate(Config.train_date):
      print u"乘车日期错误,请重新输入:"
      Config.train_date = inputDate()
    # 分析乘客信息
    Config.passengers = []
    index = 1
    passenger_sections = ["passenger%d"%(i) for i in xrange(1,6)]
    sections = cp.sections()
    for section in passenger_sections:
      if section in sections:
        passenger = {}
        passenger['index'] = index
        passenger['name'] = cp.get(section,"name") # 必选参数
        passenger['cardtype'] = cp.get(section,"cardtype") if cp.has_option(section,"cardtype") else "1" # 证件类型:可选参数,默认值1,即二代身份证
        passenger['id'] = cp.get(section,"id") # 必选参数
        passenger['phone'] = cp.get(section,"phone") if cp.has_option(section,"phone") else "13751119427" # 手机号码
        passenger['seattype'] = cp.get(section,"seattype") if cp.has_option(section,"seattype") else "1" # 席别:可选参数, 默认值1, 即硬座
        passenger['tickettype'] = cp.get(section,"tickettype") if cp.has_option(section,"tickettype") else "1" #票种:可选参数, 默认值1, 即成人票
        Config.passengers.append(passenger)
        index += 1
  def setTrainDate(self, date):
    Config.train_date = date
  def printConfig(self):
    printDelimiter()
    print u"订票信息:"
    print u"%s\t%s\t%s--->%s"%(Config.username,Config.train_date,Config.from_city_name,Config.to_city_name)
    printDelimiter()
    print u"序号 姓名\t证件类型\t证件号码\t\t手机号码\t席别\t票种\t"
    for p in Config.passengers:
      print u"%d  %s\t%s\t%s\t%s\t%s\t%s"%(p['index'],p['name'].decode("utf-8","ignore"),getCardType(p['cardtype']),p['id'],p['phone'],getSeatType(p['seattype']),getTicketType(p['tickettype']))#使用decode("gb2312","ignore")会乱码,因为文件是保存为 utf-8 编码的

#------------------------------------------------------------------------------
# Main function
def Main12306():
  logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(filename)s %(funcName)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %X',
            filename='log.txt',
            filemode='w')
  logging.debug('Start')

  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--config', help='Specify config file, default is config.ini')
  parser.add_argument('-d', '--date', help='Specify train date, 2013-09-09')
  args = parser.parse_args()

  stationInit()

  cfg = Config()
  if args.config:
    cfg.readConfig(args.config)
  else:
    cfg.readConfig()
  if args.date:
    if checkDate(args.date):
      cfg.setTrainDate(args.date)
    else:
      print u"乘车日期错误,请重新输入:"
      cfg.setTrainDate(inputDate())
  cfg.printConfig()

  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  opener.addheaders = [('Accept',	'text/html'),
             ('Referer', 'https://dynamic.12306.cn/otsweb/'),
             ('Accept-Language', 'zh-CN'),
             ('User-Agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; MALC'),
             ('Accept-Encoding', 'deflate'),
             ('Host', "dynamic.12306.cn"),
             ('Connection', 'Keep-Alive'),
            ]
  urllib2.install_opener(opener)

  max_tries = 3
  tries = 0

  while tries < max_tries:
    tries += 1
    printDelimiter()
    if login(cfg.username,cfg.password):
      print u"登陆成功^_^"
      break
    else:
      print u"登陆失败啦!重新登陆..."
  else:
    print u"失败次数太多,自动退出程序"
    sys.exit()

  while 1:
    trains = queryTickets(cfg)
    ret = selectAction(trains,cfg)
    if ret == -1:
      continue
    elif ret == 0:
      sys.exit()
    index = ret
    onClickDict = parseOnClick(trains[index-1],cfg)
    respInfo = orderInit(onClickDict)
    ret = getHiddenItem(respInfo)
    if not ret:
      print(u"getHiddenItem() failed")
      continue
    hiddenDict = ret[0]
    hiddenList = ret[1]
    # 请求图片验证码
    captcha = getCaptcha("https://dynamic.12306.cn/otsweb/passCodeNewAction.do?module=passenger&rand=randp")
    commonPostData = genCommonDataOneByOne(hiddenList,cfg,captcha)
    # 检查订单信息
    ret = checkOrderInfo(commonPostData,captcha)
    if ret == 0:
      continue
    elif ret == -1: # 验证码错误
      captcha = getCaptcha("https://dynamic.12306.cn/otsweb/passCodeNewAction.do?module=passenger&rand=randp"+"%1.16f"%(random.random()))
      commonPostData = genCommonDataOneByOne(hiddenList,cfg,captcha)
      ret = checkOrderInfo(commonPostData,captcha)
    # 查询排队和余票情况, 不能省略
    ret = getQueueCount(hiddenDict)
    # 提交订单到队里中
    ret = confirmSingleForQueue(commonPostData)
    # 获取队里等待时间, 服务器会返回 orderId, orderId 会作为随后的POST参数
    orderId = queryOrderWaitTime()
    # 正式提交订单
    url = "https://dynamic.12306.cn/otsweb/order/confirmPassengerAction.do?method=payOrder&orderSequence_no=" + orderId
    resp = sendPostRequest(url,commonPostData)
    try:
      respInfo = resp.read()
    except:
      print(u"Main12306()->sendPostRequest(%s)->resp.read() exception"%(url))
    if checkOrderResult(respInfo):
      print u"订票成功^_^请在45分钟内完成网上支付,否则系统将自动取消"
      break

    # 访问未完成订单页面检查是否订票成功
    url = "https://dynamic.12306.cn/otsweb/order/myOrderAction.do?method=queryMyOrderNotComplete&leftmenu=Y"
    resp = sendGetRequest(url)
    try:
      respInfo = resp.read()
    except:
      print(u"Main12306()->sendGetRequest(%s)->resp.read() exception"%(url))
    if checkOrderResult(respInfo):
      print u"订票成功^_^请在45分钟内完成订单,否则系统将自动取消"
      break
    else:
      print u"订票失败啦!请重试"

  raw_input("Press any key to continue")
  logging.debug('End')

if __name__=="__main__":
  Main12306()

# EOF