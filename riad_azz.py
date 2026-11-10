import json
import time

import requests

from variables import *

POST_DOC_ID = "27128499623469141"
LEGACY_POST_DOC_ID = "8845758582119845"
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "X-IG-App-ID": "1217981644879628",
    "X-ASBD-ID": "359341",
}


def _media_item(media_type, url):
    if not url:
        return None
    return {"type": media_type, "url": url}


def _warmup_session(session, shortcode, content_type):
    referer = f"https://www.instagram.com/{content_type}/{shortcode}/"
    response = session.get(
        referer,
        headers={**DEFAULT_HEADERS, "Accept": "text/html,application/xhtml+xml"},
        proxies=warp_proxies,
        timeout=20,
    )
    response.raise_for_status()
    return referer


def _graphql_variables(shortcode, doc_id):
    if doc_id == POST_DOC_ID:
        return {
            "shortcode": shortcode,
            "__relay_internal__pv__PolarisAIGMMediaWebLabelEnabledrelayprovider": False,
        }
    return {
        "shortcode": shortcode,
        "fetch_tagged_user_count": None,
        "hoisted_comment_id": None,
        "hoisted_reply_id": None,
    }


def _graphql_query(session, shortcode, content_type, doc_id):
    referer = _warmup_session(session, shortcode, content_type)
    csrf = session.cookies.get("csrftoken", "")
    params = {
        "variables": json.dumps(_graphql_variables(shortcode, doc_id), separators=(",", ":")),
        "doc_id": doc_id,
        "server_timestamps": "true",
    }
    response = session.get(
        "https://www.instagram.com/graphql/query",
        headers={
            **DEFAULT_HEADERS,
            "X-CSRFToken": csrf,
            "Referer": referer,
        },
        params=params,
        proxies=warp_proxies,
        timeout=20,
    )
    if response.status_code != 200:
        raise ValueError(f"graphql status {response.status_code}")
    payload = response.json()
    if payload.get("errors"):
        raise ValueError(payload["errors"][0].get("message", "graphql error"))
    return payload


def _extract_from_graphql_media(media):
    media_links = []
    caption = ""
    caption_data = media.get("edge_media_to_caption", {}).get("edges", [])
    if caption_data:
        caption = caption_data[0].get("node", {}).get("text", "") or ""

    if media.get("__typename") == "XDTGraphSidecar" and "edge_sidecar_to_children" in media:
        for edge in media["edge_sidecar_to_children"]["edges"]:
            node = edge["node"]
            if node.get("is_video"):
                item = _media_item("video", node.get("video_url"))
            else:
                display_resources = node.get("display_resources", [])
                url = display_resources[-1]["src"] if display_resources else node.get("display_url")
                item = _media_item("photo", url)
            if item:
                media_links.append(item)
    elif media.get("is_video"):
        item = _media_item("video", media.get("video_url"))
        if item:
            media_links.append(item)
    else:
        display_resources = media.get("display_resources", [])
        url = display_resources[-1]["src"] if display_resources else media.get("display_url")
        item = _media_item("photo", url)
        if item:
            media_links.append(item)
    return media_links, caption


def _extract_from_v1_media(media):
    media_links = []
    caption_data = media.get("caption")
    caption = caption_data.get("text", "") if isinstance(caption_data, dict) else ""

    carousel = media.get("carousel_media") or []
    if carousel:
        for item in carousel:
            if item.get("media_type") == 2:
                videos = item.get("video_versions") or []
                media_item = _media_item("video", videos[0]["url"] if videos else None)
            else:
                candidates = (item.get("image_versions2") or {}).get("candidates") or []
                media_item = _media_item("photo", candidates[0]["url"] if candidates else None)
            if media_item:
                media_links.append(media_item)
    elif media.get("media_type") == 2:
        videos = media.get("video_versions") or []
        media_item = _media_item("video", videos[0]["url"] if videos else None)
        if media_item:
            media_links.append(media_item)
    else:
        candidates = (media.get("image_versions2") or {}).get("candidates") or []
        media_item = _media_item("photo", candidates[0]["url"] if candidates else None)
        if media_item:
            media_links.append(media_item)
    return media_links, caption


def _parse_graphql_payload(payload):
    data = payload.get("data") or {}
    web_info = data.get("xdt_api__v1__media__shortcode__web_info") or {}
    items = web_info.get("items") or []
    if items:
        return _extract_from_v1_media(items[0])

    media = data.get("xdt_shortcode_media")
    if media:
        return _extract_from_graphql_media(media)

    raise ValueError("graphql returned no media")


def _content_types_to_try(content_type):
    if content_type == "reel":
        return ("reel", "p")
    return (content_type or "p",)


def fetch_instagram_media(shortcode, content_type="p"):
    errors = []
    session = requests.Session()
    for doc_id in (POST_DOC_ID, LEGACY_POST_DOC_ID):
        for path_type in _content_types_to_try(content_type):
            for attempt in range(3):
                if attempt:
                    time.sleep(3 * attempt)
                try:
                    payload = _graphql_query(session, shortcode, path_type, doc_id)
                    media_links, caption = _parse_graphql_payload(payload)
                    if media_links:
                        print(
                            f"instagram media fetched via graphql "
                            f"(doc={doc_id}, path={path_type}, attempt={attempt + 1})"
                        )
                        return media_links, caption
                    errors.append(f"{doc_id}/{path_type}/attempt-{attempt + 1}: empty media list")
                except Exception as exc:
                    errors.append(f"{doc_id}/{path_type}/attempt-{attempt + 1}: {exc}")

    print(f"graphql failed for {shortcode}: {' | '.join(errors)}")
    return [], None


def get_instagram_media_links(shortcode, content_type="p"):
    return fetch_instagram_media(shortcode, content_type)
