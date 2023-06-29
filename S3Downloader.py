import boto3
import os
import csv
from threading import Thread

from botocore.config import Config

from singleton import Singleton
from utils import create_dir

BUCKET = 'redial'
SAVED_MODELS_DIR = "saved_models"
MAYACHEM_BIN_DIR = "mayachemtools/bin"
SCALERS_DIR = "scalers"
script_path = 'mayachemtools/bin/TopologicalPharmacophoreAtomTripletsFingerprints.pl'
s3 = boto3.client('s3')

class S3Downloader(metaclass = Singleton):
    def __init__(self):
        # self.s3 = boto3.client('s3')

        self.model_names = []
        self.models = []
        self.scaler_names = []
        self.scalers = {}

        self.load_model_names()
        self.load_models()
        self.load_scaler_names()
        self.load_scalers()

        create_dir(MAYACHEM_BIN_DIR)

        self.download_file(script_path)

    def load_model_names(self):
        names = []
        with open('saved_model_names.csv', newline='') as csvfile:
            data = csv.reader(csvfile)

            for row in data:
                names.append(row[0])
        self.model_names = names

    def load_obj(self, key):
        obj = s3.get_object(Bucket = BUCKET, Key = key)['Body'].read()
        
        return obj

    def load_models(self):
        for name in self.model_names:
            self.models.append([self.load_obj(name), name])

        print("loaded all models")

    def load_scaler_names(self):
        scalers = []
        with open("saved_scaler_names.csv", newline='') as csvfile:
            data = csv.reader(csvfile)

            for row in data:
                scalers.append(row[0])
        self.scaler_names = scalers

    def load_scalers(self):
        for name in self.scaler_names:
            self.scalers[name] = self.load_obj(name)

        print("loaded scalers")

    def get_scalers(self):
        return self.scalers

    def get_models(self):
        return self.models
    
    def download_file(self, key):
        s3.download_file(Bucket= BUCKET, Key = key, Filename = key)