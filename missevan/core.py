# SPDX-FileCopyrightText: 2022 Weibin Jia <me@isweibin.com>
# SPDX-License-Identifier: Apache-2.0

import httpx


class MissEvanSpider():

    def __init__(self, dramaid=None, soundid=None):
        self.dramaid = dramaid
        self.soundid = soundid
        self.soundname = ''
        self.headers = {
            'Cookie': 'Hm_lvt_91a4e950402ecbaeb38bd149234eb7cc=1666867677,1667906714; Hm_lpvt_91a4e950402ecbaeb38bd149234eb7cc=1668079521; MSESSID=i0qqrqhhql9bc0ds4mj0eka9qh; acw_tc=76b20fe516680792856353541e250e1904dc374fb677269d46f34b76f70058; token=636cdeddfea7dc17c89cb7e9%7C5d0655c2cd16b52d2a687d2c257ade6f%7C1668079325%7C91fc420cfed43792',
            'Referer': f'https://www.missevan.com/mdrama/{self.dramaid}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        }

    def get_soundurl(self):
        url = f'https://www.missevan.com/sound/getsound?soundid={self.soundid}'
        resp = httpx.get(url=url, headers=self.headers)
        soundurl =  resp.json()['info']['sound']['soundurl']

        return soundurl

    def download_sound(self):
        soundurl = self.get_soundurl()
        resp = httpx.get(url=soundurl, headers=self.headers)
        if self.soundname:
            filename = f'downloads/{self.soundid}_{self.soundname}.m4a'
        else:
            filename = f'downloads/{self.soundid}.m4a'
        with open(filename, 'wb') as f:
            f.write(resp.content)

    def get_episodes(self):
        url = f'https://www.missevan.com/dramaapi/getdrama?drama_id={self.dramaid}'
        resp = httpx.get(url=url, headers=self.headers)
        episodes = resp.json()['info']['episodes']['episode']
        episodes = {_['name']:_['sound_id'] for _ in episodes}
        
        return episodes
    
    def download_episodes(self):
        episodes = self.get_episodes()
        for k, v in episodes.items():
            self.soundid, self.soundname = k, v
            self.download_sound()


if __name__ == '__main__':
    print("MissEvan Spider, enter dramaid or soundid to download!" + "\n")
    dramaid = input("? dramaid ")
    soundid = input("? soundid ")
    if dramaid:
        spider = MissEvanSpider(dramaid=dramaid)
        spider.download_episodes()
    elif soundid:
        spider = MissEvanSpider(soundid=soundid)
        spider.download_sound()
