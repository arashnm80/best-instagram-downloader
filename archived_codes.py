# download all posts of a specific profile
'''
USERNAME = "therock"
profile = Profile.from_username(L.context, USERNAME)
for post in profile.get_posts():
    L.download_post(post, target=profile.username)
'''
def media_id_to_code(media_id):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    short_code = ''
    while media_id > 0:
        remainder = media_id % 64
        media_id = (media_id-remainder)/64
        short_code = alphabet[remainder] + short_code
    return short_code


def code_to_media_id(short_code):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    media_id = 0
    for letter in short_code:
        media_id = (media_id*64) + alphabet.index(letter)

    return media_id

print(code_to_media_id("C0KuSEuI_JU"))
print(code_to_media_id("C0KuSEuI"))