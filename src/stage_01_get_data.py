import argparse   
import shutil 
import logging 
from tqdm import tqdm 
import os 
import random
from src.utils.common import read_yaml, create_directories, unzip_file
import urllib.request as req


STAGE="GET_DATA"
logging.basicConfig(
    filename=os.path.join("logs","running_logs.log"),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s : %(module)s]: %(message)s",
    filemode="a"
)

def main(config_path):
    config=read_yaml(config_path)
    #print(config)
    URL=config["data"]["source_url"]
    #print(URL)
    local_dir=config["data"]["local_dir"]
    print(create_directories([local_dir]))
    data_file=config["data"]["data_file"]
    data_file_path=os.path.join(local_dir, data_file)
    logging.info("Download Started.......................")
    if not os.path.isfile(data_file_path):
        filename, headers=req.urlretrieve(URL, data_file_path)
        logging.info(f"filename: {filename} created with info {headers}")
    else:
        logging.info(f"filename: {data_file} already present.")
    
    #unzip operation
    unzip_data_dir=config["data"]["unzip_data_dir"]
    print(unzip_data_dir)
    create_directories([unzip_data_dir])
    unzip_file(source=data_file_path, dest=unzip_data_dir)







if __name__=='__main__':
    args=argparse.ArgumentParser()
    args.add_argument("--config","-c", default="configs/config.yaml")
    parsed_args=args.parse_args()

    try:
        logging.info("\n***********************************")
        logging.info(f">>>> stage {STAGE} started <<<<")
        main(config_path=parsed_args.config)
        logging.info(f">>>> stage {STAGE} Completed <<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
