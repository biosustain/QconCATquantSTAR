# Copyright (C) 2020 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import pandas as pd
from argparse import ArgumentParser

def extractDDA(fullDDAresults):
    columns = fullDDAresults.columns
    experiments = [col for col in columns if "Abundances" in col]
    DDAresults = fullDDAresults[["Annotated Sequence","Modifications","Master Protein Accessions"]+experiments].copy()
    for pep in DDAresults["Annotated Sequence"].unique():
        pos = [n for n in range(len(pep)) if pep.find('.', n) == n]
        seq_pep = pep[pos[0]+1:pos[1]]
        DDAresults.loc[DDAresults["Annotated Sequence"] == pep, "Annotated Sequence"] = seq_pep
    DDAresults.loc[DDAresults["Modifications"].isna(), "Modifications"] = "unlabel"
    for mod in DDAresults["Modifications"].unique():
        if "13C" in mod:
            DDAresults.loc[DDAresults["Modifications"] == mod, "Modifications"] = "label13C"
        else:
            DDAresults.loc[DDAresults["Modifications"] == mod, "Modifications"] = "unlabel"

    return DDAresults, experiments

def quantification(DDAresults,QconCATs,experiments):
    DDAheavypep = DDAresults.loc[(DDAresults["Modifications"] == "label13C"), ["Annotated Sequence", "Master Protein Accessions"]].drop_duplicates(subset="Annotated Sequence")
    for exp in experiments:
        for pep in DDAheavypep["Annotated Sequence"].unique():
            intensity = DDAresults.loc[(DDAresults["Annotated Sequence"] == pep) & (DDAresults["Modifications"] == "label13C"), exp].dropna()
            if intensity.any():
                DDAheavypep.loc[(DDAheavypep["Annotated Sequence"] == pep), exp] = intensity.sum()
    DDAlightpep = DDAresults.loc[(DDAresults["Modifications"] == "unlabel"), ["Annotated Sequence", "Master Protein Accessions"]].drop_duplicates(subset="Annotated Sequence")
    for exp in experiments:
        for pep in DDAlightpep["Annotated Sequence"].unique():
            intensity = DDAresults.loc[(DDAresults["Annotated Sequence"] == pep) & (DDAresults["Modifications"] == "unlabel"), exp].dropna()
            if intensity.any():
                DDAlightpep.loc[(DDAlightpep["Annotated Sequence"] == pep), exp] = intensity.sum()

    QconCATpep = list(QconCATs["FullPeptideName"])
    for i, exp in enumerate(experiments):
        for pep in QconCATpep:
            if pep in DDAheavypep["Annotated Sequence"].unique():
                heavy = DDAheavypep.loc[(DDAheavypep["Annotated Sequence"] == pep), exp].dropna()
                light = DDAlightpep.loc[(DDAlightpep["Annotated Sequence"] == pep), exp].dropna()
                if heavy.any() and light.any():
                    ratio = light.values[0]/heavy.values[0]
                    conc = QconCATs.loc[(QconCATs["FullPeptideName"] == pep), "Concentration"].values[0]
                    QconCATs.loc[(QconCATs["FullPeptideName"] == pep), "conc_sample"+str(i+1)] = ratio * conc

    QconCATproteins = QconCATs["ProteinName"].drop_duplicates().to_frame()
    for i, exp in enumerate(experiments):
        for prot in QconCATs["ProteinName"].unique():
            temp = QconCATs.loc[(QconCATs["ProteinName"] == prot), "conc_sample"+str(i+1)].dropna()
            if temp.any():
                QconCATproteins.loc[(QconCATproteins["ProteinName"] == prot), ["conc_sample"+str(i+1)]] = sum(temp)/len(temp)

    return QconCATproteins

def main():
    parser = ArgumentParser(description="Quantification of QconCAT endogenous proteins for STAR protocol")
    parser.add_argument("-i", action="store", dest="DDA_input_file", type=str, help="Input file (.CSV) with DDA PeptideGroups results from ProteomeDiscoverer")
    parser.add_argument("-Q", action="store", dest="QconCAT_file", type=str, help="Input file (.CSV) with QconCAT peptide sequences and concentrations")
    args = parser.parse_args()

    fullDDAresults = pd.read_csv(args.DDA_input_file,sep=",",header=0)
    QconCATs = pd.read_csv(args.QconCAT_file,sep=",",header=0)

    DDAresults, experiments = extractDDA(fullDDAresults)
    QconCATproteins = quantification(DDAresults,QconCATs,experiments)

    current = os.getcwd()
    QconCATproteins.to_csv(os.path.join(current,"QconCATproteins.csv"),sep=",",index=False)

if __name__ == "__main__":
    main()
