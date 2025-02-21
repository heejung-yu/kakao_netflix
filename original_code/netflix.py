from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import urllib
import pandas as pd

def content_crawling(word_list):
    #_____________넷플릭스 로그인 및 프로필 선택_______________
    # 크롬 드라이버 경로 지정
    driver = webdriver.Chrome('C:/Users/User/chromD/chromedriver.exe')
    login_form = {"id":"", "pw":""}

    # get 명령으로 접근하고 싶은 주소 지정
    url="https://www.netflix.com/browse"  
    driver.get(url)  #브라우저 접속

    #로그인 
    driver.implicitly_wait(3)  #대기
    driver.find_element_by_id('id_userLoginId').send_keys(login_form['id'])  #id값
    driver.find_element_by_id('id_password').send_keys(login_form['pw'])

    driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button').click()  #로그인 버튼
    driver.implicitly_wait(3)

    #넷플릭스 시청할 프로필 선택
    driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[1]/div/a/div/div').click() #프로필 버튼
    driver.implicitly_wait(3)
    print("넷플릭스 접속 완료")

    #__________________필요한 정보 크롤링_________________________
    from selenium.webdriver.common.keys import Keys

    content_list=[]  #2차원 리스트가 될 예정
    casting_list=[]
    genre_list=[]
    keyword_list=[]
    DB_key=1

    print("콘텐츠 크롤링 중..")
    for w in word_list:
        try:
            driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div/div/div[1]/div/button').click()  #검색창 클릭
        except Exception as e:
            pass
        driver.find_element_by_name("searchInput").send_keys(w)  #키워드 검색
        try :
            driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div/span[1]').click()
        except Exception as e:
            pass

        #_________________이미지 크롤링______________________
        page_source = driver.page_source  #페이지 소스 가져오기 
        soup = BeautifulSoup(page_source, "html.parser")
        driver.implicitly_wait(3)

        img = []
        imgList = soup.find_all("img")  #, _class="boxart-image boxart-image-in-padded-container", 클래스를 적으니까 안 됌
        del imgList[0]  #프로필 사진 제거

        src=[]; s=[]
        for i in range(5):  #상위 5개 컨텐츠만
            src=str(imgList).split()[-1] #이미지만 따로 추출하려는데 필요없는 정보 제거, imgList는 원래 nontype
            s=str(src).split('"')
            img.append(str(s))
            src=[]; s=[]
            
        #로컬 저장
        print("로컬 저장 중.. ", end="")
        for i in range(5):
            path="C:/Users/User/Desktop/논문/data/크롤링 이미지/"+str(i+1)+".png"  #저장할 로컬 주소
            urllib.request.urlretrieve(img[i], path)
            print("#", end= "")
        print("로컬 저장 완료")
        
        #___________________콘텐츠 크롤링_________________________
        for i in range(5):  #키값, xpath  !!!!!!!!!!!개수 5개로 수정!!!!!!!!!
            content=[]  #키값, 제목, 줄거리, 이미지 
            content.append(DB_key)  #키값

            title=""
            title=driver.find_element_by_xpath('//*[@id="title-card-0-'+str(i)+'"]/div[1]/a/div[1]/div/p').text  #제목
            content.append(title)
             
            #모달 이동
            modal=driver.find_element_by_css_selector("#title-card-0-"+str(i)+" > div.ptrack-content").click()
            driver.implicitly_wait(2)
            driver.get(driver.current_url)  #모달창으로 이동
            driver.implicitly_wait(3)

            story=""
            story=driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[3]/div/div[1]/div/div/div[1]/p/div').text  #줄거리 
            if story=="":
                story="NULL"
            else:
                content.append(story)   
                content_list.append(content)

            right_modal_list=driver.find_elements_by_class_name('previewModal--tags')  #오른쪽 출연, 장르, 키워드 모두 크롤링
            content_feature_list=[]
            
            for i in range(3):
                content_feature_list.append(list(right_modal_list[i].text.split(', ')))
            right_modal_list=[]
        
            for d in content_feature_list:  #필요없는 문자 제거
                if '더 보기' in d: d.remove('더 보기')
                edit=d[0].split(': ')
                d[0]=edit[1]

            casting=[]
            if len(content_feature_list[0])==0:
                casting.append("NULL")
                casting_list.append(casting)
            else:
                for c in content_feature_list[0]:  #출연진
                    casting.append(DB_key)
                    casting.append(c)
                    casting_list.append(casting)
                    casting=[]
                
            genre=[]
            if len(content_feature_list[1])==0:
                genre.append("NULL")
                genre_list.append(genre)
            else:           
                for c in content_feature_list[1]:  #장르
                    genre.append(DB_key)
                    genre.append(c)
                    genre_list.append(genre)
                    genre=[]
                
            keyword=[]
            if len(content_feature_list[2])==0:
                keyword.append("NULL")
                keyword_list.append(keyword)
            else:
                for c in content_feature_list[2]:  #키워드
                    keyword.append(DB_key)
                    keyword.append(c)
                    keyword_list.append(keyword)
                    keyword=[]
                    
            content_feature_list.clear()  #초기화

            DB_key+=1
            print("#", end="")
            driver.back()   #뒤로가기
            driver.implicitly_wait(3)
        driver.back()
            
    print("\n콘텐츠 정보 크롤링 완료")

    content_df=pd.DataFrame(content_list, columns=['key','img','title', 'story'])  #데이터 프레임에 크롤링한 정보 입력, 
    casting_df=pd.DataFrame(casting_list,columns=['key', 'name'])
    genre_df=pd.DataFrame(genre_list, columns=['key', 'genre'])
    keyword_df=pd.DataFrame(keyword_list,columns=['key','keyword'])
    
    #__________로컬 저장______________
    print("데이터 로컬 저장 중...")

    content_df.to_csv("C:/Users/User/Desktop/논문/data/결과/콘텐츠 정보.csv", header=False, encoding='euc-kr', index=False)  #저장할 로컬 주소
    casting_df.to_csv("C:/Users/User/Desktop/논문/data/결과/캐스팅 정보.csv", header=False, encoding='euc-kr', index=False)
    genre_df.to_csv("C:/Users/User/Desktop/논문/data/결과/장르 정보.csv", header=False, encoding='euc-kr', index=False)
    keyword_df.to_csv("C:/Users/User/Desktop/논문/data/결과/키워드 정보.csv", header=False, encoding='euc-kr', index=False)
    
    print("로컬 저장 완료")
    