import logging
import os

# 로깅 설정 ----------------------------------------------------------------------------------------------
def setup_logging(log_file: str = "log.txt"):
    logging.basicConfig(
        level=logging.INFO,  # 로그 레벨 설정 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(levelname)s - %(message)s",  
        handlers=[
            logging.FileHandler(log_file),  # mode='w': 파일에 로그 저장, mode 기본은 append
            logging.StreamHandler()  # 콘솔 출력 (필요 없으면 제거 가능)
        ]
    )
    
# 환경 변수 값 가져오기 ---------------------------------------------------------------------------------
def get_env_var(key: str) -> str:
    value = os.getenv(key)
    if not value:
        logging.error(f"환경 변수 {key} 없음")
        raise ValueError(f"환경 변수 {key} 없음")
    return value