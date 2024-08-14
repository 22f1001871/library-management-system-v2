def raw(text):
    split_list=text.split()
    scrch_word=''
    for word in split_list:
        scrch_word+=word.lower()
    return scrch_word