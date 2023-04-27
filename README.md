<div align="center">
  <h1>SoundCloud Downloader</h1>
</div>

<div align="justify">
   This script allows you to download tracks from the <a href="https://soundcloud.com/">SoundCloud</a> platform at the track URL. It uses the SoundCloud API to get the streaming URL of a track and breaks it up into small chunks that are downloaded and merged into a single file. The script can process several tracks at the same time using Threading. 
</div>

<br>

<div align="center">

# Settings
To use it, you need to complete the following steps:

<br>

### 📁 Clone this repository

   ```
   git clone https://github.com/lazycatcoder/SoundCloudDownloader.git
   ```

<br>

### 📦 Install dependencies
   
   ```
   pip install -r requirements.txt
   ```

<br>

### 🔧 Additional Information

<div align="left">

<br>
In order to download music, you can enter links to tracks from SoundCloud:

*- manually through the terminal* 

   ```
      url = input("URL: ")
      sc_downloader.get_track(url)
   ```
<br>

*- pass a link to one track directly in the code*

   ```
      url = "https://soundcloud.com/username/trackname"
      sc_downloader.get_track(url)
   ```

<br>

*- pass a list of links to multiple tracks*

   ```
      url_list = [
         "https://soundcloud.com/username/trackname",
         "https://soundcloud.com/username/trackname",
         "https://soundcloud.com/username/trackname"
      ]
      sc_downloader.get_track(url_list)
   ```

<br>

</div>