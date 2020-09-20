import urllib3, json, requests, os, asyncio, getopt, sys

class ImageDownloader:
    def __init__(self):
        self.url = ""
        self.url_info = ()
        self.save_dir = ""
        self.json = {}
        self.save_to = ""

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url.lower()
        self.parse_url()

    @property
    def save_dir(self):
        return self.__save_dir

    @save_dir.setter
    def save_dir(self, save_dir):
        if save_dir == "":
            self.__save_dir = os.getcwd()
        else:
            self.__save_dir = os.path.join(os.getcwd(), save_dir)
        if not os.path.exists(self.__save_dir):
            try:
                os.makedirs(self.__save_dir)
            except:
                raise("InvalidDIR")

    def parse_url(self):
        try:
            url = self.url.split("/")
        except ValueError:
            return
        try:
            thread_index = url.index("thread")
            self.url_info = (url[thread_index - 1], url[thread_index + 1])
        except:
            return

    async def save_file(self, data):
        with open(os.path.join(self.save_to, data[0]), "wb") as f:
            print(f"https://i.4cdn.org/{self.url_info[1]}/{data[0]}")
            f.write(requests.get(f"https://i.4cdn.org/{self.url_info[0]}/{data[0]}").content)

    def start(self, require_confirm=False):
        pool_manager = urllib3.PoolManager()
        self.json = json.loads(pool_manager.request("GET", f"https://a.4cdn.org/{self.url_info[0]}/thread/{self.url_info[1]}.json").data)["posts"]
        
        self.save_to = os.path.join(self.save_dir, "imgdownloader", self.url_info[1])
        print(f"saving to {self.save_to}")
        
        if require_confirm:
            conf = ""
            while conf not in ["y", "n"]:
                conf = input("confirm (y/n) ")

            if conf == "n":
                print("download aborted")
                return

        try:
            os.makedirs(self.save_to)
        except FileExistsError:
            pass

        for i in self.json:
            try:
                asyncio.run(self.save_file((str(i["tim"]) + str(i["ext"]), round(int(i["fsize"]) / 1024, 1))))
            except KeyError:
                continue

def print_help():
    print("Arguments and usage examples")
    print("-h\thelp")
    print("--url\thttps://boards.4channel.org/g/thread/1333337/ OR g/thread/1333337")
    print("-s\tC:\\MyDirectory\\ OR \\My\\Directory")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:", ["url="])
        print(opts, args)
    except getopt.GetoptError as err:
        print(str(err))
        return

    if len(args) + len(opts) == 0:
        print_help()
    
    img_downloader = ImageDownloader()

    for opt, arg in opts:
        if opt == "--url":
            img_downloader.url = arg
        if opt == "-s":
            img_downloader.save_dir = arg
        if opt == "-h":
            print_help()

    img_downloader.start(require_confirm=True)

if __name__ == "__main__":
    main()
