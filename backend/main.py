from fastapi import FastAPI, File, UploadFile,Form
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UploadData(BaseModel):
    sampleName: str
    barcode: str
    chip: str
    lane: str
    datapath: str
    path: str
    content:List[dict]
class UploadData2(BaseModel):
    path: str
    content:List[dict]
    changes:List[dict]

def makenames(df:pd.DataFrame,col:str)->pd.DataFrame:
    s='_'+df.groupby(col).cumcount().add(1).astype(str)
    df.loc[:,col]+=s.mask(s=="_1","")
    return df

@app.post("/upload")
async def read_upload(file:UploadFile):
    contents = await file.read()
    df = pd.read_excel(contents)
    df.columns = ["n"+str(i+1) for i in range(df.shape[1])]
    df = df.fillna('')
    return df.to_dict(orient="records")

@app.post("/test")
async def process(uploading:UploadData):
    remotePath = uploading.path
    df = pd.DataFrame(uploading.content)
    df.columns = ["sampleName", "barcode", "chip", "lane", "dataPath"]
    df = df[df.dataPath!=""]
    df = makenames(df,"sampleName")
    df = df.assign(filename1=df.apply(lambda row : "_".join([row['chip'],row['lane'],str(row['barcode']),"1.fq.gz"]),axis=1))
    df = df.assign(filename2=df.apply(lambda row : "_".join([row['chip'],row['lane'],str(row['barcode']),"2.fq.gz"]),axis=1))
    cmd1 = "\n".join(df.apply(lambda row: "scp " + os.path.join(row['dataPath'],row['filename1']) + " " + os.path.join(remotePath,row['sampleName'] + "_R1.fastq.gz"),axis=1).tolist())
    cmd2 = "\n".join(df.apply(lambda row: "scp " + os.path.join(row['dataPath'],row['filename2']) + " " + os.path.join(remotePath,row['sampleName'] + "_R2.fastq.gz"),axis=1).tolist())
    return {"cmd1":cmd1,"cmd2":cmd2}

@app.post("/receivename")
async def reveives(file:UploadFile):
    df = pd.read_csv(file.file,header=None,delimiter="\t")
    df.columns = ["sampleName","trueName"]
    return df.to_dict(orient="records")

@app.post("/change")
async def change(uploading:UploadData2):
    df2 = pd.DataFrame(uploading.content)
    df2.columns = ["sampleName", "barcode", "chip", "lane", "dataPath"]
    df2 = df2[df2.dataPath!=""]
    df = pd.DataFrame(uploading.changes)
    df2 = df2.merge(df,how="left",on="sampleName")
    df2 = df2.drop(columns=["sampleName"])
    df2 = df2.rename(columns={"trueName":"sampleName"})
    df2 = makenames(df2,"sampleName")
    df2 = df2.assign(filename1=df2.apply(lambda row : "_".join([row['chip'],row['lane'],str(row['barcode']),"1.fq.gz"]),axis=1))
    df2 = df2.assign(filename2=df2.apply(lambda row : "_".join([row['chip'],row['lane'],str(row['barcode']),"2.fq.gz"]),axis=1))
    df2 = df2.dropna()
    cmd1 = "\n".join(df2.apply(lambda row: "scp " + os.path.join(row['dataPath'],row['filename1']) + " " + os.path.join(uploading.path,row['sampleName'] + "_R1.fastq.gz"),axis=1).tolist())
    cmd2 = "\n".join(df2.apply(lambda row: "scp " + os.path.join(row['dataPath'],row['filename2']) + " " + os.path.join(uploading.path,row['sampleName'] + "_R2.fastq.gz"),axis=1).tolist())
    return {"cmd1":cmd1,"cmd2":cmd2}