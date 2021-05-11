import instascrape as ig
import pandas as pd


class InstagramScrapper:
    def __init__(self, following):

        self.following = following
        self.max_depth = 25
        self.columns = ['postid','likes', 'category','link','data']
        self.SESSIONID = '47114138175%3AbgoISOWzPi3O6b%3A7'
        self.seen = set()


        # keep only nonprivate accounts
        """
        for handle in following:
            profile = ig.Profile(handle)
            profile.scrape()
            if not profile.is_private:
                self.following.append(handle)
        """

    def scrape(self):
        df = pd.DataFrame(columns=self.columns)

        SESSIONID = self.SESSIONID
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
            "cookie": f"sessionid={SESSIONID};"}


        for handle in self.following:
            profile = ig.Profile(handle)
            profile.scrape(headers=headers)

            profile_posts = profile.get_recent_posts()
            depth = 0
            for post in profile_posts:

                if post.json_dict['__typename'] == 'GraphImage':
                    datetime = post.upload_date.strftime("%Y-%m-%d:%Hh%Mm")
                    #post.download(f"instagram_photos/{handle}{datetime}.png")

                    id = 'ig' + str(int(post.json_dict['id']) % 100000000).zfill(8)

                    display_url = post.json_dict['display_url']
                    caption = post.json_dict['edge_media_to_caption']['edges'][0]['node']
                    category = 'instagram@' + handle
                    thumbnail = post.json_dict['thumbnail_resources'][0]['src']
                    likes = post.likes # post.json_dict['likes']

                    #print(likes)
                    df = df.append({'postid':id,'likes':likes,'category': category,
                                    'link':display_url,'data':caption}, ignore_index=True)


                    depth += 1
                    if depth > self.max_depth:
                        break

        return df

    def close(self):
        return None



if __name__ == "__main__":
    instagram = InstagramScrapper(['carnegiemellon', 'instagram'])
    df = instagram.scrape()
    print(df.head())

