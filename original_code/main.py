from kakao2 import kakao2 
from NETFLIX_CLASS import Netflix_content_crawling_class

talk=kakao2("", "")  #매개변수(파일 경로, 사용자 이름)
word_list = talk.main()  # 25개의 단어 긁어오기
print(word_list)

# test_list=['보고', '고민', '자식', '룸메', '선생님']
# # #test=Netflix_content_crawling_class(word_list)
# test=Netflix_content_crawling_class(test_list)
# test.run()

