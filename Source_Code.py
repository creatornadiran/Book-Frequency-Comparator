import requests # To request HTML code
from bs4 import BeautifulSoup #To search in HTML codes
import fitz #To read text from PDF
import urllib.request#To read text from PDF
from stop_words import get_stop_words #for stopwords

try:
    n=int(input("Enter frequency number: "))
except:
    n = 20 #default
book_name=[] # book name's holding in list
word_list = [] #list of all words in the book
stop_words = [] #list of stop words getting from xpo6 (referenced by Vikipedi)
frequency = {0:{},1:{}} #frequency disctionary contains all the words (1 represents 1st book...)
sorted_frequency={0:{},1:{}} #sorted frequency disctionary
frequency_sum = {} #frequency disctionary contains all the words of the two books
sorted_frequency_sum={}#sorted frquency_sum disctionary
puncts="!#$%&()'+-,./:;*<=>?@[\]^_`“”{|}~.—\"" #punctuations will be removed
stop_chars=("abcdefghijklmnopqrstuvwxyz1234567890") #chars will be ignored
stop_words = get_stop_words('en') #getting and assigning stop words
stop_words.extend(['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't','ll', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'])
stop_words.extend(list(stop_chars)) #extending stop word list
tour=-1 #represents first and second book
while(True):
    tour += 1
    try: #Tries to scrape printable version first
        try: #firstly search on wikibooks
            book_name.append(input("Enter the book name: "))
            txt = open(f"{book_name[tour]}.txt", "w",encoding="utf-8")
            url=f"https://en.wikibooks.org/wiki/{book_name[tour]}" #scraping printable link first
            request= requests.get(url) #scraping HTML code
            soup = BeautifulSoup(request.text,"html.parser")
            printable_link=soup.find("a",text="printable version").get("href") #Searching on HTML code & getting printable version's link
            request=requests.get("https://en.wikibooks.org/"+printable_link)
            soup = BeautifulSoup(request.text, "html.parser")
            text = soup.find("div", {"class": "mw-parser-output"}).findChildren(recursive=False) #findChildren method does return all the child tag in a list
        except: #if the book is not available on wikibook searches on wikisource
            url = f"https://en.wikisource.org/wiki/{book_name[tour]}"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            text2 = soup.find("span", id= "headernext").a #To skip home page
            url = "https://en.wikisource.org" + text2.get("href")#getting next chapter/header link on wikisource
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            text = soup.find("div", {"class": "mw-parser-output"}).findChildren(recursive=False)
            while True: #scrapes all chapters
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                try: #stops when chapters are over
                    text2 = soup.find("span", id= "headernext").a
                except:
                    break
                url = "https://en.wikisource.org"+text2.get("href")
                request = requests.get(url)
                soup = BeautifulSoup(request.text, "html.parser")
                text += soup.find("div", {"class": "mw-parser-output"}).findChildren(recursive=False) #Adding current chapters HTML codes
        finally: #Searching on HTML code scraped to find texts
            for line in text:
                txt.write(line.text.lower())
        txt.close()  # closing text opened to write
    except: #if can not downloads printable version downloads PDF version // After downloading the pdf version, it writes the whole text to the txt file
        try:
            txt = open(f"{book_name[tour]}.txt", "w", encoding="utf-8")
            url = f"https://en.wikibooks.org/wiki/{book_name[tour]}"
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            link = soup.find_all("table", {"class": "plainlinks noprint messagebox growth"})
            for Link in link:
                if Link.b.find("a", {"class": "internal"}) != None:
                    download_link = Link.b.find("a", {"class": "internal"})
            download_link = download_link.get("href") #scraped pdf download link
            url2 = "http:" + download_link
            response = urllib.request.urlopen(url2)
            file = open(f"{book_name[tour]}" + ".pdf", 'wb') #Saves as PDF
            file.write(response.read())
            file.close()
            with fitz.open(f'{book_name[tour]}.pdf') as doc: #Read from pdf and saves on txt
                for page in doc:
                    txt.write(page.getText().lower())
            txt.close()  # closing text opened to write
        except:
            print("There is no book such that.")
    finally:
        txt = open(f"{book_name[tour]}.txt", "r", encoding='utf-8') #opening  text to read (encoding for unicode chars)
        txt1=txt.read()
        txt.close()
        for punct in puncts: #removing punctuations
            txt1 = txt1.replace(punct, " ") #Removes punctutations
        word_list = txt1.split()#Splits texts into words
    for word in word_list: #Transfer words to frequency list of current book
        frequency[tour][word]=0
        if word not in frequency_sum:#Transfer words to frequency_sum list
            frequency_sum[word]=0
    for word in word_list:
        if word == "":#skips the blanks/none
            continue
        elif word in stop_words: #skips the stop words
            continue
        frequency[tour][word]+=1 #Calculating frequency of current book
        frequency_sum[word] += 1 #Calculating the total frequency
    sorted_frequency[tour]=sorted(frequency[tour].items(), key=lambda x: x[1], reverse=True) #sorting frequency dict
    if(len(sorted_frequency[tour])>0):#
        print(f"Book name: {book_name[tour]}")
        print(f"{'NO':>3} {'WORD':<10} {'FREQ_1':>10}") #to keep code tidy used align format
        step = 1
        for word in sorted_frequency[tour]: #printing words and frequencies in a row
            if step>n: #stops the loop when it reaches the desired number
                break
            print(f"{step:>3}", f"{word[0]:<10}", f"{word[1]:>10}")
            step+=1
    else:#to stop when invalid book entered
        ans="n"
        break
    if(tour==0):
        while(True):
            ans=input("Do you want to compare to other book? y/n").lower() #asks user whether she/he wants to compare wit other book
            if ans=="y":
                double_break = False
                break
            elif ans=="n":
                double_break=True
                break
            else:
                print("Invalid Input")
    if(double_break or tour!=0):
        break
if(ans=="y"): #if user answers yes
    print("\n Total Frequency:")
    step=1
    print(f"{'NO':>3} {'WORD':<10} {'FREQ_1':>10} {'FREQ_2':>10} {'FREQ_3':>10}") #Formatting to look tidy
    sorted_frequency_sum= sorted(frequency_sum.items(), key=lambda x: x[1], reverse=True)
    for word in sorted_frequency_sum:
        if word[0] not in frequency[0] or word[0] not in frequency[1]: #Skips distinct words
            continue
        print(f"{step:>3}",f"{word[0]:<10}",f"{frequency[0][word[0]]:>10}",f"{frequency[1][word[0]]:>10}", f"{word[1]:>10}")
        step+= 1
        if step>n:
            break
    for i in range(2): #Printing distinct words
        step=1
        print(f"Book name: {book_name[i]}")
        print("Distinct Words:")
        print(f"{'NO':>3} {'WORD':<10} {'FREQ':>10}")
        for word in sorted_frequency[i]:
            if step > n:#stops the loop when it reaches the desired number
                break
            if word[0] not in frequency[(i+1)%2]:
                print(f"{step:>3}",f"{word[0]:<10}",f"{word[1]:>10}")
                step+=1



