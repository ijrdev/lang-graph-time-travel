import schedule, time, uuid, logging

from concurrent.futures import ThreadPoolExecutor

from src.graphs.main_graph import MainGraph

def init() -> None:
    try:
        # Busca na base os que estão diferente de finalizados.
        # Pega os novos ou marcados para serem reprocessados no time travel.
        subjects = [
            {"input": "World Hello", "thread_id": uuid.uuid4()},
        ]
        
        if len(subjects) > 0:
            with ThreadPoolExecutor(max_workers = 5) as executor:
                _ = [executor.submit(MainGraph().run, item) for item in subjects]
        else:
            logging.error("Nenhum assunto foi capturado.")
    except Exception as ex:
        raise ex

if __name__ == "__main__":
    try:
        logging.basicConfig(
            level = logging.INFO,
            format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt = '%d-%m-%Y %H:%M:%S'
        )
        
        logging.info("⏳ Scheduler iniciado...")
        
        init()
        
        # schedule.every(5).seconds.do(init)
        
        # while True:
        #     schedule.run_pending()
            
        #     time.sleep(1)
    except Exception as ex:
        logging.error(ex)
        
        exit(0)