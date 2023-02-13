import os
import re
import time

try:import img2pdf
except ModuleNotFoundError:os.system('pip3 install img2pdf');import img2pdf
try:import requests
except ModuleNotFoundError:os.system('pip3 install requests');import requests
try:from bs4 import BeautifulSoup
except ModuleNotFoundError:os.system('pip3 install bs4');from bs4 import BeautifulSoup 
try:from colorama import Fore, Back
except ModuleNotFoundError:os.system('pip3 install colorama');from colorama import Fore, Back


def image2pdf(manga, chapter):
    os.chdir(fr"MangaImages")
    imageList = os.listdir(os.getcwd())
    pdf = img2pdf.convert(imageList)
    os.chdir("..")
    with open(f"{manga}/Chapter{chapter}.pdf", "wb") as D:
        D.write(pdf)
        D.close()
    if os.name == 'nt':
        os.system(f'RMDIR MangaImages /S /Q')
    else:
        os.system('sudo rm -r MangaImages')


def slice_text(text):
    global img
    soup = BeautifulSoup(str(text), "html.parser")
    scripts = soup.find_all("script", {"class": "js-react-on-rails-component"})
    string_data = scripts[0].get_text()
    data = json.loads(string_data)
    readerDataAction = data['readerDataAction']
    readerData = readerDataAction['readerData']
    release = readerData['release']
    pages = release['pages']
    storage_key = release['storage_key']
    storage_url = "https://media.gmanga.me/uploads/releases/"
    idk = "/mq_webp/"
    images = []
    for page in pages:
        image = storage_url + storage_key + idk + page
        img = [f"{image}.webp", f'{image}.jpg', f'{image}.png', f'{image}.jpg', f'{image}.jpg.jpg', f'{image}.jpg.webp']
        for i in img:
            response = requests.get(i).status_code
            if response != 200:
                continue
            else:
                images.append(i)
                break
        continue
    return images


