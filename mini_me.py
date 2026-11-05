LINES = {
        "collapsed": "I'd have picked 26,7 too, after overthinking it (No, i am just joking,why to confuse youself when you have favorite numbers.)",
        "tunnel_pass": "I would have done siuuuuuu!",
        "tunnel_fail": "It's ok yaar, happens to everyone",
        "observed": "Being watched changes things. Would have felt during exams.",
        "entangled": "Two particles, one fate.Like me and my best friend during exams.",
        "passport": "Checking ID wihout scaring it. I wish airports were like it.",
        "decohered": "Held it too long and it fell apart. Same as my attention in e-games"
}

def mini_me(event, **data):
    return " mini-Rishav: " + LINES[event].format(**data)

if __name__ == "__main__":
    print(mini_me("collapsed", value=1))