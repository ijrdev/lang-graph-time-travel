import schedule, time

from concurrent.futures import ThreadPoolExecutor

from src.graphs.main_graph import MainGraph

def init() -> None:
    try:
        # Busca na base os que estão diferente de finalizados.
        # Pega os novos ou marcados para serem reprocessados no time travel.
        subjects = []

        if len(subjects) > 0:
            with ThreadPoolExecutor(max_workers = 5) as executor:
                _ = [executor.submit(MainGraph().run, item) for item in subjects]
        else:
            print("Nenhum assunto foi capturado.")
    except Exception as ex:
        raise ex

if __name__ == "":
    try:
        schedule.every(5).seconds.do(init)

        print("⏳ Scheduler iniciado. Rodando jobs...")
        
        while True:
            schedule.run_pending()
            
            time.sleep(1)
    except Exception as ex:
        raise ex