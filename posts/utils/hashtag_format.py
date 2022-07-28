from django.core.exceptions import ValidationError

import re

class HashtagFormatter:
    
    def hashtag_to_list(input_string):
        tag_list = input_string.split(",")
        hashtags = []
        for tag in tag_list:
            filtered_tag = re.search('#([0-9a-zA-Z\ ]+)$', tag.strip())
            if not filtered_tag:
                raise ValidationError("올바르지 못한 입력값입니다.")
            hashtags.append(filtered_tag.group(1))
        return hashtags
        
    def words_to_regex(input_string):
        word_list = list(map(lambda x:x.strip(), input_string.split(",")))
        filter_tags = []
        for word in word_list:
            if not word:
                raise ValidationError("올바르지 못한 검색값입니다,")
            filter_tags.append('^([0-9a-zA-Z]+\,)*%s(,[0-9a-zA-Z]+)*$'%word)
        return filter_tags
            
    