from bs4 import BeautifulSoup
import unittest
import requests
import csv

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!

print('\n\n       *********** NEW EXECUTION ***********\n')

######### PART 0 #########

# Write your code for Part 0 here.

page = requests.get("http://newmantaylor.com/gallery.html")
print(page.status_code,'\n')

soup = BeautifulSoup(page.content, 'html.parser')

all_imgs = soup.find_all('img')
for i in all_imgs:
    print(i.get('alt', "No alt text provided"))


######### PART 1 #########

# Get the main page data...

def Pull_cache(site, file_name, states):
    try:
      main_data = open(file_name,'r').read()
    except:
      main_data = requests.get(site).text
      f = open(file_name,'w')
      f.write(main_data)
      f.close()

    soup = BeautifulSoup(main_data, 'html.parser')
    menu = soup.find('div', {'class': 'SearchBar-keywordSearch input-group input-group-lg'})
    state_list = menu.find_all('a', href = lambda href: href and 'state' in href)

    link_list = []
    for st in states:
        for item in state_list:
            text = str(item)
            find_st = '/'+st+'/'
            if find_st in text:
                link_list.append(item)

    url_list = []
    for item in link_list:
        nameU = find_specific(str(item),'>','</')
        name = nameU.lower()
        abrev = find_specific(str(item),'state/','/index')
        try:
            fname = name+'_data'
            fname = open(name+'_data.html','r').read()
            link = 'https://www.nps.gov/state/'+abrev+'/index.htm'
            url_list.append(link)
        except:
            fname = name+'_data'
            link = 'https://www.nps.gov/state/'+abrev+'/index.htm'
            url_list.append(link)
            fname = requests.get(link).text
            f = open(name+'_data.html','w')
            f.write(fname)
            f.close()
    return url_list


def find_specific(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""



#states = ['Arkansas', 'California', 'Michigan']
states = ['ar', 'ca', 'mi']
urls = Pull_cache('https://www.nps.gov/index.htm', 'nps_gov_data.html', states)



######### PART 2 #########


## Define your class NationalSite here:


class NationalSite(object):

    def __init__(self, object):
        if object == None:
            macroInfo = None
        else:
            self.macroInfo = object
            self.name = self.macroInfo.find('a').get_text()
            self.location = self.macroInfo.find('h4').get_text()
            self.type = self.macroInfo.find('h2').get_text()
            self.description = self.macroInfo.find('p').text

    def __str__(self):
        return '{} {} | {}'.format(self.type, self.name, self.location)

    def get_mailing_address(self):

        holder = self.macroInfo.find('h3')
        site = holder.find('a')['href']
        link = 'https://www.nps.gov/'+site+'/index.htm'
        site_data = requests.get(link).text
        siteSoup = BeautifulSoup(site_data, 'html.parser')

        self.macroAdr = siteSoup.find('p', {'class': 'adr'}).get_text()
        badChars = '\n'
        for c in badChars: self.macroAdr = self.macroAdr.replace(c, " ")
        return '{}'.format(self.macroAdr)

        badChars = '\n'
        #self.address = self.macroAdr.strip('','\n')
        for c in badChars: self.macroAdr = self.macroAdr.replace(c, " ")
        return '{}'.format(self.macroAdr)

    def __contains__(self, test_string):
        #if test_string == type(''):
        return test_string in self.name



######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.


def CreateSiteUrl(state):
    link = 'https://www.nps.gov/state/'+state+'/index.htm'
    state_data = requests.get(link).text
    stateSoup = BeautifulSoup(state_data, 'html.parser')

    siteList =[]
    parks = stateSoup.find('ul', {'id': 'list_parks'})
    siteList = parks.find_all('li', {'class': 'clearfix'})

    siteObjectList = []
    for site in siteList:
        siteObject = NationalSite(site)
        siteObjectList.append(siteObject)

    return siteObjectList


arkansas_natl_sites = CreateSiteUrl('ar')
california_natl_sites = CreateSiteUrl('ca')
michigan_natl_sites = CreateSiteUrl('mi')


#below code uses student example from piazza
def CreateSiteCSV(siteList, state):
    with open(state+'.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for obj in siteList:
            writer.writerow([obj.name, obj.location, obj.type, obj.get_mailing_address(), obj.description])
    return


CreateSiteCSV(arkansas_natl_sites, 'arkansas')
CreateSiteCSV(california_natl_sites, 'california')
CreateSiteCSV(michigan_natl_sites, 'michigan')
