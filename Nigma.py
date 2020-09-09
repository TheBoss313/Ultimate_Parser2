from bs4 import BeautifulSoup

s = """
<section class="grid-wrap">
                
                <ul class="grid">
                  <li class="grid-sizer li-sticker"></li>
                  <li id='gallery-pages-sticker-small' class="li-sticker">
  <figure>
    <div class="wrap-img-head">
      <div class='wrap-cover-img zoom-slide '><img src="https://www.nigmabook.ru/cgi-bin/unishell?usr_data=gd-image(lots,NF0001491,,1,fix-i1_asis-340x214,00000000,)&hide_Cookie=yes" alt="Капитан Сорви-голова. Повесть" title="Капитан Сорви-голова. Повесть"></div>
    </div>
  </figure>
</li><li id='gallery-pages-sticker-small-26' class="li-sticker">
  <figure>
    <div class="wrap-img-head">
      <div class='wrap-cover-img zoom-slide '><img src="https://www.nigmabook.ru/cgi-bin/unishell?usr_data=gd-image(lots,NF0001491,,1,fix-i2_asis-340x214,00000000,)&hide_Cookie=yes" alt="Капитан Сорви-голова. Повесть" title="Капитан Сорви-голова. Повесть"></div>
    </div>
  </figure>
</li><li id='gallery-pages-sticker-small-27' class="li-sticker">
  <figure>
    <div class="wrap-img-head">
      <div class='wrap-cover-img zoom-slide '><img src="https://www.nigmabook.ru/cgi-bin/unishell?usr_data=gd-image(lots,NF0001491,,1,fix-i3_asis-340x214,00000000,)&hide_Cookie=yes" alt="Капитан Сорви-голова. Повесть" title="Капитан Сорви-голова. Повесть"></div>
    </div>
  </figure>
</li><li id='gallery-pages-sticker-small-28' class="li-sticker">
  <figure>
    <div class="wrap-img-head">
      <div class='wrap-cover-img zoom-slide '><img src="https://www.nigmabook.ru/cgi-bin/unishell?usr_data=gd-image(lots,NF0001491,,1,fix-i4_asis-340x214,00000000,)&hide_Cookie=yes" alt="Капитан Сорви-голова. Повесть" title="Капитан Сорви-голова. Повесть"></div>
    </div>
  </figure>
</li><li id='gallery-pages-sticker-small-29' class="li-sticker">
  <figure>
    <div class="wrap-img-head">
      <div class='wrap-cover-img zoom-slide '><img src="https://www.nigmabook.ru/cgi-bin/unishell?usr_data=gd-image(lots,NF0001491,,1,fix-i5_asis-340x214,00000000,)&hide_Cookie=yes" alt="Капитан Сорви-голова. Повесть" title="Капитан Сорви-голова. Повесть"></div>
    </div>
  </figure>
</li><li id='gallery-pages-sticker-small-30' class="li-sticker">
  <figure>
    <div class="wrap-img-head">
      <div class='wrap-cover-img zoom-slide '><img src="https://www.nigmabook.ru/cgi-bin/unishell?usr_data=gd-image(lots,NF0001491,,1,fix-i6_asis-340x214,00000000,)&hide_Cookie=yes" alt="Капитан Сорви-голова. Повесть" title="Капитан Сорви-голова. Повесть"></div>
    </div>
  </figure>
</li><li id='gallery-pages-sticker-small-31' class="li-sticker">
"""

soup = BeautifulSoup(s, "html.parser")
p_tag = soup.find("section", class_="grid-wrap")
for i in p_tag.findAll('img'):
    print(i.get('src'))