def lekDownload(manga, start='10', end='10', good=False):
    global goodfile
    mangaName = str(manga).replace(" ", "-")

    if good:
        goodfile = open("GoodChapters.txt").readlines()
    else:
        start = int(start)
        end = int(end)
        if start > end:
            print(f"{Fore.RED}Bruh..☠")
            exit()

    response = requests.get(f"https://mangalek.com/manga/{mangaName}")
    if response.url == 'https://mangalek.com':
        exit(
            f"{Fore.LIGHTWHITE_EX}[{Fore.RED}-{Fore.LIGHTWHITE_EX}]{Fore.RED} Hmm..? Search Error With Your Manga >> {mangaName}")
    #
    if not os.path.exists(f"{mangaName}"):
        os.mkdir(f"{mangaName}")

    if good:
        for i in goodfile:
            i = str(i)
            if not os.path.exists("MangaImages"):
                os.mkdir('MangaImages')

            site = f'https://mangalek.com/manga/{mangaName}/{i}'
            response = requests.get(site)

            # if '<h4 class="comments-title">' in response.text:
            #    print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}-{Fore.LIGHTWHITE_EX}] Hmm..? Search {Fore.LIGHTYELLOW_EX}Error{Fore.LIGHTWHITE_EX} With Chapter {start}")
            #    exit()

            soup = BeautifulSoup(response.text, 'html.parser')
            image_tags = soup.find_all('img')

            urls = [img['src'] for img in image_tags]

            print(
                f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Found {len(urls) - 1} Images For Chapter {i}")

            k = 10
            for url in urls:
                k += 1

                if k == 1:
                    continue

                filename = re.search(r'/([\w_-]+[.](jpg|png))$', url)

                if not filename:
                    continue

                with open(f"MangaImages/Image{k}.jpg", "wb") as f:
                    if 'http' not in url:
                        url = site, url
                    response = requests.get(url)
                    f.write(response.content)
                    f.close()

            image2pdf(manga=mangaName, chapter=i)

            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Download Chapter {i}.. \n")
        print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] All Chapter Download Successfully")

    else:
        while True:

            if start == end + 1:
                print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] All Chapter Download Successfully")
                break

            if not os.path.exists("MangaImages"):
                os.mkdir('MangaImages')

            site = f'https://mangalek.com/manga/{mangaName}/{start}'
            response = requests.get(site)

            # if '<h4 class="comments-title">' in response.text:
            #    print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}-{Fore.LIGHTWHITE_EX}] Hmm..? Search {Fore.LIGHTYELLOW_EX}Error{Fore.LIGHTWHITE_EX} With Chapter {start}")
            #    exit()

            soup = BeautifulSoup(response.text, 'html.parser')
            image_tags = soup.find_all('img')

            urls = [img['src'] for img in image_tags]

            print(
                f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Found {len(urls) - 1} Images For Chapter {start}")

            k = 10
            for url in urls:
                k += 1

                if k == 1:
                    continue

                filename = re.search(r'/([\w_-]+[.](jpg|png))$', url)

                if not filename:
                    continue

                with open(f"MangaImages/Image{k}.jpg", "wb") as f:
                    if 'http' not in url:
                        url = site, url
                    response = requests.get(url)
                    f.write(response.content)
                    f.close()

            image2pdf(manga=mangaName, chapter=start)

            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Download Chapter {start}.. \n")
            start += 1


def azoraDownload(manga, start='10', end='10', good=False):
    # Not Working ! I Think We Can Download Image But We Cant Convert To PDF ):

    mangaName = str(manga).replace(" ", "-")

    start = int(start)
    end = int(end)

    if start > end:
        print(f"{Fore.RED}Bruh..☠")
        exit()

    response = requests.get(f"https://azoranov.com/series/{mangaName}")
    if response.status_code == 404:
        exit(
            f"{Fore.LIGHTWHITE_EX}[{Fore.RED}-{Fore.LIGHTWHITE_EX}]{Fore.RED} Hmm..? Search Error With Your Manga >> {mangaName}")
    #
    if not os.path.exists(f"{mangaName}"):
        os.mkdir(f"{mangaName}")

    while True:
        if not os.path.exists("MangaImages"):
            os.mkdir('MangaImages')

        if start == end + 1:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] All Chapter Download Successfully")
            break

        site = f'https://azoranov.com/series/{mangaName}/{start}'
        response = requests.get(site)

        # if '??' in response.text:
        #    print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}-{Fore.LIGHTWHITE_EX}] Hmm..? Search {Fore.LIGHTYELLOW_EX}Error{Fore.LIGHTWHITE_EX} With Chapter {start}")
        #    exit()

        soup = BeautifulSoup(response.text, 'html.parser')
        image_tags = soup.find_all('img')

        urls = [img['src'] for img in image_tags]

        print(
            f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Found {len(urls) - 1} Images For Chapter {start}")

        k = 10
        for url in urls:
            k += 1

            if k == 1:
                continue

            filename = re.search(r'/([\w_-]+[.](jpg|png))$', url)

            if not filename:
                continue

            with open(f"MangaImages/Image{k}.jpg", "wb") as f:
                if 'http' not in url:
                    url = site, url
                response = requests.get(url)
                f.write(response.content)
                f.close()

        image2pdf(manga=mangaName, chapter=start)

        print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Download Chapter {start}.. \n")
        start += 1


def teamxDownload(manga, start='10', end='10', good=False):
    mangaName = str(manga).replace(" ", "-")

    start = int(start)
    end = int(end)

    if start > end:
        print(f"{Fore.RED}Bruh..☠")
        exit()

    response = requests.get(f"https://team1x1.fun/series/{mangaName}")
    if response.status_code == 404:
        exit(
            f"{Fore.LIGHTWHITE_EX}[{Fore.RED}-{Fore.LIGHTWHITE_EX}]{Fore.RED} Hmm..? Search Error With Your Manga >> {mangaName}")
    #
    if not os.path.exists(f"{mangaName}"):
        os.mkdir(f"{mangaName}")

    while True:

        if start == end + 1:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] All Chapter Download Successfully")
            break

        if not os.path.exists("MangaImages"):
            os.mkdir('MangaImages')

        site = f'https://team1x1.fun/series/{mangaName}/{start}'
        response = requests.get(site)

        # if '??' in response.text:
        #    print(f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}-{Fore.LIGHTWHITE_EX}] Hmm..? Search {Fore.LIGHTYELLOW_EX}Error{Fore.LIGHTWHITE_EX} With Chapter {start}")
        #    exit()

        soup = BeautifulSoup(response.text, 'html.parser')
        image_tags = soup.find_all('img')

        urls = [img['src'] for img in image_tags]

        print(
            f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Found {len(urls) - 1} Images For Chapter {start}")

        k = 10
        for url in urls:
            k += 1

            if k == 1:
                continue

            with open(f"MangaImages/Image{k}.jpg", "wb") as f:
                if 'http' not in url:
                    url = site, url
                response = requests.get(url)
                f.write(response.content)
                f.close()

        image2pdf(manga=mangaName, chapter=start)

        print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Download Chapter {start}.. \n")
        start += 1


def gmangaDownload(manga, ID, start='10', end='10', good=False):
    global goodfile
    mangaName = str(manga).replace(" ", "-")

    if good:
        goodfile = open('GoodChapters.txt').readlines()

    else:
        start = int(start)
        end = int(end)

        if start > end:
            print(f"{Fore.RED}Bruh..☠")
            exit()

    response = requests.get(f"https://gmanga.org/mangas/{ID}/{mangaName}")
    if response.status_code == 404:
        exit(
            f"{Fore.LIGHTWHITE_EX}[{Fore.RED}-{Fore.LIGHTWHITE_EX}]{Fore.RED} Hmm..? Search Error With Your Manga >> {mangaName}")
    #
    if not os.path.exists(f"{mangaName}"):
        os.mkdir(f"{mangaName}")

    if good:
        for i in goodfile:
            if not os.path.exists("MangaImages"):
                os.mkdir('MangaImages')
            site = f'https://gmanga.org/mangas/{ID}/{mangaName}/{i}'
            response = requests.get(site)

            if response.status_code == 404:
                print(
                    f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}-{Fore.LIGHTWHITE_EX}] Hmm..? Search {Fore.LIGHTYELLOW_EX}Error{Fore.LIGHTWHITE_EX} With Chapter {i}")
                exit()

            slice_text(response.text)
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Found {len(urls) - 1} Images For Chapter {i}")

            k = 10
            for url in urls:
                k += 1

                with open(f"MangaImages/Image{k}.jpg", "wb") as f:
                    if 'http' not in url:
                        url = site, url
                        print(url)
                    response = requests.get(url)
                    f.write(response.content)
                    f.close()

            image2pdf(manga=mangaName, chapter=i)

            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Download Chapter Successfully{i} \n")
        print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] All Chapter Download Successfully")

    else:
        while True:
            if not os.path.exists("MangaImages"):
                os.mkdir('MangaImages')

            if start == end + 1:
                print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] All Chapter Download Successfully")
                break

            site = f'https://gmanga.org/mangas/{ID}/{mangaName}/{start}'
            response = requests.get(site)

            if response.status_code == 404:
                print(
                    f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}-{Fore.LIGHTWHITE_EX}] Hmm..? Search {Fore.LIGHTYELLOW_EX}Error{Fore.LIGHTWHITE_EX} With Chapter {start}")
                exit()

            soup = BeautifulSoup(response.text, 'html.parser')
            image_tags = soup.find_all('img')

            urls = [img['src'] for img in image_tags]

            print(
                f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Found {len(urls) - 1} Images For Chapter {start}")

            k = 10
            for url in urls:
                k += 1

                if k == 1:
                    continue

                filename = re.search(r'/([\w_-]+[.](jpg|png|webp))$', url)

                if not filename:
                    continue

                with open(f"MangaImages/Image{k}.jpg", "wb") as f:
                    if 'http' not in url:
                        url = site, url
                        print(url)
                    response = requests.get(url)
                    f.write(response.content)
                    f.close()

            image2pdf(manga=mangaName, chapter=start)

            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Download Chapter {start}.. \n")
            start += 1


def _3ashqDownload(manga, start='10', end='10', good=False):
    global goodfile
    mangaName = str(manga).replace(" ", "-")

    if good:
        goodfile = open('GoodChapters.txt').readlines()

    else:
        start = int(start)
        end = int(end)

        if start > end:
            print(f"{Fore.RED}Bruh..☠")
            exit()

    response = requests.get(f"https://3asq.org/manga/{mangaName}")
    if response.status_code == 404:
        exit(
            f"{Fore.LIGHTWHITE_EX}[{Fore.RED}-{Fore.LIGHTWHITE_EX}]{Fore.RED} Hmm..? Search Error With Your Manga >> {mangaName}")

    if not os.path.exists(f"{mangaName}"):
        os.mkdir(f"{mangaName}")

    if good:
        for i in goodfile:
            if not os.path.exists("MangaImages"):
                os.mkdir('MangaImages')

            site = f'https://3asq.org/manga/{mangaName}/{i}/'
            response = requests.get(site)

            if response.status_code == 404:
                exit(
                    f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}-{Fore.LIGHTWHITE_EX}] Hmm..? Search {Fore.LIGHTYELLOW_EX}Error{Fore.LIGHTWHITE_EX} With Chapter {i}")

            soup = BeautifulSoup(response.text, 'html.parser')
            image_tags = soup.find_all('img')

            urls = [img['src'] for img in image_tags]

            print(
                f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Found {len(urls) - 1} Images For Chapter {i}")
            k = 10
            for url in urls:
                k += 1

                if k == 10:
                    continue

                with open(f"MangaImages/Image{k}.jpg", "wb") as f:
                    if 'http' not in url:
                        url = site, url
                        print(url)
                    response = requests.get(url)
                    f.write(response.content)
                    f.close()
            image2pdf(mangaName, start)

            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Download Chapter {i} Successfully \n")
            start += 1

    while True:
        if not os.path.exists("MangaImages"):
            os.mkdir('MangaImages')

        if start == end:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] All Chapter Download Successfully")
            break

        site = f'https://3asq.org/manga/{mangaName}/{start}/'
        response = requests.get(site)

        if response.status_code == 404:
            exit(
                f"{Fore.LIGHTWHITE_EX}[{Fore.LIGHTYELLOW_EX}-{Fore.LIGHTWHITE_EX}] Hmm..? Search {Fore.LIGHTYELLOW_EX}Error{Fore.LIGHTWHITE_EX} With Chapter {start}")

        soup = BeautifulSoup(response.text, 'html.parser')
        image_tags = soup.find_all('img')

        urls = [img['src'] for img in image_tags]

        print(
            f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Found {len(urls) - 1} Images For Chapter {start}")
        k = 10
        for url in urls:
            k += 1

            if k == 10:
                continue

            with open(f"MangaImages/Image{k}.jpg", "wb") as f:
                if 'http' not in url:
                    url = site, url
                    print(url)
                response = requests.get(url)
                f.write(response.content)
                f.close()
        image2pdf(mangaName, start)

        print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN}+{Fore.LIGHTWHITE_EX}] Download Chapter {start} Successfully \n")
        start += 1


