import schedule
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import autoit
import clipboard


#from ui_gui import Ui_WhatsappAutomation
#from callgui import addcontacts
import time
import datetime
import os

browser = None
Contact = None
message = None
Link = "https://web.whatsapp.com/"
wait = None
choice = None
docChoice = None
doc_filename = None
unsaved_Contacts = None
excep = None

def input_contacts(x,n,inp,choi):
    global Contact,unsaved_Contacts
    # List of Contacts

    Contact = []
    unsaved_Contacts = []
    while True:
        # Enter your choice 1 or 2
        print("1.Enter Saved Contact number->")
        print("2.Enter Unsaved Contact number->")
        #x = int(input("Enter your choice(1 or 2):->"))

        if int(x) == 1:
            Contact = inp
            #n = int(input('Enter number of Contacts to add(count)->'))
            #for i in range(0,int(n)):
                #inp = str(input("Enter contact name(text)->"))
                #inp = '"' + inp + '"'
                #print (inp)
                #Contact.append(inp)
        elif int(x) == 2:
            #n = int(input('Enter number of unsaved Contacts to add(count)->'))
            #for i in range(0,n):
                # Example use: 919899123456, Don't use: +919899123456
                # Reference : https://faq.whatsapp.com/en/android/26000030/
                #inp = str(input("Enter unsaved contact number with country code(interger)->"))
                # print (inp)
                unsaved_Contacts = inp

        #choi = input("Do you want to add more contacts(yes or no)->")
        if choi == "no":
            break

    print("Saved contacts entered list->",Contact)
    print("Unsaved numbers entered list->",unsaved_Contacts)

def input_message(msg):
    print("Message Scanned")
    global message
    # Enter your Good Morning Msg
    message = msg

def whatsapp_login(ch,dch):
    print("QR Scanning")
    global wait,browser,Link
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 600)
    browser.get(Link)
    browser.maximize_window()
    print("QR Scanned")
    #sender(ch,dch)

def send_message(target):
    global message,wait, browser

    excep = None
    chat_path = '//*[@id="app"]/div/div/div[3]/div/header/div[2]/div/span/div[2]/div/span'
    chat_button = wait.until(EC.presence_of_element_located((By.XPATH, chat_path)))
    chat_button.click()
    x_arg = '//span[contains(@title,' + target + ')]'
    try:
        group_title = browser.find_element_by_xpath(x_arg)
        print("Found")
    except Exception as e:
        excep = str(e)

    if excep == None:
        target = target.replace('"','')
        inp_xpath_search = "//input[@title='Search contacts']"
        input_box_search = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath_search)))
        input_box_search.send_keys(target + Keys.ENTER)


        #group_title.click()
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
                #input_box.send_keys(clipboard.paste())
        #clipboard.copy(message)
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)


def send_unsaved_contact_message():
    global message,wait, browser
    try:
        time.sleep(5)
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        time.sleep(7)
        print("Message sent successfuly")
    except NoSuchElementException:
        print("Failed to send message")
        return

def send_attachment(dfn):
    # Attachment Drop Down Menu
    global browser
    clipButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)

    # To send Videos and Images.
    mediaButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button')
    mediaButton.click()
    time.sleep(3)
    image_path = dfn #os.getcwd() + "\\Media\\" + 'image.jpg'
    #hour = datetime.datetime.now().hour

    # After 5am and before 11am scheduled this.
    #if(hour >=5 and hour <=11):

    # After 9pm and before 11pm schedule this
    #elif (hour>=21 and hour<=23):
        #image_path = os.getcwd() +"\\Media\\" + 'goodnight.jpg'
    #else: # At any other time schedule this.
        #image_path = os.getcwd() +"\\Media\\" + 'howareyou.jpg'
    # print(image_path)

    autoit.control_focus("Open","Edit1")
    autoit.control_set_text("Open","Edit1",(image_path) )
    autoit.control_click("Open","Button1")
	
    time.sleep(3)
    #whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span')
    whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span')
    whatsapp_send_button.click()

#Function to send Documents(PDF, Word file, PPT, etc.)
def send_files(dfilename):
    global browser
    # Attachment Drop Down Menu
    clipButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)

    # To send a Document(PDF, Word file, PPT)
    docButton = browser.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button')
    docButton.click()
    time.sleep(1)

    docPath = dfilename

    autoit.control_focus("Open","Edit1")
    autoit.control_set_text("Open","Edit1",(docPath) )
    autoit.control_click("Open","Button1")

    time.sleep(3)
    #whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span')
    whatsapp_send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span')
    whatsapp_send_button.click()


def sender(choice, docChoice,imgn,dfn):
    global Contact, unsaved_Contacts
    for i in Contact:  
        #print(message+"check")
        try:
            send_message(i)
            print("Message sent to ",i)
            if(choice=="yes"):
                send_attachment(imgn)
            if(docChoice == "yes"):
                send_files(dfilename=dfn)
        except:
            pass
    time.sleep(5)
    if len(unsaved_Contacts)>0:
        for i in unsaved_Contacts:
            link = "https://wa.me/"+i
            #driver  = webdriver.Chrome()
            browser.get(link)
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="action-button"]').click()
            time.sleep(5)
            print("Sending message to", i)
            try:
                send_unsaved_contact_message()
                if(choice=="yes" and docChoice=="yes"):
                    send_attachment(imgn)
                    send_files(dfilename=dfn)
                    time.sleep(20)
                elif(choice=="no" and docChoice == "yes"):
                    send_files(dfilename=dfn)
                    time.sleep(10)
                elif(choice=="yes" and docChoice == "no"):
                    send_attachment(imgn)
                    time.sleep(10)
            except:
                pass


# For GoodMorning Image and Message
schedule.every().day.at("07:00").do( sender )
# For How are you message
schedule.every().day.at("13:35").do( sender )
# For GoodNight Image and Message
schedule.every().day.at("22:00").do( sender )

# Example Schedule for a particular day of week Monday
schedule.every().monday.at("08:00").do(sender)


# To schedule your msgs
def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":

    print("Web Page Open")
    # Append more contact as input to send messages
    input_contacts()
    # Enter the message you want to send
    input_message()
    #Send Attachment Media only Images/Video
    choice = input("Would you like to send attachment(yes/no): ")
    # Let us login and Scan

    docChoice = input("Would you file to send a Document file(yes/no): ")
    if(docChoice == "yes"):
        # Note the document file should be present in the Document Folder
        doc_filename = input("Enter the Document file name you want to send: ")

    print("SCAN YOUR QR CODE FOR WHATSAPP WEB")
    whatsapp_login()

    # Send message to all Contact List
    # This sender is just for testing purpose to check script working or not.
    # Scheduling works below.
    #Comment this line is case you don't want to test
    #or have completed the testing part of script.
    sender()

    # First send Task Complete
    print("Completed")

    # Messages are scheduled to send
    scheduler()

    # browser.quit()