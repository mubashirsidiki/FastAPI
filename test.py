my_posts = [{'id' : 1 ,\
             'title' : 'title of post 1',\
             'content' : 'content of post 1'},\
            {'id' : 2 ,\
             'title' : 'fav foods',\
             'content' : 'zinger burger'}]
id = 2
for i in my_posts:
    #print(i)
    if i['id'] == id:
        print({'post_detail' : f"here is post {i}"})
        break