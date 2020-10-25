def ticktack(*args):
    break_count = 0
    def iterator():
        while True:
            for item in args:
                if break_count < len(args):
                    yield item
                else:
                    return
    
    def breaker(should_break):
        nonlocal break_count
        break_count = break_count + 1 if should_break else 0

    return iterator, breaker