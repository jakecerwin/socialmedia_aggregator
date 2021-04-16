import instascrape as ig
import json, csv

raw_data = open("data/raw_instagram.json", "w")
cleaned_data = open("data/cleaned_instagram.csv", "w")
cleaned_data_writer = csv.writer(cleaned_data, delimiter=',')
cleaned_data_writer.writerow(['postid','author','datetime','imagelink','caption'])

handles = ['carnegiemellon', 'iris_rover', 'heinzcollege_careersvcs', 'carnegiemellonece']
# Instantiate the scraper objects

for handle in handles:

    profile = ig.Profile(handle)
    profile.scrape()
    profile_posts = profile.get_recent_posts()
    i = 0
    for post in profile_posts:

        json.dump(post.json_dict, raw_data, indent=2)


        #print(post.json_dict['__typename'])
        if post.json_dict['__typename'] == 'GraphImage':

            datetime = post.upload_date.strftime("%Y-%m-%d:%Hh%Mm")
            post.download(f"instagram_photos/{handle}{datetime}.png")

            id = post.json_dict['id']
            display_url = post.json_dict['display_url']
            caption = post.json_dict['edge_media_to_caption']['edges'][0]['node']
            thumbnail = post.json_dict['thumbnail_resources'][0]['src']

    
            #cleaned_data

            cleaned_data_writer.writerow([id, handle, datetime, display_url, caption])

            i += 1
            if i > 5:
                break
    


raw_data.close()
cleaned_data.close()

