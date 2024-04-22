from bs4 import BeautifulSoup
#from urllib.request import Request, urlopen
import urllib.request
import time, traceback
import pandas as pd

#fiis_list = ["btlg11"]
fiis_list = ["bcff11","btlg11","cpts11","cvbi11","deva11","ggrc11","hctr11","hfof11","hgbs11","hglg11","hgru11","hsml11","irdm11","kncr11","knri11","mcci11","mfii11","mxrf11","rbva11","recr11","rect11","rzat11","snci11","snff11","tord11","trbl11","trxf11","urpr11","vgip11","visc11","vrta11","vslh11","xpci11","xpcm11","xplg11","xpml11"]

fiis_indicators = []
for fii in fiis_list:
  url = f"https://statusinvest.com.br/fundos-imobiliarios/{fii}"
  print(url)
  
  time.sleep(0.25)
  try:
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
    html = urllib.request.urlopen(req)
    soup = BeautifulSoup(html, 'html.parser')

    fund = soup.find("div", id="fund-section")
    main = soup.find("main", id="main-2")

    name = fund.find_all("div", "info")[1].find("strong").getText()
    init = fund.find_all("div", "info")[2].find("strong").getText()
    sector = fund.find("div", "top-info top-info-1 top-info-sm-2 top-info-md-n sm d-flex justify-between").find("strong").getText()
    type = fund.find_all("div", "info")[4].find("strong").getText()
    administrator = fund.find("div", "container").find("strong", "fw-700").getText()

    price = main.find("div", title="Valor atual do ativo").find("strong").getText()
    dividend_yield = main.find("div", title="Dividend Yield com base nos últimos 12 meses").find("strong").getText()
    net_worth = main.find("div", "top-info top-info-2 top-info-md-3 top-info-lg-n d-flex justify-between").find_all("div", recursive=False)[0].find("span", "sub-value").getText().replace("R$ ","")
    asset_value = main.find("div", "top-info top-info-2 top-info-md-3 top-info-lg-n d-flex justify-between").find_all("div", recursive=False)[0].find("strong").getText()
    pvp = main.find("div", "top-info top-info-2 top-info-md-3 top-info-lg-n d-flex justify-between").find_all("div", recursive=False)[1].find("strong").getText()
    shareholders = main.find("div", "top-info top-info-2 top-info-md-3 top-info-lg-n d-flex justify-between").find_all("div", recursive=False)[5].find("strong").getText()
    lastDiv = main.find("div", "mt-5 d-flex flex-wrap flex-lg-nowrap justify-between").find_all("div", recursive=False)[1].find("strong").getText()
    lastDate = main.find("div", "mt-5 d-flex flex-wrap flex-lg-nowrap justify-between").find_all("div", recursive=False)[1].find_all("b")[3].getText()
    nextDiv = main.find("div", "mt-5 d-flex flex-wrap flex-lg-nowrap justify-between").find_all("div", recursive=False)[2].find("strong").getText()
    nextDate = main.find("div", "mt-5 d-flex flex-wrap flex-lg-nowrap justify-between").find_all("div", recursive=False)[2].find_all("b")[3].getText()

    dict = {  "fii": fii,
        "nome": name,
        "segmento": sector,
        "tipo": type,
        "administrador": administrator,
        "cotistas" : shareholders,
        "patrimonio": net_worth,
        "vp" : asset_value,
        "valor_atual": price,
        "pvp": pvp,
        "dividend_yield": dividend_yield,
        "ultimo dividendo" : lastDiv,
        "data pagamento(u)": lastDate,
        "proximo dividendo" : nextDiv,
        "data pagamento(p)": nextDate,
    }
    fiis_indicators.append(dict)
  except Exception as e:
    print(e)
    print(repr(traceback.format_exception(e)))

df = pd.DataFrame.from_dict(fiis_indicators)
df.to_excel("fiis.xlsx", index=False)
