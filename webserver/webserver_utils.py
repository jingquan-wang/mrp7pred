from datetime import datetime
import string
import random
import os
import pandas as pd
from pandas import DataFrame

from mrp7pred.mrp7pred import MRP7Pred
from mrp7pred.utils import get_molweight, draw_molecule, standardize_smiles
from typing import Optional, Dict, List
import numpy as np

## uploading specs ##
UPLOAD_FOLDER = "./data/"


def ensure_folder(path: str) -> None:
    if not os.path.isdir(path):
        os.mkdir(path)


def get_current_time() -> str:
    now = datetime.now()
    return now.strftime("%Y%m%d")


def random_string(N: int) -> str:
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(N)
    )


def get_predictions(
    df: DataFrame, clf_dir: str, selected_features: Optional[str] = None
):
    m7p = MRP7Pred(clf_dir=clf_dir)
    selected_features_arr = np.load(selected_features)
    out = m7p.predict(
        compound_df=df,
        selected_features_arr=selected_features_arr,
        prefix=f"{get_current_time()}",
    )
    out = out.sort_values(by=["score"], ascending=False)
    # print(out.head())
    return out


def generate_report_dict_list(out: DataFrame) -> List[Dict[str, str]]:
    """
    Generate html report from prediction output

    Sample input:
       name                               smiles  pred     score
    0  cAMP  Nc1ncnc2c1ncn2C1OC2COP(=O)(O)OC2C1O     0  0.394112

    Sample output:
    {
        'name': 'cAMP',
        'svg': svg,
        'smiles': 'Nc1ncnc2c1ncn2C1OC2COP(=O)(O)OC2C1O',
        'mw': mw,
        'score': score,
        'is_modulator': 'yes/no',
    }
    """
    report_d_l = []
    for row in out.itertuples():
        report_d = dict()
        smiles = getattr(row, "smiles")
        report_d["name"] = getattr(row, "name")
        report_d["smiles"] = standardize_smiles(smiles)
        report_d["score"] = round(getattr(row, "score"), 3)
        report_d["is_modulator"] = "Yes" if getattr(row, "score") >= 0.5 else "No"
        report_d["mw"] = get_molweight(smiles)
        report_d["svg"] = draw_molecule(smiles, subImgSize=(300, 200))
        report_d_l.append(report_d)
    return report_d_l