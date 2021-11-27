#!/usr/bin/env python3

import os
import codecs
import json
import string
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup

import cache
cache.prefix = "20081103231349"


def add_games_json(d):
    g = get_games_json()
    for i, game in enumerate(g):
        if game["id"] == d["id"]:
            # Update instead
           g[i] = d
           break
    else:
        g.append(d)
    write_games_json(g)


def get_games_json():
    with open(os.path.join("..", "games.json"), "r") as f:
        return json.loads(f.read())


def write_games_json(g):
    with open(os.path.join("..", "games.json"), "w") as f:
        json.dump(g, f, ensure_ascii=True)

def get_RunContent_url(d, game, data):
    offset = data.find("AC_FL_RunContent(")
    if offset == -1:
        print(f"{d['name']} ({d['id']}): could not find AC_FL_RunContent(")
        return
    
    offset += len("AC_FL_RunContent(")
    offset = data.find("'src','", offset)
    if offset == -1:
        print(f"{d['name']} ({d['id']}): could not find 'src'")
        return

    offset += len("'src','")

    url = ""
    while data[offset] != "'":
        url += data[offset]
        offset += 1
    
    before_url = "http://web.archive.org" + game["href"]

    url_parts = url.split("?")
    if len(url_parts) == 2:
        url = url_parts[0] + ".swf?" + url_parts[1]
    else:
        url = url_parts[0] + ".swf"
    url = unquote(url)

    return before_url + url


def get_embed_url(d, game, data):
    offset = data.find("<embed src=\"/")
    if offset == -1:
        print(f"{d['name']} ({d['id']}): could not find <embed>")
        return

    offset += len("<embed src=\"/")-1
    url = ""
    while data[offset] != '"':
        url += data[offset]
        offset += 1
    
    return "http://web.archive.org" + url


def main():
    all_games_url = "http://web.archive.org/web/20081103231349/http://www.miniclip.com/games/en/full_games_list.php"

    data = cache.cache_or_url("allgames.txt", all_games_url)

    soup = BeautifulSoup(data, "html.parser")
    all_games = soup.select("div.gameWrapper>div.col>ul>li>a")

    for game in all_games:
        d = {
            "name": game.get_text(),
            "id": game["id"],
            "href": "",
            "description": "",
            "controls":  {},
        }

        data = cache.cache_or_url(d["id"], "http://web.archive.org" + game["href"])
        soup = BeautifulSoup(data, "html.parser")

        if "AC_SW_RunContent(" in data:
            print(f"Warning: {d['name']} ({d['id']}) is a Shockwave game, skipping")
            continue
        
        # Get game description
        gameInfo = soup.select_one("div#tab_Gameinfo>p")
        if gameInfo is not None:
            d["description"] = gameInfo.get_text()
        else:
            print(f"Warning: {d['name']} ({d['id']}): could not find Game Info")

        # Get controls
        controls = soup.select_one("div#tab_Gameinfo>ul.controls")
        if controls is not None:
            controls_items = controls.select("li")
            for li in controls_items:
                key = None
                arrows = li.select_one("img")
                div_key = li.select_one("div.key")
                print(d["id"])
                text = [x for x in li.stripped_strings]
                if len(text) == 0:
                    text = ""
                else:
                    text = text[-1]
                if arrows is not None:
                    if "icon_c_arrows.gif" in arrows["src"]:
                        key = "arrows"
                    elif "icon_c_lr.gif" in arrows["src"]:
                        key = "left_right"
                    elif "icon_c_down.gif" in arrows["src"]:
                        key = "down"
                    elif "icon_c_space.gif" in arrows["src"]:
                        key = "space"
                    elif "icon_c_up.gif" in arrows["src"]:
                        key = "up"
                    elif "icon_c_left.gif" in arrows["src"]:
                        key = "left"
                    elif "icon_c_right.gif" in arrows["src"]:
                        key = "right"
                    elif "icon_c_wasd.gif" in arrows["src"]:
                        key = "wasd"
                    elif "icon_c_enter.gif" in arrows["src"]:
                        key = "enter"
                    elif "icon_c_ctrl.gif" in arrows["src"]:
                        key = "ctrl"
                    elif "icon_c_end.gif" in arrows["src"]:
                        key = "end"
                    elif "icon_c_shift.gif" in arrows["src"]:
                        key = "shift"
                    elif "icon_c_numbers1.gif" in arrows["src"]:
                        key = "123"
                    elif "icon_c_numbers2.gif" in arrows["src"]:
                        key = "123456789"
                    elif "icon_c_backspace.gif" in arrows["src"]:
                        key = "backspace"
                    elif "icon_c_tab.gif" in arrows["src"]:
                        key = "tab"
                    elif "icon_c_ud.gif" in arrows["src"]:
                        key = "updown"
                    elif "icon_c_esc.gif" in arrows["src"]:
                        key = "escape"
                    elif "icon_c_mousemove.gif" in arrows["src"]:
                        key = "mouse"
                    elif "icon_c_mouseleft.gif" in arrows["src"]:
                        key = "mouse-left"
                    elif "icon_c_mouseright.gif" in arrows["src"]:
                        key = "mouse-right"
                    elif "icon_c_mousescroll.gif" in arrows["src"]:
                        key = "mouse-scroll"
                    else:
                        raise ValueError("Unknown arrows: " + arrows["src"])
                elif div_key is not None:
                    key = div_key.get_text()

                d["controls"][key] = text

        # Download SWF file
        filename = d["id"] + ".swf"
        ondisk_filename = os.path.join("..", "games", filename)
        d["href"] = "games/" + filename
        if os.path.isfile(ondisk_filename):
            print(f"Warning: {ondisk_filename} already exists, skipping download")
        else:
            url = get_RunContent_url(d, game, data)
            is_404 = False
            if url:
                r = requests.get(url, stream=True)
                with open(ondisk_filename, "wb") as f:
                    for c in r.iter_content(chunk_size=512):
                        if b"<!DOCTYPE html>" in c:
                            is_404 = True
                            break
                        f.write(c)
            
            if is_404 or not url:
                url = get_embed_url(d, game, data)
                if url:
                    r = requests.get(url, stream=True)
                    is_404 = False
                    with open(ondisk_filename, "wb") as f:
                        for c in r.iter_content(chunk_size=512):
                            if b"<!DOCTYPE html>" in c:
                                is_404 = True
                                break
                            f.write(c)
                
            if is_404 or not url:
                print(f"Warning: {d['name']} ({d['id']}) returned 404 twice")
                try:
                    os.unlink(ondisk_filename)
                except FileNotFoundError:
                    pass
                continue
        
        add_games_json(d)
        print(f"Successfully added {d['name']} => {filename}")
            


if __name__ == "__main__":
    main()