# 카카오톡 대화파일에서 한 사람이 사용한 최빈다 단어 추출
from functions import setup_logging
import logging
import pandas as pd
from konlpy.tag import Okt
import re, sys, os

# 대화 내역에서 삭제할 정규 표현식 -------------------------------------------------------------------------
delete_patern_list = [
    re.compile(r'저장한 날짜 : \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'), # 헤더 패턴
    re.compile(r'--------------- \d{4}년 \d{1,2}월 \d{1,2}일 .요일 ---------------')  # 날짜 패턴
    ] 

# csv 파일 읽기 ---------------------------------------------------------------------------------------
def read_csv(file_path: str, sep: str = "\t")-> pd.DataFrame:
    for encoding in ['utf-8', 'euc-kr', 'cp949', 'utf-8-sig']:
        try:
            df = pd.read_csv(file_path, sep=sep, encoding=encoding)
            return df
        except UnicodeDecodeError: continue
        except Exception as e: raise Exception(f"{file_path}: {e}")
            
    return pd.DataFrame()

# 대화 파일 칼럼명 변경 ---------------------------------------------------------------------------------
def change_col_name(target_df: pd.DataFrame, new_col_name: str="대화내역")-> pd.DataFrame:
    if len(target_df.columns)==1:
        target_df.columns=[new_col_name]
        return target_df
    else: 
        raise ValueError("칼럼 값이 너무 많습니다. 카카오톡 대화파일이 맞는지 확인하세요.")

# 대화가 아닌 데이터(헤더 혹은 날짜 등) 삭제 ------------------------------------------------------------
def filter_valid_chat(df: pd.DataFrame, pattern_list: list)-> pd.DataFrame:
    def filter_invalid_pattern(df: pd.DataFrame, pattern: re.Pattern)->pd.DataFrame:
        df = df[~df.iloc[:, 0].astype(str).str.match(pattern)]  
        return df
    
    for p in pattern_list:
        df = filter_invalid_pattern(df, p)
    
    return df

# main -----------------------------------------------------------------------------------------------
def main(chat_file_path: str, target_name: str)-> list:
    setup_logging()
    
    logging.INFO("카카오톡 대화 파일 읽는 중")
    chat_df = filter_valid_chat(change_col_name(read_csv(chat_file_path)), delete_patern_list)
    
    