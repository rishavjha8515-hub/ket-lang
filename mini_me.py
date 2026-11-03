LINES = {
        "collapsed": "I'd have picked 26,7 too, after overthinking it (No, i am just joking,why to confuse youself when you have favorite numbers.)",
        "tunnel_pass": "I would done siuuuuuu!",
        "tunnel_fail": "It's ok yaar, happens to everyone",
        "observed": "Being watched changes things. Would have felt during exams.",
}

def mini_me(event, **data):
    return " mini-Rishav: " + LINES[event].format(**data)

if __name__ == "__main__":
    print(mini_me("collapsed", value=1))