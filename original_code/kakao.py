import operator
import pandas as pd
from konlpy.tag import Okt

def kakao_To_word_DF(file="KakaoTalkChats.txt", name=""):
    print("데이터 정제 중....")
    
    df=pd.read_csv(file, sep="\t", encoding="utf-8")
    data=[]
    
    #문자열에서는 삭제할 문자가 없어도 에러 안뜨는데 리스트는 뜬다
    deleteS=['ㅜ', 'ㅠ','ㅋ','ㅇ','𐌅','ㅗ']  #문자
    deleteL=['이모티콘','삭제된', '메시지','사진', '동영상']   #문자열

    #_________________데이터 정제- 필요없는 데이터들 지우기_______________________
    for i in range(len(df)):
        l=df.iloc[i,0].split(', ')  #리스트로 반환
        if len(l)>1:
            del l[0]  #날짜 정보 제거
            if len(l)>=1:
                l_str = str(l[0])
                l2=l_str.split(' : ')
            
                if l2[0] == name:  #특정 사용자만
                #불필요한 문자 삭제
                    for d in deleteL: 
                        if d in l2: l2.remove(d)

                    result=""
                    if len(l2)>1:
                        result = str(l2[1])
                        for d in deleteS: result=result.replace(d,'')
                        
                    if not result.isspace() and len(result)!=0: data.append(result)  #그래도 공백.
    print("#",end="")
    
    
    #___________최빈다 단어 계산+불용어 2차 제거___________________
    #명사만 추출, 빈도수 계산
    okt=Okt()
    words_freq={}

    #명사만 추출+빈도수 확인
    for d in data:
        n_list=okt.nouns(d) 
        for n in n_list:
            if len(n)!=1: 
                if n not in list(words_freq.keys()): words_freq[n]=1
                else: words_freq[n]=words_freq[n]+1

    sdict= sorted(words_freq.items(), key=operator.itemgetter(1),reverse=True) #내림차순 정렬 딕셔너리=>리스트, value값 기준 정렬
    print("#",end="")

    #________________불용어 사전_________________________
    # 빈 리스트 전달받을 때 
    try: 
        word_df=pd.DataFrame(sdict)
        word_df.columns=['단어', '빈도수']
    
        file2="C:/Users/User/Desktop/논문/data/불용어사전2.csv"
        stopword_df=pd.read_csv(file2, sep="\t",encoding='utf-8')

        for i in range(len(stopword_df)):
            stopword=stopword_df.iloc[i,0]
            
            idx=word_df[word_df['단어']==stopword].index
            word_df.drop(idx, inplace=True)  #inplace=True : 원본 데이터 프레임 위에 메소드를 적용
            #word_df=word_df[word_df.단어!=stopword]
        print("#")     
        
        word_df.to_csv("C:/Users/User/Desktop/test2/test2_"+name+".csv", encoding='utf-8-sig', index=False)
        
        
        print("로컬 저장 완료")
        return word_df['단어'].values.tolist()[:4]
      
    except Exception as e:
        print(e)