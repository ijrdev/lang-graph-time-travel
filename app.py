import schedule, time, logging, warnings, sys

from concurrent.futures import ThreadPoolExecutor

from pandas import DataFrame

from application.enums.status_enum import StatusEnum
from services.graphs.main_graph import MainGraph
from infrastructure.repositories.subjects_repository import SubjectsRepository

def init() -> None:
    try:
        df: DataFrame = SubjectsRepository.get_all([StatusEnum.PENDING.value, StatusEnum.REPROCESS.value])
                
        if len(df) > 0:
            subjects: list = df.to_dict("records")
            
            with ThreadPoolExecutor(max_workers = 5) as executor:
                _ = [executor.submit(MainGraph().run, item) for item in subjects]
        else:
            logging.info("⏬ Nenhum assunto foi capturado.")
    except Exception as ex:
        raise ex

if __name__ == "__main__":
    try:
        warnings.filterwarnings('ignore')
        
        logging.basicConfig(
            stream = sys.stdout, 
            level = logging.INFO, 
            encoding = "utf-8",
            datefmt = "%d/%m/%Y %H:%M:%S",
            format = "%(asctime)s - %(levelname)s - %(message)s",
        )
        
        logging.info("⏳ Scheduler iniciado!")
        
        init()
        
        # schedule.every(5).seconds.do(init)
        
        # while True:
        #     schedule.run_pending()
            
        #     time.sleep(1)
    except Exception as ex:
        logging.error(ex)
        
        exit(0)