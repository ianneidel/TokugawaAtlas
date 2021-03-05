from random import seed
from random import random
import colorsys
import numpy as np
from PIL import Image
from PIL import ImageColor

alldomains =  ["麻田藩",
"和歌山藩",
"大多喜藩",
"忍藩",
"岩槻藩",
"川越藩",
"小諸藩",
"桑名藩",
"鳥羽藩",
"盛岡藩",
"山形藩",
"沼田藩",
"吉井藩",
"古河藩",
"佐倉藩",
"柳川藩",
"福江藩",
"熊本藩",
"小倉藩",
"中津藩",
"岡藩",
"柏原藩",
"府内藩",
"宇都宮藩",
"小浜藩",
"亀山藩",
"小田原藩",
"伊保藩",
"刈谷藩",
"会津藩",
"高崎藩",
"関宿藩",
"金沢藩",
"姫路藩",
"若桜藩",
"庭瀬藩",
"広島藩",
"臼杵藩",
"三田藩",
"福知山藩",
"久留里藩",
"高島藩",
"浜松藩",
"吉田藩",
"岡崎藩",
"膳所藩",
"仙台藩",
"米沢藩",
"前橋藩",
"伊勢崎藩",
"府中藩",
"土浦藩",
"牛久藩",
"足守藩",
"長府藩",
"杵築藩",
"日出藩",
"佐伯藩",
"大田原藩",
"壬生藩",
"松代藩",
"田原藩",
"彦根藩",
"平藩",
"大垣藩",
"松岡藩",
"福井藩",
"岡山藩",
"延岡藩",
"飯山藩",
"笠間藩",
"津山藩",
"今治藩",
"新発田藩",
"挙母藩",
"棚倉藩",
"麻生藩",
"出石藩",
"名古屋藩",
"津藩",
"加納藩",
"水戸藩",
"徳島藩",
"宇和島藩",
"茂木藩",
"沢海藩",
"川中島藩",
"狭山藩",
"飯田藩",
"大村藩",
"佐野藩",
"甲府藩",
"黒羽藩",
"村上藩",
"松本藩",
"西尾藩",
"萩藩",
"高槻藩",
"長沼藩",
"安中藩",
"小幡藩",
"郡山藩",
"柳本藩",
"谷田部藩",
"赤穂藩",
"岡田藩",
"尼崎藩",
"高田藩",
"須坂藩",
"館林藩",
"七日市藩",
"高遠藩",
"明石藩",
"林田藩",
"龍野藩",
"成羽藩",
"福岡藩",
"岸和田藩",
"長岡藩",
"園部藩",
"大溝藩",
"浜田藩",
"福山藩",
"久留米藩",
"佐賀藩",
"田辺藩",
"烏山藩",
"佐貫藩",
"峰山藩",
"三池藩",
"新庄藩",
"庄内藩",
"上山藩",
"宮津藩",
"大洲藩",
"勝山藩",
"淀藩",
"亀田藩",
"本荘藩",
"下館藩",
"新谷藩",
"大野藩",
"山家藩",
"三春藩",
"白河藩",
"生実藩",
"松江藩",
"田中藩",
"鹿児島藩",
"掛川藩",
"岩村藩",
"鳥取藩",
"綾部藩",
"与板藩",
"泉藩",
"神戸藩",
"小野藩",
"唐津藩",
"八幡藩",
"島原藩",
"村松藩",
"富山藩",
"大聖寺藩",
"皆川藩",
"高岡藩",
"高須藩",
"椎谷藩",
"丸亀藩",
"岩国藩",
"弘前藩",
"二本松藩",
"土佐藩",
"横須賀藩",
"新宮藩",
"宇土藩",
"松山藩",
"鹿沼藩",
"飯野藩",
"北条藩",
"岡部藩",
"一関藩",
"沼津藩",
"小見川藩",
"中村藩",
"八戸藩",
"久居藩",
"湯長谷藩",
"秋田藩",
"岡山新田藩",
"守山藩",
"福島藩",
"糸魚川藩",
"水口藩",
"鞠山藩",
"宮川藩",
"山上藩",
"小倉新田藩",
"小島藩",
"上田藩",
"谷村藩",
"多度津藩",
"三日月藩",
"新見藩",
"三上藩",
"篠山藩",
"館山藩",
"多古藩",
"桑折藩",
"喜連川藩",
"久喜藩",
"結城藩",
"岩村田藩",
"足利藩",
"長島藩",
"相良藩",
"下妻藩",
"安志藩",
"徳山藩",
"西条藩",
"黒川藩",
"三日市藩",
"八田藩",
"三草藩",
"西大平藩",
"森藩",
"高畠藩",
"蓮池藩",
"人吉藩",
"下手渡藩",
"黒石藩",
"下村藩",
"天童藩",
"一宮藩",
"秋月藩",
"鶴牧藩",
"奥殿藩",
"鯖江藩",
"請西藩",
"犬山藩",
"今尾藩",
"伯太藩",
"高知藩"]

correspondingcolors = []
seed(1)



def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(int(r*255+.5),int(g*255+.5),int(b*255+.5))

produceImages = False

codeFor = "Incumbent" #or "Incumbent" or "Both"

print("""var domrenderer = {
  type: "unique-value",  // autocasts as new UniqueValueRenderer()
  field: "Dump_Dom13",
  field2: "Dump_Dom_1",
  fieldDelimiter: ", ",
  defaultSymbol: {type: "picture-fill", url: "http://localhost:3000/blank.png", width: 5, height: 5},
  uniqueValueInfos: [""")
numdom = len(alldomains)
for i in range(numdom):
    hue = i/numdom*360
    satr = .5+random()/2
    val = .5+random()/2
    rgbtpl = colorsys.hsv_to_rgb(hue,satr,val)
    hexcode = rgb2hex(rgbtpl[0],rgbtpl[1],rgbtpl[2])
    hexnohash = hexcode.strip("#")
    correspondingcolors.append(hexcode)
    if codeFor == 'Both':
        print('    {value: "Regular, ' + str(alldomains[i]) + '", symbol: {type: "simple-fill", color: "' + hexcode + '"}},')
        print('    {value: "Newcomer, ' + str(alldomains[i]) + '", symbol: {type: "picture-fill", url: "http://localhost:3000/n'+hexnohash+'.png", outline: {style: "solid"}, width: 5, height: 5}},')
        print('    {value: "Incumbent, ' + str(alldomains[i]) + '", symbol: {type: "picture-fill", url: "http://localhost:3000/i' + hexnohash + '.png", outline: {style: "solid"}, width: 5, height: 5}}', end="")
    else:
        print('    {value: "Regular, ' + str(
            alldomains[i]) + '", symbol: {type: "simple-fill", color: "' + hexcode + '"}},')
        print('    {value: "' + codeFor + ', ' + str(
            alldomains[i]) + '", symbol: {type: "simple-fill", color: "' + hexcode + '"}}', end="")
    if i == numdom-1:
        print(']', end="")
    else:
        print(',')

    if produceImages:
        #produce inc and newc images:
        rgbval = ImageColor.getcolor(hexcode,"RGB")

        im = Image.open('newcomer.png')
        data = np.array(im)
        red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
        mask = (red == 255) & (green == 255) & (blue == 255)
        data[:, :, :3][mask] = [rgbval[0], rgbval[1], rgbval[2]]

        im = Image.fromarray(data)
        im.save('n{}.png'.format(hexcode.strip("#")))

        incumbentim = im.transpose(Image.FLIP_LEFT_RIGHT)
        incumbentim.save('i{}.png'.format(hexcode.strip("#")))

#change final comma into ']'
print('};')


