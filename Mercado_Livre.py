#Mercado Livre Search Scrapper (Hix3nn)

from bs4 import BeautifulSoup
import requests
import csv
import re

#Abre o arquivo
csv_file = open('data.csv','a',newline='')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['Anúncio','Preço','Parcela','Juros','Frete','Vendas','Localização','Link'])

def user_input():    
    usr_input =input('Digite a Pesquisa: ')
    usr_input = usr_input.replace(" ","-")
    return usr_input

def page_number():
    num_loop = int(input('Digite o número de Páginas: '))
    while num_loop > 6:
        num_loop = int(input('Digite o número de Páginas: '))
    return num_loop

    
def Main():
    count = 0
    usr_input = user_input()
    num_loop= page_number()
    pages_increment = ['0','49','101','151','202','253']
    for x in range(0,num_loop):

        source = requests.get('https://lista.mercadolivre.com.br/'+usr_input+'_Desde_'+pages_increment[x]+'_DisplayType_LF').text
        soup = BeautifulSoup(source,"html5lib")

        for item_shop in soup.find_all('li', class_="results-item article stack "):
            name_item = item_shop.find('span',class_="main-title").text
            price_item = item_shop.find('span',class_="price__fraction").text
            link = item_shop.find('a',class_="item__info-title")['href']
            sales = item_shop.find('div',class_="item__condition").text

            #Parte decimal do preço pode não existir, no caso corresponde a zero
            if (item_shop.find('span',class_="price__decimals") == None):
                price_d_item = '00'
            else:
                price_d_item = item_shop.find('span',class_="price__decimals").text

            #quando o frete não é grátis
            if item_shop.find('p', class_="stack-item-info item--has-fulfillment") != None:
                delivery = (item_shop.find('p', class_="stack-item-info item--has-fulfillment").text).replace(' ','',1)
            elif item_shop.find('p', class_="stack-item-info ") == None:
                delivery = 'Combinar com o vendedor'
            else:
                delivery = (item_shop.find('p', class_="stack-item-info ").text).replace(' ','',1)

            # Caso não apareça no "pré" anúncio as parcelas
            if item_shop.find('span',class_="item-installments-multiplier") == None:
                pre_text = ''
                cc_t = 'Não divide no cartão'
                cc_price =''
            else:
                pre_text = 'Divide em'
                cc_t = (item_shop.find('span',class_="item-installments-multiplier").text + 'de')
                cc_price = (item_shop.find('span', class_="item-installments-price").text)


            #Caso não tenha a informação dos sem juros
            if (item_shop.find('span',class_="item-installments-interest") == None):
                interest = 'com juros'
            else:
                interest = (item_shop.find('span',class_="item-installments-interest").text).replace(' ','',1)

            #quando não há informação nenhuma
            if (item_shop.find('div',class_="item__condition") == None):
                sales_2 = ['0 vendidos','Sem Localização']

            #Quando não há vendas apenas a localização
            elif ' - ' not in (item_shop.find('div',class_="item__condition").text):
                sales_2 = ['0 vendidos',item_shop.find('div',class_="item__condition").text]

            #quando não tem frete grátis e tem vendas
            elif item_shop.find('p', class_="stack-item-info item__free-shipping-disabled") != None:
                if item_shop.find('p', class_="stack-item-info item__free-shipping-disabled").text == ' Envio para todo o país  ':
                    sales = (item_shop.find('div', class_="item__condition").text).replace(' ', '', 1)
                    sales_2=sales.split("-")

                else:
                    sales_2 = ['0',item_shop.find('p', class_="stack-item-info item__free-shipping-disabled").text]
            else:
                sales = (item_shop.find('div',class_="item__condition").text).replace(' ','',1)
                sales_2=sales.split("-")

            count += 1
            sales_2[1]=sales_2[1].replace(' ', '', 1)
            #Printando resultado
            print('Anúncio: ' + name_item)
            print('Preço: R$ ' + price_item +',' + price_d_item)
            print(pre_text + cc_t + cc_price + interest)
            print('Frete: ' + delivery)
            print('Link: ' +link)
            print('Vendas: '+ sales_2[0])
            print('Localização: ' + sales_2[1])
            print('\n')
            csv_writer.writerow([name_item,('R$ '+price_item+','+price_d_item),cc_price,interest,delivery,sales_2[0],sales_2[1],link])

    print('Foram extraídos '+str(count)+' anúncios.')
    csv_file.close
Main()