def gmangaStart():
    print(f"\n{Fore.WHITE}Example: gmanga.org/mangas/8587/Berserk")
    URL = input(f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Enter Manga URL  : ")

    if 'https://' in URL:
        exit(f"{Fore.LIGHTWHITE_EX}[ {Fore.RED}-{Fore.LIGHTWHITE_EX} ] Please Enter The URL Without \"https://\" : ")

    mangaName = URL.split("/")[3]
    mangaID = URL.split("/")[2]
    print(f"- Manga Name => {mangaName}", end='\r')
    print(f"- Manga ID => {mangaID}\n", end='\r')
    time.sleep(2)

    GC = input(
        f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Use GoodChapters File [G] or Costom [C] [G/C]:")
    if GC.title() == 'C':
        print(f'\n{Fore.WHITE}Example: 10-100\n')
        start1 = input(
            f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Enter From Chapter To Chapter For Download:").split(
            "-")
        try:
            start = start1[0]
            end = start1[1]
        except IndexError:
            start = start1[0]
            end = start1[0]

        print(
            f"{Fore.LIGHTWHITE_EX}[ {Fore.YELLOW}${Fore.LIGHTWHITE_EX} ] So You Want To Download Chapter {start} To Chapter {end} From {mangaName} Manga !\n")
        print('\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

        gmangaDownload(manga=mangaName, ID=mangaID, start=start, end=end)

    elif GC.title() == 'G':
        if not os.path.exists('GoodChapters.txt'):
            exit(f"{Fore.LIGHTWHITE_EX}[ {Fore.RED}-{Fore.LIGHTWHITE_EX} ] You Dont Have GoodChapters File !")

        print('\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
        gmangaDownload(manga=mangaName, ID=mangaID, good=True)


def lekStart():
    print(f"\n{Fore.WHITE}Example: berserk")
    mangaName = input(f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Enter Manga Name  : ")

    GC = input(
        f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Use GoodChapters File [G] or Custom [C] [G/C]:")
    if GC.title() == 'C':

        print(f'\n{Fore.WHITE}Example: 10-100')
        start1 = input(
            f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Enter From Chapter To Chapter For Download:").split(
            "-")

        start = start1[0]
        end = start1[1]
        print(
            f"{Fore.LIGHTWHITE_EX}[ {Fore.YELLOW}${Fore.LIGHTWHITE_EX} ] So You Want To Download Chapter {start} To Chapter {end} From {mangaName} Manga !\n")

        print('\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
        lekDownload(manga=mangaName, start=start, end=end)

    elif GC.title() == 'G':
        if not os.path.exists('GoodChapters.txt'):
            exit(f"{Fore.LIGHTWHITE_EX}[ {Fore.RED}-{Fore.LIGHTWHITE_EX} ] You Dont Have GoodChapters File !")
        print('\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
        lekDownload(manga=mangaName, good=True)


def _3ashqStart():
    print(f"\n{Fore.WHITE}Example: Berserk\n")
    mangaName = input(f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Enter Manga Name  : ")

    print(f'\n\n{Fore.WHITE}Example: 10-100')
    print(f"{Fore.WHITE}Note: We Just Can Download Chapter Like 1, 10, 44")

    start1 = input(
        f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Enter From Chapter To Chapter For Download:").split(
        "-")
    start = start1[0]
    end = start1[1]
    print(
        f"{Fore.LIGHTWHITE_EX}[ {Fore.YELLOW}${Fore.LIGHTWHITE_EX} ] So You Want To Download Chapter {start} To Chapter {end} From {mangaName} Manga !\n")
    time.sleep(5)

    _3ashqDownload(manga=mangaName, start=start, end=end)


def teamxStart():
    print(f"\n{Fore.WHITE}Example: master of gu")
    mangaName = input(f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Enter Manga Name  : ")

    GC = input(
        f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Use GoodChapters File [G] or Custom [C] [G/C]:")
    if GC.title() == 'C':

        print(f'\n{Fore.WHITE}Example: 10-100')
        start1 = input(
            f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Enter From Chapter To Chapter For Download:").split(
            "-")

        start = start1[0]
        end = start1[1]
        print(
            f"{Fore.LIGHTWHITE_EX}[ {Fore.YELLOW}${Fore.LIGHTWHITE_EX} ] So You Want To Download Chapter {start} To Chapter {end} From {mangaName} Manga !\n")

        print('\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
        teamxDownload(manga=mangaName, start=start, end=end)

    elif GC.title() == 'G':
        if not os.path.exists('GoodChapters.txt'):
            exit(f"{Fore.LIGHTWHITE_EX}[ {Fore.RED}-{Fore.LIGHTWHITE_EX} ] You Dont Have GoodChapters File !")
        print('\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
        teamxDownload(manga=mangaName, good=True)


def checkGmanga(manga, ID):
    k = float(0)
    chapters = ['0A', '0B', '0C', '0D', '0E', '0F', '0G', '0H', '0Y', '0J', '0K']
    for chapter in range(100):

        response = requests.get(f'https://gmanga.org/mangas/{ID}/{manga}/{chapter}', timeout=2)

        if 'الصفحة غير موجودة' in response.text:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.RED} - {Fore.LIGHTWHITE_EX}] {chapter} => {Fore.RED} False")
        else:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN} + {Fore.LIGHTWHITE_EX}] {chapter} => {Fore.CYAN}True")
            with open("GoodChapters.txt", "a") as D:
                D.write(f'{chapter}\n')

    for i in range(100):
        if str(k).endswith('0'):
            continue

        response = requests.get(f'https://gmanga.org/mangas/{ID}/{manga}/{k}', timeout=2.5)

        if 'الصفحة غير موجودة' in response.text:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.RED} - {Fore.LIGHTWHITE_EX}] {k} => {Fore.RED} False")
        else:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN} + {Fore.LIGHTWHITE_EX}] {k} => {Fore.CYAN}True")
            with open("GoodChapters.txt", "a") as D:
                D.write(f'{k}\n')
        k += 0.5

    for chapter in chapters:
        response = requests.get(f'https://gmanga.org/mangas/{ID}/{manga}/{chapter}', timeout=2.5)

        if 'الصفحة غير موجودة' in response.text:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.RED} - {Fore.LIGHTWHITE_EX}] {chapter} => {Fore.RED} False")
        else:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN} + {Fore.LIGHTWHITE_EX}] {chapter} => {Fore.CYAN}True")
            with open("GoodChapters.txt", "a") as D:
                D.write(f'{chapter}\n')
        k += 0.5
    print(f"{Fore.WHITE} [$] All Exists Chapter Printed In File Named [GoodChapters.txt]")
    print("[$] You Can Download All Exists Chapter From Download Mod (:")


def checkLek(manga):
    k = float(0)
    chapters = ['0A', '0B', '0C', '0D', '0E', '0F', '0G', '0H', '0Y', '0J', '0K']
    for chapter in range(100):

        response = requests.get(f'https://mangalek.com/manga/{manga}/{chapter}/', timeout=2.5)

        if response.status_code != 200:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.RED} - {Fore.LIGHTWHITE_EX}] {chapter} => {Fore.RED} False")
        else:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN} + {Fore.LIGHTWHITE_EX}] {chapter} => {Fore.CYAN}True")
            with open("GoodChapters.txt", "a") as D:
                D.write(f'{chapter}\n')

    for i in range(100):
        if str(k).endswith('0'):
            continue

        response = requests.get(f'https://mangalek.com/manga/{manga}/{k}/', timeout=2)

        if response.status_code != 200:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.RED} - {Fore.LIGHTWHITE_EX}] {k} => {Fore.RED} False")
        else:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN} + {Fore.LIGHTWHITE_EX}] {k} => {Fore.CYAN}True")
            with open("GoodChapters.txt", "a") as D:
                D.write(f'{k}\n')
        k += 0.5

    for chapter in chapters:
        response = requests.get(f'https://mangalek.com/manga/{manga}/{chapter}/', timeout=2)

        if response.status_code != 200:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.RED} - {Fore.LIGHTWHITE_EX}] {chapter} => {Fore.RED} False")
        else:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN} + {Fore.LIGHTWHITE_EX}] {chapter} => {Fore.CYAN}True")
            with open("GoodChapters.txt", "a") as D:
                D.write(f'{chapter}\n')
        k += 0.5
    print(f"{Fore.WHITE} [$] All Exists Chapter Printed In File Named [GoodChapters.txt]")
    print("[$] You Can Download All Exists Chapter From Download Mod (:")


