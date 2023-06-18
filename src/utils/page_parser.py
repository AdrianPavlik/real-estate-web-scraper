from string import Template

pages = ["https://www.nehnutelnosti.sk", "https://www.reality.sk", "https://www.zoznamrealit.sk/reality?ref=qs&q", "https://www.topreality.sk"]

district_format = ["$page/$district-kraj", "$page/$district-kraj", "$page=kraj-$district|typ-predaj", "$page/$district-kraj"]

districts = ["presovsky", "trenciansky", "trnavsky", "bratislavsky", "zilinsky", "kosicky", "banskobystricky", "nitriansky"]

for page in range(0, len(pages)):
    print(f"=-------------------------------------------------------------------------- ↓↓↓ {pages[page]} ↓↓↓")
    for district in range(0, len(districts)):
        template = Template(district_format[page])
        fn = template.substitute(page=pages[page],district=districts[district])
        print(f"\"{fn}\",")
