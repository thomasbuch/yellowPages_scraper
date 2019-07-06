from selenium import webdriver
import csv
import html

#truck_db = [['entry', 'company', 'contact', 'phone', 'email', 'suburb',
#            'state', 'date', 'truck_type', 'comments', 'link']]
database = [['entry', 'company_name', 'description', 'phone', 'email', 'website', 'state', 'suburb', 'postnumber']]

entry = 0

def scrape_multiple_pages(entry, database):
    raw_name = input("What do you want to search on? (please don't use special characters like '&')\n")
    search_name = raw_name.replace(" ", "+")
    raw_location = input("Where do you want to search it - state, suburb or postcode? (please don't use special characters like '&')\n")
    search_location = raw_location.replace(" ", "+")
    page_number = int(input("How many pages do you want to scrape?\n")) + 1
    starting_page = int(input("Which page do you want to start on?\n"))
    for n in range(starting_page, starting_page + page_number):
        if n == 0:
            continue
        else:
            url = "https://www.yellowpages.com.au/search/listings?clue=" + search_name + "s&locationClue=" + search_location + "&pageNumber=" + str(n) + "&referredBy=www.yellowpages.com.au&&eventType=pagination"
            entry = scrape_page(entry, database, url, n)
            if entry == "break":
                break

def scrape_page(entry, database, url, n):
    content_cards = get_url(url)
    if content_cards == []:
        print("scraping ended at page " + str(n))
        return "break"
    database, entry = get_data(database, content_cards, entry)
    save_to_csv(database)
    return entry

def get_url(url):
    driver = webdriver.Chrome(executable_path=r"C:/Users/ThomasBuch/Desktop/chromedriver.exe")
    driver.get(url)
    content_cards = driver.find_elements_by_xpath("//div[contains(@class, 'search-contact-card') and contains(@class, 'call-to-actions')]")
    return content_cards

def get_data(database, content_cards, entry):
    for item in content_cards:
        htmltxt = item.get_attribute("innerHTML")

        if " ad " not in htmltxt:
            name_start = htmltxt.find('"View more about this business">') + len('"View more about this business">')
            name_end = name_start + htmltxt[name_start:].find("</a>")
            name = htmltxt[name_start:name_end]
            name = html.unescape(name)

            des_start = htmltxt.find('<h3 class="listing-short-description">') + len('<h3 class="listing-short-description">')
            des_end = des_start + htmltxt[des_start:].find("</h3>")
            description = ""
            description += htmltxt[des_start:des_end]
            description = html.unescape(description)

            phone_start = htmltxt.find('"contact-text">') + len('"contact-text">')
            phone_end = phone_start + htmltxt[phone_start:].find("</span>")
            phone = ""
            phone += htmltxt[phone_start:phone_end]

            email_start = htmltxt.find('data-email="') + len('data-email="')
            email_end = email_start + htmltxt[email_start:].find('"')
            email = ""
            email += htmltxt[email_start:email_end]
            if "<div class=" in email:
                email = ""

            website_locator = 'rel="nofollow" target="_blank" title="'
            look_for_website = htmltxt.find(website_locator) - 100
            website_start = look_for_website + htmltxt[look_for_website:].find('<a href="') + len('<a href="')
            website_end = website_start + htmltxt[website_start:].find('"')
            website = ""
            website += htmltxt[website_start:website_end]

            address_locator = htmltxt.find('<p class="listing-heading"')
            address_locator2 = address_locator + htmltxt[address_locator:].find('data-index-link="true">') + len('data-index-link="true">')
            suburb_start = address_locator2 + htmltxt[address_locator2:].find(" - ") + len(" - ")
            suburb_end = suburb_start + htmltxt[suburb_start:].find(",")
            suburb = ""
            suburb += htmltxt[suburb_start:suburb_end]

            state_start = suburb_end + htmltxt[suburb_end:].find(" ") + len(" ")
            state_end = state_start + htmltxt[state_start:].find(" ")
            state = ""
            state += htmltxt[state_start:state_end]

            post_start = state_end + htmltxt[state_end:].find(" ") + len(" ")
            post_end = post_start + 4
            postnumber = ""
            postnumber += htmltxt[post_start:post_end]

            data_entry = [entry, name, description, phone, email, website, suburb, state, postnumber]
            database.append(data_entry)
            print("data appended")

            entry += 1
    return database, entry

def save_to_csv(database):
    charset = 'cp1252'
    with open('yellowPages_data.csv', 'w', encoding = charset, errors = 'replace', newline = '') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(database)
    csvFile.close()

scrape_multiple_pages(entry, database)
