# download all posts of a specific profile
'''
USERNAME = "therock"
profile = Profile.from_username(L.context, USERNAME)
for post in profile.get_posts():
    L.download_post(post, target=profile.username)
'''