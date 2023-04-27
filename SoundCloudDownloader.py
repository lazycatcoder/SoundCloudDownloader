import requests, re, os, threading
from bs4 import BeautifulSoup


class SoundCloudDownloader:
    # Setting the request headers and getting the client_id
    def __init__(self):
        self.headers = {
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'api-v2.soundcloud.com',
            'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
        }
        self.client_id = self.get_client_id()

    # Getting the client_id
    def get_client_id(self):
        url = "https://soundcloud.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        scripts = soup.find_all("script")[-1]['src']
        script = requests.get(scripts).text
        client_id = script.split(",client_id:")[1].split('"')[1]
        return client_id

    # Getting the track name
    def get_track_name(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find("title").text
        track_name = re.search(r"Stream\s(.+)\sby", title).group(1)
        return track_name

    # Getting the track ID
    def get_track_id(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        track_id = soup.find("meta", property="twitter:app:url:googleplay")["content"].split(":")[-1]
        return track_id

    # Get the chunks of the track from SoundCloud API
    def get_track_chunks(self, track_id):
        url = f"https://api-v2.soundcloud.com/tracks?ids={track_id}&client_id={self.client_id}"
        res = requests.get(url, headers=self.headers).json()

        # Extract the stream URL from the response
        stream_url = res[0]["media"]["transcodings"][0]["url"]
        stream_url += "?client_id=" + self.client_id

        # Get m3u8 URL from the stream URL
        m3u8_url = requests.get(stream_url, headers=self.headers).json()["url"]
        
        # Get the content of the m3u8 file
        m3u8_file = requests.get(m3u8_url).text

        # Split the m3u8 file into chunks and filter out comments
        m3u8_file_split = m3u8_file.splitlines()
        chunks = []
        for chunk in m3u8_file_split:
            if "#" not in chunk:
                chunks.append(chunk)
        return chunks

    def download_track(self, file_name, chunks):
        file_name = file_name.strip()
        
        # Check if the file already exists
        if os.path.isfile(file_name + ".mp3"):
            i = 1
            while os.path.isfile(file_name + f" ({i:02d})" + ".mp3"):
                i += 1
            file_name += f" ({i:02d})"

        file_name += ".mp3"
        file = open(file_name, "ab")

        # Download each chunk and write its content to the file
        for chunk in chunks:
            content = requests.get(str(chunk), headers={}).content
            file.write(content)
        file.close()


    def get_track(self, url_list):
        # Check if the input is a string or a list
        if isinstance(url_list, str):
            url_list = [url_list]
        elif not isinstance(url_list, list):
            raise ValueError("Invalid input type. Expected str or list.")
                   
        def download_track_wrapper(url):
            # Call helper functions
            try:
                track_name = self.get_track_name(url)
                track_id = self.get_track_id(url)
                chunks = self.get_track_chunks(track_id)
                print(f"Downloading... \nName: {track_name}\nId: {track_id}")       
                self.download_track(track_name, chunks)
                print(f"{track_name} downloaded successfully!")
            except ValueError:
                print(f"Error downloading {url}. Invalid URL entered. Try again.")

        # Download tracks concurrently using threading
        threads = []
        for url in url_list:
            t = threading.Thread(target=download_track_wrapper, args=(url,))
            threads.append(t)
            t.start()
        
        # Wait for all threads to complete before returning
        for t in threads:
            t.join()



# Create an instance of the SoundCloudDownloader class
sc_downloader = SoundCloudDownloader()

# url = input("URL: ")
# sc_downloader.get_track(url)

# url = "https://soundcloud.com/username/trackname"
# sc_downloader.get_track(url)

url_list = [
    "https://soundcloud.com/username/trackname",
    "https://soundcloud.com/username/trackname",
    "https://soundcloud.com/username/trackname"
]
sc_downloader.get_track(url_list)