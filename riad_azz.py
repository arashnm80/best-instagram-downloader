from variables import *

def generate_request_body(shortcode):
    return urllib.parse.urlencode({
        'av': '0',
        '__d': 'www',
        '__user': '0',
        '__a': '1',
        '__req': 'b',
        '__hs': '20183.HYP:instagram_web_pkg.2.1...0',
        'dpr': '3',
        '__ccg': 'GOOD',
        '__rev': '1021613311',
        '__s': 'hm5eih:ztapmw:x0losd',
        '__hsi': '7489787314313612244',
        '__dyn': '7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJw5ux609vCwjE1EE2Cw8G11wBz81s8hwGxu786a3a1YwBgao6C0Mo2swtUd8-U2zxe2GewGw9a361qw8Xxm16wa-0oa2-azo7u3C2u2J0bS1LwTwKG1pg2fwxyo6O1FwlA3a3zhA6bwIxe6V8aUuwm8jwhU3cyVrDyo',
        '__csr': 'goMJ6MT9Z48KVkIBBvRfqKOkinBtG-FfLaRgG-lZ9Qji9XGexh7VozjHRKq5J6KVqjQdGl2pAFmvK5GWGXyk8h9GA-m6V5yF4UWagnJzazAbZ5osXuFkVeGCHG8GF4l5yp9oOezpo88PAlZ1Pxa5bxGQ7o9VrFbg-8wwxp1G2acxacGVQ00jyoE0ijonyXwfwEnwWwkA2m0dLw3tE1I80hCg8UeU4Ohox0clAhAtsM0iCA9wap4DwhS1fxW0fLhpRB51m13xC3e0h2t2H801HQw1bu02j-',
        '__comet_req': '7',
        'lsd': 'AVrqPT0gJDo',
        'jazoest': '2946',
        '__spin_r': '1021613311',
        '__spin_b': 'trunk',
        '__spin_t': '1743852001',
        '__crn': 'comet.igweb.PolarisPostRoute',
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'PolarisPostActionLoadPostQueryQuery',
        'variables': json.dumps({
            'shortcode': shortcode,
            'fetch_tagged_user_count': None,
            'hoisted_comment_id': None,
            'hoisted_reply_id': None,
        }),
        'server_timestamps': 'true',
        'doc_id': '8845758582119845',
    })

def get_instagram_media_links(shortcode):
    url = "https://www.instagram.com/graphql/query"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-FB-Friendly-Name': 'PolarisPostActionLoadPostQueryQuery',
        'X-BLOKS-VERSION-ID': '0d99de0d13662a50e0958bcb112dd651f70dea02e1859073ab25f8f2a477de96',
        'X-CSRFToken': 'uy8OpI1kndx4oUHjlHaUfu',
        'X-IG-App-ID': '1217981644879628',
        'X-FB-LSD': 'AVrqPT0gJDo',
        'X-ASBD-ID': '359341',
        'Sec-GPC': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Referer': f'https://www.instagram.com/p/{shortcode}/',
    }
    data = generate_request_body(shortcode)
    response = requests.post(url, headers=headers, data=data, proxies=warp_proxies)
    response.raise_for_status()
    json_response = response.json()

    # debug - to view json view pretty
    with open(f"instagram_response.json", "w") as f:
        json.dump(json_response, f, indent=2)

    media_links = []
    caption = None
    try:
        media = json_response['data']['xdt_shortcode_media']
        # caption
        caption = media.get('edge_media_to_caption', {}).get('edges', [{}])[0].get('node', {}).get('text', '')
        # Check if it's a sidecar (multiple media)
        if media.get('__typename') == 'XDTGraphSidecar' and 'edge_sidecar_to_children' in media:
            edges = media['edge_sidecar_to_children']['edges']
            for edge in edges:
                node = edge['node']
                media_type = 'video' if node.get('is_video', False) else 'image'
                if media_type == 'video':
                    url = node.get('video_url')
                else:
                    display_resources = node.get('display_resources', [])
                    if display_resources:
                        url = display_resources[-1]['src']
                    else:
                        url = node.get('display_url')
                media_links.append({'type': media_type, 'url': url})
        else:
            media_type = 'video' if media.get('is_video', False) else 'image'
            if media_type == 'video':
                url = media.get('video_url')
            else:
                display_resources = media.get('display_resources', [])
                if display_resources:
                    url = display_resources[-1]['src']
                else:
                    url = media.get('display_url')
            media_links.append({'type': media_type, 'url': url})
    except Exception as e:
        print(f"Error extracting media info: {e}")
        # return "error", f"{e}"
    return media_links, caption

# # Example usage:
# # shortcode = "DJx51PyxMpy"  # rock post: multiple videos and images
# shortcode = "DMLLAxNsWFL"  # zelatan: one video (opens in my browser but erros for telegram servers)
# links, caption = get_instagram_media_links(shortcode)
# print(links, caption)