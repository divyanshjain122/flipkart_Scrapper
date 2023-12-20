import requests
from bs4 import BeautifulSoup
import csv
import os
import codecs
import emoji
import logging
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin

logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
  return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            flipkart_page="https://www.flipkart.com"
            ########inputs query########################
            query=request.form['content'].replace(" ","")
          # proxy="https://vepro.hocke.eu/proxy/index.php?"
            proxy=""
            flipkart_query_page=f'{proxy}{flipkart_page}/search?q={query}'
          # print(flipkart_query_page)
            try:
                flipkart_query_page_result=requests.get(flipkart_query_page)
            except ConnectionError:
                print("Connection error")
            except requests.exceptions.RequestException as e:
            # Handle any other errors
                print(f"Unhandled error: {e}")

          # print(flipkart_query_page_result)
          # print(flipkart_query_page_result.text)
            soup=BeautifulSoup(flipkart_query_page_result.text,"html.parser")
          # print(soup)

          ####################################getting list of all the products#################################################
            product_box_list=soup.find_all("div",{"class":"_2kHMtA"})
          
          ######################################## opening product link###################################


            k=0
            file_name=f'{query}.csv'
          

            try:
                with open(file_name, 'w', encoding='utf-8', errors='replace') as csvfile:
                    fieldnames = ['product','name', 'rating', 'review_heading', 'review_full']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
            except OSError as e :
                print(f"Error writing file: {e}")
            reviews = []

            for product in product_box_list[0:5]:
            # k=k+1
                product_link_test=flipkart_page+product.a['href']
                try:
                    product_page_request=(requests.get(product_link_test))
                except ConnectionError:
                    print("Connection error")
                except requests.exceptions.RequestException as e:
              # Handle any other errors
                    print(f"Unhandled error: {e}")
                product_soup=BeautifulSoup(product_page_request.text,'html.parser')
            # print (product_soup.prettify(encoding='utf-8')) ############### this line nessesary to prevent error###############
                comment_box_list=product_soup.find_all('div',{"class":"_16PBlm"})
                print(len(comment_box_list))
          ##################################stores revievs all comments of a perticular product#################################
            
                for comment_box in comment_box_list:
                    try:
                        name=emoji.demojize(comment_box.div.div.find('p',{"class":"_2sc7ZR _2V5EHH"}).text)
                        # print(name)
                    except:
                        logging.info("name")
                    try:
                        rating=comment_box.div.div.div.div.text
                        # print(rating)
                    except:
                        rating = 'No rating'
                        logging.info("rating")
                    try:
                        review_heading=emoji.demojize(comment_box.div.div.div.p.text)
                        # print(review_heading)
                    except:
                        review_heading='No review_heading'
                        logging.info("No review_heading")
                    try:
                        review_full=emoji.demojize(comment_box.div.div.find_all('div',{"class":""})[0].div.text)
                        # print(review_full)
                    except:
                        review_full='No review_full'
                        logging.info("No review_full")
                    mydict={"product":query,"name":name,"rating":rating,"review_heading":review_heading,"review_full":review_full}
                    reviews.append(mydict)
              # fieldnames = ['name', 'rating', 'review_heading', 'review_full']
        
            # logging.info("log my final result {0}".format(reviews))  
            try:
                reviews=reviews[0:len(reviews)-1]  
            except:
                print("problem in reveis -1")
            try:
                print(reviews)
            except:
                print("error in list of dictionaries reviews")
            # try :
                
            return render_template('result.html',reviews=reviews) 
            # except:
                # print("problem found") 
                # return render_template('base.html')  
              # try:
              #   with open(file_path, 'a', encoding='utf-8', errors='replace') as csvfile:
              #     fieldnames = ['name', 'rating', 'review_heading', 'review_full']
              #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

              #     writer.writerow({'name': name, 'rating': rating, 'review_heading': review_heading, 'review_full': review_full})
              # except OSError as e :
              #   print(f"Error writing file: {e}")
        
        
        
        
        
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(host="0.0.0.0")




















# from flask import Flask, render_template, request,jsonify
# from flask_cors import CORS,cross_origin
# import requests
# from bs4 import BeautifulSoup as bs
# from urllib.request import urlopen as uReq
# import logging
# logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

# app = Flask(__name__)

# @app.route("/", methods = ['GET'])
# def homepage():
#     return render_template("index.html")

# @app.route("/review" , methods = ['POST' , 'GET'])
# def index():
#     if request.method == 'POST':
#         try:
#             searchString = request.form['content'].replace(" ","")
#             flipkart_url = "https://www.flipkart.com/search?q=" + searchString
#             uClient = uReq(flipkart_url)
#             flipkartPage = uClient.read()
#             uClient.close()
#             flipkart_html = bs(flipkartPage, "html.parser")
#             bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
#             del bigboxes[0:3]
#             box = bigboxes[0]
#             productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
#             prodRes = requests.get(productLink)
#             prodRes.encoding='utf-8'
#             prod_html = bs(prodRes.text, "html.parser")
#             print(prod_html)
#             commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})

#             filename = searchString + ".csv"
#             fw = open(filename, "w")
#             headers = "Product, Customer Name, Rating, Heading, Comment \n"
#             fw.write(headers)
#             reviews = []
#             for commentbox in commentboxes:
#                 try:
#                     #name.encode(encoding='utf-8')
#                     name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

#                 except:
#                     logging.info("name")

#                 try:
#                     #rating.encode(encoding='utf-8')
#                     rating = commentbox.div.div.div.div.text


#                 except:
#                     rating = 'No Rating'
#                     logging.info("rating")

#                 try:
#                     #commentHead.encode(encoding='utf-8')
#                     commentHead = commentbox.div.div.div.p.text

#                 except:
#                     commentHead = 'No Comment Heading'
#                     logging.info(commentHead)
#                 try:
#                     comtag = commentbox.div.div.find_all('div', {'class': ''})
#                     #custComment.encode(encoding='utf-8')
#                     custComment = comtag[0].div.text
#                 except Exception as e:
#                     logging.info(e)

#                 mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
#                           "Comment": custComment}
#                 print(mydict)
#                 reviews.append(mydict)
#             logging.info("log my final result {}".format(reviews))
#             return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
#         except Exception as e:
#             logging.info(e)
#             return 'something is wrong'
#     # return render_template('results.html')

#     else:
#         return render_template('index.html')


# if __name__=="__main__":
#     app.run(host='127.0.0.1', port=5000, debug=True)