def checkTeamX(manga):
    k = float(0)
    chapters = ['0A', '0B', '0C', '0D', '0E', '0F', '0G', '0H', '0Y', '0J', '0K']
    for chapter in range(100):

        response = requests.get(f'https://team1x1.fun/series/{manga}/{chapter}', timeout=2.5)

        if response.status_code != 200:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.RED} - {Fore.LIGHTWHITE_EX}] {chapter} => {Fore.RED} False")
        else:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN} + {Fore.LIGHTWHITE_EX}] {chapter} => {Fore.CYAN}True")
            with open("GoodChapters.txt", "a") as D:
                D.write(f'{chapter}\n')

    for i in range(100):
        if str(k).endswith('0'):
            continue

        response = requests.get(f'https://team1x1.fun/series/{manga}/{k}', timeout=2.5)

        if response.status_code != 200:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.RED} - {Fore.LIGHTWHITE_EX}] {k} => {Fore.RED} False")
        else:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN} + {Fore.LIGHTWHITE_EX}] {k} => {Fore.CYAN}True")
            with open("GoodChapters.txt", "a") as D:
                D.write(f'{k}\n')
        k += 0.5

    for chapter in chapters:
        response = requests.get(f'https://team1x1.fun/series/{manga}/{chapter}', timeout=2.5)

        if response.status_code != 200:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.RED} - {Fore.LIGHTWHITE_EX}] {chapter} => {Fore.RED} False")
        else:
            print(f"{Fore.LIGHTWHITE_EX}[{Fore.CYAN} + {Fore.LIGHTWHITE_EX}] {chapter} => {Fore.CYAN}True")
            with open("GoodChapters.txt", "a") as D:
                D.write(f'{chapter}\n')
        k += 0.5
    print(f"{Fore.WHITE} [$] All Exists Chapter Printed In File Named [GoodChapters.txt]")
    print("[$] You Can Download All Exists Chapter From Download Mod (:")


def Settings():
    modes = input(f"""\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
               \tTitle: Homepage
{Fore.GREEN}Mods :
{Fore.CYAN}- 0 - Download manga from sites{Fore.LIGHTWHITE_EX}
{Fore.YELLOW}- 1 - Check chapters if exists {Fore.LIGHTWHITE_EX}
{Fore.RED}- 2 - Exit ..{Fore.LIGHTWHITE_EX}
[$] Enter : """)
    if modes == '0':
        m0des = input(f"""\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
               \tTitle: Choice Site\n
{Fore.GREEN}Choose your site :
{Fore.YELLOW}- 1 - gmanga.org
- 2 - mangalek.com
- 3 - 3asq.org
- 4 - team1x1.fun
{Fore.CYAN}- 5 - Go Back <<{Fore.LIGHTWHITE_EX}
[$] Enter : """)
        if m0des == '1':
            print('\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
            gmangaStart()
        elif m0des == '2':
            print('\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
            lekStart()
        elif m0des == '3':
            print('\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
            _3ashqStart()
        elif m0des == '4':
            print('\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
            teamxStart()
        else:
            print('\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
            return Settings()
    elif modes == '1':
        modng = input(f"""\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           Title: Choice site to check
{Fore.GREEN}Choose your site :
{Fore.YELLOW}- 1 - gmanga.org
- 2 - mangalek.com
- 3 - team1x1.fun
{Fore.CYAN}- 4 - Go Back <<{Fore.LIGHTWHITE_EX}
[$] Enter : """)
        if modng == '1':
            print('\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            print(f"\n{Fore.WHITE}Example: gmanga.org/mangas/8587/Berserk")
            URL = input(f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Enter Manga URL  : ")

            if 'https://' in URL:
                exit(
                    f"{Fore.LIGHTWHITE_EX}[ {Fore.RED}-{Fore.LIGHTWHITE_EX} ] Please Enter The URL Without \"https://\" : ")

            mangaName = URL.split("/")[3]
            mangaID = URL.split("/")[2]
            print(f"- Manga Name => {mangaName}", end='\r')
            print(f"- Manga ID => {mangaID}\n", end='\r')
            print('\n\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
            checkGmanga(manga=mangaName, ID=mangaID)

        if modng == '2':
            print('\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            print(f"\n{Fore.WHITE}Example: berserk")
            mangaName = input(f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Enter Manga Name : ")

            checkLek(manga=mangaName)

        if modng == '3':
            print('\t\t━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            print(f"\n{Fore.WHITE}Example: master of gu")
            mangaName = input(f"{Fore.LIGHTWHITE_EX}[ {Fore.MAGENTA}*{Fore.LIGHTWHITE_EX} ] Enter Manga Name : ")

            checkTeamX(manga=mangaName)

        else:
            print("\r")
            Settings()

    else:
        exit()


if __name__ == '__main__':
    print(f"""{Back.BLACK}{Fore.LIGHTWHITE_EX}

        ███    ███  █████  ███    ██  ██████   █████      {Fore.RED}██   ██{Fore.LIGHTWHITE_EX}
        ████  ████ ██   ██ ████   ██ ██       ██   ██     {Fore.RED} ██ ██{Fore.LIGHTWHITE_EX}
        ██ ████ ██ ███████ ██ ██  ██ ██   ███ ███████     {Fore.RED}  ███{Fore.LIGHTWHITE_EX}
        ██  ██  ██ ██   ██ ██  ██ ██ ██    ██ ██   ██     {Fore.RED} ██ ██{Fore.LIGHTWHITE_EX}
        ██      ██ ██   ██ ██   ████  ██████  ██   ██     {Fore.RED}██   ██{Fore.LIGHTWHITE_EX}

			{Fore.YELLOW}By Dexter @u.qdq
		    GitHub: https://github.com/dexter-90{Fore.LIGHTWHITE_EX}
""")
    Settings()
    print("""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n""")
